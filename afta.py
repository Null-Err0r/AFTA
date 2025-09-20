import sys
import subprocess
import os
import site
import psutil
import platform
import json
import tarfile
import shutil
import argparse
import logging
import hashlib
from datetime import datetime
import requests
import yaml

def setup_dependencies():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    venv_path = os.path.join(script_dir, ".venv")
    requirements_file = os.path.join(script_dir, "requirements.txt")

    if sys.platform == "win32":
        python_in_venv = os.path.join(venv_path, "Scripts", "python.exe")
        pip_in_venv = os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        python_in_venv = os.path.join(venv_path, "bin", "python")
        pip_in_venv = os.path.join(venv_path, "bin", "pip")

    if not os.path.exists(python_in_venv):
        print(f"Creating a virtual environment at: {venv_path}")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        except subprocess.CalledProcessError as e:
            print(f"Error creating virtual environment: {e}", file=sys.stderr)
            sys.exit(1)

    if not os.path.exists(requirements_file):
        print("requirements.txt not found. Creating it...")
        with open(requirements_file, "w") as f:
            f.write("requests\n")
            f.write("PyYAML\n")

    print(f"Installing dependencies into the virtual environment...")
    try:
        subprocess.check_call([pip_in_venv, "install", "-r", requirements_file])
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies into venv: {e}", file=sys.stderr)
        sys.exit(1)
    
    if sys.platform == "win32":
        site_packages = os.path.join(venv_path, "Lib", "site-packages")
    else:
        py_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
        site_packages = os.path.join(venv_path, "lib", py_version, "site-packages")

    if os.path.exists(site_packages) and site_packages not in sys.path:
        site.addsitedir(site_packages)
        print("Virtual environment is set up and ready.")

def run_command(command, shell=False):
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=False, shell=shell
        )
        if result.returncode != 0:
            if isinstance(command, list):
                cmd_str = ' '.join(command)
            else:
                cmd_str = command
            logging.warning(
                f"Command '{cmd_str}' finished with exit code {result.returncode}. Stderr: {result.stderr.strip()}"
            )
        return result.stdout.strip()
    except FileNotFoundError:
        logging.error(f"Command not found: {command[0]}")
        return "Error: Command not found."
    except Exception as e:
        cmd_str = ' '.join(command) if isinstance(command, list) else command
        logging.error(f"An unexpected error occurred while running command '{cmd_str}': {e}")
        return f"Error: {e}"

def load_config(config_path='config.yaml'):
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.error(f"Configuration file not found at {config_path}. Please create it.")
        exit(1)
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML configuration file: {e}")
        exit(1)

