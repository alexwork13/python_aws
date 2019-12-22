import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='52.214.40.131', username='ubuntu', key_filename='/home/user/aws_script/awstest.pem')

stdin, stdout, stderr = ssh.exec_command('ls -la')

for line in stdout.read().splitlines():
    print(line)

ssh.close()
