import paramiko
from getconfig import get_config_values
import sys

def createConnect():
    host = get_config_values('data','host')
    user = get_config_values('data','user')
    password = get_config_values('data', 'password')
    port = get_config_values('data', 'port')
    #print(host,user,password,port)
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, user, password, timeout=5)
        return ssh
    except:
        print('ssh connect error!')
        sys.exit()

def execCommand(command,ssh):
    remote_path = get_config_values('data','remote_path')
    command = "cd "+remote_path+" && "+ command
    stdin, stdout, stderr =  ssh.exec_command(command)
    out = stdout.read()
    return out

def uploadFile(file):
    host = get_config_values('data','host')
    user = get_config_values('data','user')
    password = get_config_values('data', 'password')
    remote_path = get_config_values('data','remote_path')
    try:
        t = paramiko.Transport((host, 22))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(file,remote_path+file)
        t.close()
        return '文件上传成功'
    except Exception as e:
        print('upload file error!')
        sys.exit()