def download_latest_avml(output_dir):
    avml_path = os.path.join(output_dir, "avml")
    if os.path.exists(avml_path):
        logging.info("AVML already exists. Skipping download.")
        os.chmod(avml_path, 0o755)
        return avml_path

    logging.info("Attempting to download the latest version of AVML...")
    api_url = "https://api.github.com/repos/microsoft/avml/releases/latest"
    try:
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()
        assets = response.json().get("assets", [])
        download_url = next((asset["browser_download_url"] for asset in assets if asset["name"] == "avml"), None)

        if not download_url:
            logging.error("Could not find AVML download URL in the latest GitHub release.")
            return None

        logging.info(f"Downloading AVML from {download_url}...")
        with requests.get(download_url, stream=True, timeout=(15, 300)) as r:
            r.raise_for_status()
            with open(avml_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        logging.info(f"AVML downloaded successfully to {avml_path}")
        os.chmod(avml_path, 0o755)
        return avml_path
    except requests.RequestException as e:
        logging.error(f"Failed to download AVML: {e}")
        return None

def collect_system_info():
    logging.info("Collecting basic system information...")
    return {
        "timestamp": datetime.now().isoformat(),
        "hostname": platform.node(),
        "os_info": f"{platform.system()} {platform.release()} {platform.version()}",
        "architecture": platform.machine(),
        "current_user": os.getlogin(),
        "uptime": run_command(["uptime", "-p"]),
        "disk_usage": run_command(["df", "-h"]),
        "loaded_kernel_modules": run_command(["lsmod"]),
    }

def collect_process_info():
    logging.info("Collecting detailed process information...")
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'status', 'create_time', 'username']):
        try:
            p_info = proc.info
            p_info['create_time'] = datetime.fromtimestamp(p_info['create_time']).isoformat()
            p_info['parent'] = proc.ppid()
            processes.append(p_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

def collect_network_info():
    logging.info("Collecting network information...")
    connections = [conn._asdict() for conn in psutil.net_connections(kind='inet')]
    return {
        "connections": connections,
        "interfaces": run_command(["ip", "a"]),
        "routing_table": run_command(["ip", "r"]),
        "listening_ports": run_command(["ss", "-tulpn"]),
    }

def collect_filesystem_artifacts(output_dir, config):
    logging.info("Collecting filesystem artifacts...")
    fs_artifacts_dir = os.path.join(output_dir, "fs_artifacts")
    os.makedirs(fs_artifacts_dir, exist_ok=True)
    
    for log_file in config.get('log_files_to_copy', []):
        if os.path.exists(log_file):
            try:
                shutil.copy(log_file, fs_artifacts_dir)
                logging.info(f"Copied log file: {log_file}")
            except Exception as e:
                logging.warning(f"Could not copy {log_file}: {e}")

    user_dirs = [os.path.join('/home', d) for d in os.listdir('/home')] + ['/root']
    for user_dir in user_dirs:
        if not os.path.isdir(user_dir): continue
        
        for history_file in config.get('shell_history_files', []):
            src_path = os.path.join(user_dir, history_file)
            if os.path.exists(src_path):
                dest_path = os.path.join(fs_artifacts_dir, f"{os.path.basename(user_dir)}_{history_file}")
                shutil.copy(src_path, dest_path)
                logging.info(f"Copied shell history: {src_path}")
        
        ssh_keys_path = os.path.join(user_dir, ".ssh", "authorized_keys")
        if os.path.exists(ssh_keys_path):
            dest_path = os.path.join(fs_artifacts_dir, f"{os.path.basename(user_dir)}_authorized_keys")
            shutil.copy(ssh_keys_path, dest_path)
            logging.info(f"Copied SSH keys: {ssh_keys_path}")

def hash_critical_binaries(config):
    logging.info("Hashing critical binaries...")
    hashes = {}
    for dir_path in config.get('directories_to_hash', []):
        if os.path.isdir(dir_path):
            for root, _, files in os.walk(dir_path):
                for name in files:
                    file_path = os.path.join(root, name)
                    if not os.path.isfile(file_path):
                        continue
                    if not os.access(file_path, os.X_OK): continue
                    try:
                        with open(file_path, 'rb') as f:
                            sha256_hash = hashlib.sha256(f.read()).hexdigest()
                            hashes[file_path] = sha256_hash
                    except Exception as e:
                        logging.warning(f"Could not hash {file_path}: {e}")
    return hashes

def find_suid_sgid_files():
    logging.info("Searching for SUID/SGID files...")
    command = "find / -type f -perm /6000 -ls 2>/dev/null"
    return run_command(command, shell=True)

def create_memory_dump(avml_path, output_dir):
    logging.info("Attempting to create memory dump with AVML...")
    if not avml_path or not os.path.exists(avml_path):
        logging.error(f"AVML tool not found at {avml_path}. Skipping memory dump.")
        return None
    
    dump_path = os.path.join(output_dir, "memory.mem")
    command = [avml_path, dump_path]
    
    try:
        logging.info(f"Executing: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        logging.info(f"Memory dump successfully created at {dump_path}")
        if result.stderr:
            logging.warning(f"AVML reported warnings:\n{result.stderr}")
        return dump_path
    except subprocess.CalledProcessError as e:
        logging.error(f"Error creating memory dump with AVML. Return code: {e.returncode}\nStderr: {e.stderr}")
        return None

def main():
    if os.geteuid() != 0:
        print("This script must be run as root. Please use `sudo`.")
        return

    config = load_config()
    
    output_dir_base = config.get('output_dir', 'forensics_output')
    timestamp_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_dir = f"{output_dir_base}_{platform.node()}_{timestamp_str}"
    os.makedirs(output_dir, exist_ok=True)

    log_file_path = os.path.join(output_dir, 'forensics_run.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )
    
    logging.info("--- Starting Advanced Live Forensics Data Collection ---")
    
    report = {}
    if config['collection_toggles']['system_info']:
        report["system_info"] = collect_system_info()
    if config['collection_toggles']['process_info']:
        report["processes"] = collect_process_info()
    if config['collection_toggles']['network_info']:
        report["network"] = collect_network_info()
    if config['collection_toggles']['suid_sgid_files']:
        report["suid_sgid_files"] = find_suid_sgid_files().splitlines()
    if config['collection_toggles']['filesystem_artifacts']:
        collect_filesystem_artifacts(output_dir, config['filesystem'])
    if config['collection_toggles']['hash_critical_binaries']:
        report["binary_hashes"] = hash_critical_binaries(config['hashing'])
    
    if config['collection_toggles']['memory_dump']:
        avml_path = download_latest_avml(os.path.dirname(os.path.realpath(__file__)))
        if avml_path:
            dump_path = create_memory_dump(avml_path, output_dir)
            if dump_path:
                report["memory_dump_path"] = os.path.basename(dump_path)

    report_filename = os.path.join(output_dir, "report.json")
    with open(report_filename, 'w') as f:
        json.dump(report, f, indent=4, default=str)
    
    logging.info("Data collection complete. Compressing output...")
    
    archive_name = os.path.basename(output_dir)
    shutil.make_archive(archive_name, 'zip', output_dir)
    
    logging.info(f"All data saved and compressed to '{archive_name}.zip'")
    
    shutil.rmtree(output_dir)
    logging.info("Cleanup complete.")


if __name__ == "__main__":
    setup_dependencies()
    main()
