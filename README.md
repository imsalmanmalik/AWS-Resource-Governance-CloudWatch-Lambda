## Overview

The Lambda function is designed to be triggered by CloudWatch Events for EC2 volume modifications and EBS snapshot creations.

In this function, we first check if the resource ARN in the event data is for a volume or a snapshot.

1. If it's a volume, the function modifies the volume, creates a snapshot, and adds the tag to the snapshot.<b>
2. If it's a snapshot, the function adds the tag to the snapshot directly.<b>

This function would work for both volume modification events and snapshot creation events.

## Project Scope

- Unsecure S3 buckets: Lambda functions can be used to monitor S3 bucket access and enforce security policies, such as preventing public access, encrypting data at rest, and logging all access activity.<b>

- No optimization of EC2 instances: Lambda functions can be used to monitor CPU utilization and other metrics of your EC2 instances, and automatically adjust the instance size or capacity based on the workload. This can help optimize performance and reduce costs.<b>

- No automation of backups and disaster recovery: Lambda functions can be used to schedule backups and automate disaster recovery processes, such as copying data to a backup S3 bucket or launching a new EC2 instance in case of a failure.<b>

- No automation of routine tasks: Lambda functions can be used to automate routine tasks, such as database backups, log analysis, and file processing. This can help reduce manual effort and improve efficiency.<b>

- IAM permissions and roles: Lambda functions can be used to enforce IAM policies and roles, such as granting least privilege access and rotating access keys. This can help improve security and compliance.<b>

## High Level Design

![55D21237-CECD-47D1-95EB-E5C97F84758D_1_201_a](https://github.com/imsalmanmalik/AWS-Resource-Governance-CloudWatch-Lambda/assets/121328365/9fa75fdf-3066-4081-92d3-ade6912d4c8d)


## Getting Started

# Prerequisites

- AWS account with access to EC2, Lambda, and CloudWatch Services
- AWS CLI installed and configured
- Python 3.6 or higher
- An EC2 volume to perform operations on
  
## Deploying the Lambda Function

- Clone this repository to your local machine.<b>
- Navigate to the AWS Lambda console and create a new function.<b>
- In the function code section, upload the code from this repository.<b>
- Make sure your Lambda function has the necessary IAM permissions. It should have access to ec2:ModifyVolume, ec2:CreateSnapshot, and ec2:CreateTags actions.<b>
- In the function triggers section, set up a new CloudWatch Event trigger. The event pattern should match EBS volume modification events and EBS snapshot creation events.<b>
- Save your function.<b>
  
## Testing the Function

You can test the function by manually changing the size or type of your EC2 volume, or creating a snapshot. Check the CloudWatch Logs for your function to verify that it's working as expected.

## Screenshots

1. This screenshot shows the CloudWatch log groups for the invoking Lambda function and helps in debugging and monitoring. Could also assist in understanding how 'event' is being parsed onto the Lambda function as a json payload. You can do this by adding `print(event)` at the top of your handler function and checking the logs after the function is triggered. Once you know the structure of the event object, you can adjust your function code accordingly. <b>

<img width="1280" alt="cloudwatch_log_groups" src="https://github.com/imsalmanmalik/AWS-Resource-Governance-CloudWatch-Lambda/assets/121328365/8c23ce24-f2cb-4bcc-827d-5379f61a5118">


2. This screenshot shows the Lambda console which shows an `EventBridge` between the Lambda function named as `resource_governance` and CloudWatch.<b>

<img width="1261" alt="lambda_console" src="https://github.com/imsalmanmalik/AWS-Resource-Governance-CloudWatch-Lambda/assets/121328365/6628ff3c-8543-4669-84eb-98fc7949a66f">

3. This screenshot shows the EBS console which displays how the invoking Lambda function adds a `Tag Key` and `Tag Value` to a newly created snapshot.<b>

<img width="1275" alt="snapshot_tag" src="https://github.com/imsalmanmalik/AWS-Resource-Governance-CloudWatch-Lambda/assets/121328365/cb27ad1f-3450-4007-8a88-8b3af003948f">
