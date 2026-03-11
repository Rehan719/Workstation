# AWS Free Tier Setup

## 🚀 Free Tier Services
- **EC2**: 750 hours per month of t2.micro (12 months).
- **Lambda**: 1 million free requests per month (Always free).
- **S3**: 5 GB of standard storage (12 months).
- **DynamoDB**: 25 GB of storage (Always free).

## 📝 Setup Instructions
1. Create an [AWS Account](https://aws.amazon.com/free).
2. Go to IAM Console and create a new user 'JulesDeployer'.
3. Attach 'AmazonS3FullAccess' and 'AWSLambda_FullAccess'.
4. Obtain Access Key ID and Secret Access Key.
5. Set 'AWS_ACCESS_KEY_ID' and 'AWS_SECRET_ACCESS_KEY' in your environment.
