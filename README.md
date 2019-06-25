# aws-cf-drift-detector
A simple cloudformation stack to monitor all cloudformation stacks and find drifts. Detected drifts are send to SNS topic 

while in `packages` folder:
```bash
pip install -r requirements.txt -t .
```

to install never versions of boto3 and boto3core needed to access drift detection api