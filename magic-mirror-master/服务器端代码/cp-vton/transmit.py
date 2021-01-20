import paramiko  # 用于调用scp命令
from scp import SCPClient


def ssh_scp_put(ip, username, password, local_file, remote_path):

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname=str(ip), port=22, username=username, password=password)

    scp = SCPClient(ssh.get_transport())
    scp.put(local_file, recursive=True, remote_path=remote_path)
    scp.close()


def remote_scp(host_ip, remote_path, local_path, username, password):
    try:
        t = paramiko.Transport((host_ip, 22))
        t.connect(username=username, password=password) # 登录远程服务器
        sftp = paramiko.SFTPClient.from_transport(t) # sftp传输协议
        src = remote_path
        des = local_path
        sftp.get(src, des) #下载文件
        # sftp.put(updatepath_file(),src) #上传文件
        t.close()
    except IOError as e:
        print(e)


if __name__ == '__main__':
    ip = "10.33.32.5"
    username = "sice"
    password = "sice123456"

    local_up = "./data/test/cloth/004325_1.jpg"
    remote_up = "/home/sice/cp-vton-master/picture/004325_1.jpg"
    local_down = "./data/test/tom_final.pth/test/try-on/004325_1.jpg"
    remote_down = "/home/sice/cp-vton-master/picture/004325_1.jpg"

    ssh_scp_put(ip, username, password, local_up, remote_up)
    print("finished up")
    remote_scp(ip, remote_down, local_down, username, password)
    print("finished down")

