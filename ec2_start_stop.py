import boto3
import botocore
import paramiko
import logging




ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='52.214.222.102', username='ubuntu', key_filename='/home/user/aws_script/awstest.pem')

bash_script = open("/home/user/aws_script/script.sh").read()
stdin, stdout, stderr = ssh.exec_command(bash_script)

for line in stdout.read().splitlines():
    print(line)

ssh.close()