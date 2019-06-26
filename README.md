# aws-cf-drift-detector
A simple cloudformation stack to monitor all cloudformation stacks and find drifts. Detected drifts are send to SNS topic 

while in `packages` folder:
```bash
pip install -r requirements.txt -t .
```

to install never versions of boto3 and boto3core needed to access drift detection api.

Also check out `deploy.sh` script to know what's going on and to configure s3 bucket for stack code

### Prerequisites needed to deploy
* AWS CLI
* AWS SAM