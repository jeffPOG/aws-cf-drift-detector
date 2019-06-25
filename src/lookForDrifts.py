import logging
import os
import time
import sys

# needed because boto3 version in lambda env is 1.7.x and all functions regarding drifts were introduced in 1.9.X
sys.path.insert(0, os.environ["LAMBDA_TASK_ROOT"] + "/packages/")

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

REGIONS = ['eu-west-1']
BAD_STATUSES = ['CREATE_IN_PROGRESS', 'CREATE_FAILED', 'ROLLBACK_FAILED', 'DELETE_FAILED', 'UPDATE_ROLLBACK_FAILED',
                'UPDATE_IN_PROGRESS', 'REVIEW_IN_PROGRESS', 'DELETE_IN_PROGRESS', 'ROLLBACK_COMPLETE']

sns = boto3.client('sns')


def lambda_handler(event, context):
    for region in REGIONS:

        cf = boto3.resource('cloudformation', region_name=region)
        cf_client = boto3.client('cloudformation', region_name=region)

        stacks_to_check = [stack for stack in cf.stacks.all() if stack.stack_status not in BAD_STATUSES]
        logger.info('Region: ' + region + ' Stacks to check: ' + str([stack.name for stack in stacks_to_check]))

        # start stacks drift detection
        drift_detection_ids = {}
        for stack in stacks_to_check:
            drift_detection_info = cf_client.detect_stack_drift(StackName=stack.name)
            drift_detection_ids[stack.name] = drift_detection_info['StackDriftDetectionId']
            time.sleep(.1)

        time.sleep(5)

        # check for detection statuses and produce messages for drifted stacks
        for stack_name, drift_detection_id in drift_detection_ids.items():
            status_info = cf_client.describe_stack_drift_detection_status(StackDriftDetectionId=drift_detection_id)

            while status_info['DetectionStatus'] == 'DETECTION_IN_PROGRESS':
                time.sleep(2)
                status_info = cf_client.describe_stack_drift_detection_status(StackDriftDetectionId=drift_detection_id)

            if status_info['StackDriftStatus'] == 'IN_SYNC':
                logger.info('Stack: ' + stack_name + ' OK')

            if status_info['StackDriftStatus'] == 'DRIFTED':
                stack_id = status_info['StackId']
                url = "https://" + region + ".console.aws.amazon.com/cloudformation/home?region=" + \
                      region + "#/stack/detail?stackId=" + stack_id
                logger.info('Stack: ' + stack_name + ' has drifted')
                msg = "Stack: " + stack_name + " has drifted.\n"
                msg = msg + "Check details: " + url
                sns.publish(TopicArn=os.environ['SNS_TOPIC'], Message=msg,
                            Subject='Stack drifted: ' + stack_name)
