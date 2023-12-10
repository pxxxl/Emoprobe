import json
import os
import paramiko
import zipfile


def get_config_path():
    script_path = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_path)
    config_path = os.path.join(script_dir, 'config.json')
    return config_path


def get_ssh_path():
    script_path = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_path)
    config_path = os.path.join(script_dir, 'password.json')
    return config_path


def get_frontend_dir_path(relative_path: str) -> str:
    script_path = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_path)
    frontend_dir_path = os.path.join(script_dir, relative_path)
    return frontend_dir_path


def print_progress(transferred, total):
    print(f"Progress: {transferred}/{total}")

def upload_directory(ssh, sftp, local_dir_path, remote_dir_path):
    # first compress, use zip folder in the deployment directory
    local_zip_path = os.path.join(os.path.dirname(local_dir_path), 'frontend.zip')
    # use python zip library to zip the folder
    with zipfile.ZipFile(local_zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(local_dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, local_dir_path))
    # then upload the zip file
    sftp.put(local_zip_path, remote_dir_path + '.zip', callback=print_progress)
    # then unzip the zip file, use Linux command
    stdin, stdout, stderr = ssh.exec_command(f"unzip {remote_dir_path}.zip -d {remote_dir_path}")
    # then delete the zip file
    sftp.remove(remote_dir_path + '.zip')
    # then delete the local zip file
    os.remove(local_zip_path)


def print_progress(transferred, total):
    percentage = transferred / total * 100
    print(f"Uploaded: {transferred}/{total} bytes ({percentage:.2f}%)")
    

if __name__ == '__main__':
    with open(get_config_path(), 'r', encoding='utf-8') as file:
        config = json.load(file)

    with open(get_ssh_path(), 'r', encoding='utf-8') as file:
        ssh_config = json.load(file)

    frontend_dir = config['frontend_dir']
    local_relative_frontend_dir = config['local_relative_frontend_dir']
    local_frontend_dir = get_frontend_dir_path(local_relative_frontend_dir)

    ip = ssh_config['ip']
    port = ssh_config['port']
    username = ssh_config['username']
    password = ssh_config['password']

    # now use ssh ftp to upload the backend jar
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password)

    sftp = ssh.open_sftp()
    # first, if old frontend dir exists, delete the old frontend dir
    try:
        sftp.stat(frontend_dir)
        sftp.rmdir(frontend_dir)
        print(f"Deleted old frontend directory: {frontend_dir}")
    except FileNotFoundError:
        pass
    # then recursively upload the new frontend dir
    upload_directory(ssh, sftp, local_frontend_dir, frontend_dir)

    sftp.close()
    ssh.close()

    print('Deployed frontend to remote server.')