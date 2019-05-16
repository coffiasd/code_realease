# encoding=utf-8
import sys
import subprocess
from getconfig import *
import time
import ssh_command
import hashlib

#dir = os.system("dir")
# git log --pretty=format:"%H:%s" -1 查看历史版本
# git diff 5cf2c0524b1cec19969205e6b46e0e86b4d49498 77403bb66cad45f728f82f1dad4858602499f474 --name-only |xargs tar -rf up2.tar

#获得本地最近的版本号
def getLastCommit():
    last_commit = subprocess.Popen('git log --pretty=format:"%H:%s" -1',shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').split(':')
    #print(last_commit) ['commitid':'tag']
    return last_commit[0],last_commit[1]

#获得远程版本号
def getRemoteCommit():
    return get_config_values('data','remote_last_commit')

#通过对比两个版本号打包文件
def tarFile(commit1,commit2):
    command = "git diff "+commit1+" "+ commit2+ " --name-only"
    file_list = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').split('\n')
    pwd = subprocess.Popen("chdir",shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').replace('\\','/')
    absolute_path = []
    for i in range(len(file_list)):
        if getAllRoute(file_list[i],pwd):
            absolute_path.append(getAllRoute(file_list[i],pwd))
    #print(absolute_path)
    return tarFileList(absolute_path),absolute_path

#按照文件列表打包文件 tar -xvf a.tar
def tarFileList(absolute_path):
    str = ''
    for i in range(len(absolute_path)):
        str= str+absolute_path[i]+" "
    #print(str)
    name = time.strftime("%Y%m%d%H%I%S", time.localtime())
    os.system("tar -rf "+name+".tar "+str)
    return name+".tar"

#对比路径获得完整目录
# path1: e:/web-code77/code/battleTeam  path2:code/battleTeam
def getAllRoute(path1,path2):
    for i in range(len(path2)-2):
        str = path2[i:]
        if path1.strip().find(str.strip())==0:
            path1 = path1.replace(str.strip()+'/', '')
            return path1
    return False

def getDirByRoute(file):
    for i in range(len(file)):
        str = file[-i]
        if str =='/':
            break
    return file[:-i]

if __name__ == '__main__':
    #打包文件
    print('开始打包本地文件')
    commit1,tag = getLastCommit()
    commit2 = getRemoteCommit()
    filename,file_list = tarFile(commit1,commit2)
    print('开始上传本地文件')
    #上传文件
    ssh  = ssh_command.createConnect()
    ssh_command.uploadFile(filename)
    #执行命令
    out = ssh_command.execCommand("md5sum "+filename,ssh).decode('utf-8').split(' ')
    file = open(filename,'rb')
    md5 = hashlib.md5(file.read()).hexdigest()
    if md5 in out:
        print('远程文件对比成功')
    else:
        sys.exit('远程文件对比失败')
    #备份远程文件
    for i in range(len(file_list)):
        #print(file_list[i])
        file = file_list[i]
        route = getDirByRoute(file)
        #print("mkdir -p backup/"+file)
        ssh_command.execCommand("mkdir -p backup/"+route,ssh)
        ssh_command.execCommand("cp " + file+" backup/"+file, ssh)
    print('备份文件成功')
    #解压缩
    out = ssh_command.execCommand("tar -xvf "+filename, ssh).decode('utf-8').split('\n')
    print('上传文件列表:')
    for i in range(len(out)):
        print(out[i])
    #删除远程文件
    out = ssh_command.execCommand("rm -f " + filename, ssh).decode('utf-8').split('\n')
    #设置本地的最后一次commit_id
    set_config_values('data','remote_last_commit',commit1)
    print('上传结束')