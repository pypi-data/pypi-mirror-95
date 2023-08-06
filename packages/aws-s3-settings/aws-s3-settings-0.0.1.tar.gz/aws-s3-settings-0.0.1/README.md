# aws-s3-settings

The purpose of this project is very simple. Allow EC2 instances in an Auto Scaling Group named after Netflix standards to retrieve and expose environment variables from an S3 bucket.

The EC2 instances should use an IAM Role to allow reading those specific files only.

This will give your applicaton developers easy-to-use environment variables just like on Heroku or similar.
