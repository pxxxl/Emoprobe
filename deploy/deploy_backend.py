import json
import os
import paramiko


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


def get_jar_path(relative_jar_dir: str) -> str: 
    script_path = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_path)
    jar_dir = os.path.join(script_dir, relative_jar_dir)
    jar_name = None
    for file in os.listdir(jar_dir):
        if file.endswith('.jar'):
            jar_name = file
            break
    if jar_name is None:
        raise FileNotFoundError('No .jar file found in the directory.')
    return os.path.join(jar_dir, jar_name)


def print_progress(transferred, total):
    percentage = transferred / total * 100
    print(f"Uploaded: {transferred}/{total} bytes ({percentage:.2f}%)")

  
if __name__ == '__main__':
    with open(get_config_path(), 'r', encoding='utf-8') as file:
        config = json.load(file)

    with open(get_ssh_path(), 'r', encoding='utf-8') as file:
        ssh_config = json.load(file)

    backend_dir = config['backend_dir']
    backend_jar_name = config['backend_jar_name']
    local_backend_dir = config['local_backend_jar_relative_dir']
    local_backend_path = get_jar_path(local_backend_dir)
    remote_backend_path = os.path.join(backend_dir, backend_jar_name)

    ip = ssh_config['ip']
    port = ssh_config['port']
    username = ssh_config['username']
    password = ssh_config['password']

    # now use ssh ftp to upload the backend jar
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password)

    sftp = ssh.open_sftp()

    try:
        sftp.stat(remote_backend_path)
        sftp.rmdir(remote_backend_path)
        print(f"Deleted old frontend directory: {remote_backend_path}")
    except FileNotFoundError:
        pass

    sftp.put(local_backend_path, remote_backend_path, callback=print_progress)
    sftp.close()
    ssh.close()

    print('Deployed backend to remote server.')