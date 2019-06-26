#!/usr/bin/env bash

CODE_BUCKET_NAME="common-microservices-code"
ADMIN_MAIL="lukpep@gmail.com"

# validate template
sam validate

# check if s3 bucket exists
if aws s3 ls "s3://$CODE_BUCKET_NAME" 2>&1 | grep -q 'NoSuchBucket'
then
    echo "Bucket $CODE_BUCKET_NAME does not exists - creating ..."
    aws s3 mb s3://${CODE_BUCKET_NAME}
fi


# package and upload to S3
# IMPORTANT! common-microservices-code bucket must be present on AWS S3
sam package \
   --template-file template.yaml \
   --output-template-file generated-template.yaml \
   --s3-bucket ${CODE_BUCKET_NAME}

# deploy stack
sam deploy \
   --template-file generated-template.yaml \
   --stack-name DRIFT-DETECTOR-SERVICE \
   --capabilities CAPABILITY_IAM \
   --parameter-overrides AdminMail=${ADMIN_MAIL}