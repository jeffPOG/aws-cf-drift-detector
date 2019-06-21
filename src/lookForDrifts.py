import logging
import os
import sys

# needed because boto3 version in lambda env is 1.7.x and all functions regarding drifts were introduced in 1.9.X
sys.path.insert(0, os.environ["LAMBDA_TASK_ROOT"]+"/packages/")

import boto3
import botocore

logger = logging.getLogger()
logger.setLevel(logging.INFO)

REGIONS = ['eu-west-1']
BAD_STATUSES = ['CREATE_IN_PROGRESS', 'CREATE_FAILED', 'ROLLBACK_FAILED', 'DELETE_FAILED', 'UPDATE_ROLLBACK_FAILED',
                'UPDATE_IN_PROGRESS', 'REVIEW_IN_PROGRESS', 'DELETE_IN_PROGRESS', 'ROLLBACK_COMPLETE']


def lambda_handler(event, context):
    for region in REGIONS:
        print("boto3 version:" + boto3.__version__)
        logger.info('Looking for drifts in region: ' + region)

        cf = boto3.resource('cloudformation', region_name=region)
        stacks_to_check = [stack for stack in cf.stacks.all() if stack.stack_status not in BAD_STATUSES]
        logger.info('Stacks to check in this region: ' + str([stack.name for stack in stacks_to_check]))

        for stack in stacks_to_check:
            info = stack.drift_information
            logger.info(info)

        drift_detection_ids = {}


