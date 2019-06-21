#!/usr/bin/env bash

# validate template
sam validate

# package and upload to S3
# IMPORTANT! common-microservices-code bucket must be present on AWS S3
sam package \
   --template-file template.yaml \
   --output-template-file generated-template.yaml \
   --s3-bucket common-microservices-code

# deploy stack
sam deploy \
   --template-file generated-template.yaml \
   --stack-name DRIFT-DETECTOR-SERVICE \
   --capabilities CAPABILITY_IAM