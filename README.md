# AWS_EC2-Instance
Creating AWS EC2 instance using python and boto3
Make sure awscli and python3 is installed and aws lab is started and aws credentials are copied and pasted to credentials folder after starting each lab.
Alter the code accordingly if you do not want to create multiple key-pairs and security groups for ssh.
If awscli not installed follow the steps,
a. sudo apt update
b. sudo apt install awscli
c. sudo apt install python3-pip
d. pip3 install --upgrade awscli
e. mkdir ~/.aws
f. nano ~/.aws/credentials and copy the contents from AWS Details ==> Show in Start Lab Page
g. optional- aws configure and set the default region only if you are not adding the AWS region in python program.
h. aws ec2 describe-instances show any running instances.
