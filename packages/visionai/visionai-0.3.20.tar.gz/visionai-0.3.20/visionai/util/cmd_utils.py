import sys
from pathlib import Path
import os
import docker
import typer
import json


FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # visionai/visionai directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH


from visionai.util.license_server_services import LicenseServerCommunication

license_server_com =  LicenseServerCommunication()


import uuid
from cryptography.fernet import Fernet
from datetime import datetime,timedelta
from config import CONFIG_FILE

SECRET_FILE_PATH = ROOT / 'config' / 'secret.txt'
KEY = b"MHHD3HQDKlkN8Z69mQeNbzzsvEAtRdLKImH1Z1NmjE0="  # Should be 32 url-safe base64-encoded bytes
cipher_suite = Fernet(KEY)



def get_mac_address() -> str:
    mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                    for elements in range(0,2*6,2)][::-1])
    return mac


def save_registration_data(company:str,
                           license_type:str="trial",
                           license_end_date:str=None,
                           sites:int=1,
                           is_trial:bool=True,
                           action_type:str="create"):
    '''
    save registration data to secret.txt file
    and push to visionify license server
    '''
    current_mac = get_mac_address()
    if not license_end_date:
        today = datetime.now()
        trail_data = today + timedelta(days=90)
        license_end_date = trail_data.strftime('%Y-%m-%d')
    license_key = f'{company}_{current_mac}_{str(license_end_date)}_{license_type}_{sites}'
    registration_data = (license_key).encode()
    encrypted_data = cipher_suite.encrypt(registration_data)
    with open(SECRET_FILE_PATH, 'w') as f:
        f.write(encrypted_data.decode())

    # push to visionify license server
    license_data = {
        "company":company,
        "trial":is_trial,
        "scenarios":"PPE Compliance",
        "pricing":0,
        "license":f'{company}_{license_type}',
        "cameras":5,
        "customer":company,
    }
    if action_type == "create":
        license_server_com.create_license(license_data)



def is_registered() -> bool:
    status = {
        "status":"registered",
        "days_left":0
    }
    if not os.path.exists(SECRET_FILE_PATH):
        status["status"] = "not_registered"
        return status
    
    with open(SECRET_FILE_PATH, 'r') as f:
        encrypted_data = f.read().encode()

    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    created_date = datetime.strptime(decrypted_data.split("_")[2],"%Y-%m-%d")    
    current_date = datetime.now()

    days_difference = (created_date - current_date).days
    if days_difference < 0:
        status["status"] = "expired"
        return status
        
    status["days_left"] = days_difference
    # current_mac = get_mac_address()
    # expected_data = current_mac + "_registered"
    return status



def update_license(license_txt:str):
    '''
    update license with new license key
    '''
    decrypted_data = cipher_suite.decrypt(license_txt).decode()
    company = decrypted_data.split("_")[0]
    date_string = decrypted_data.split("_")[2]
    license_end_date = datetime.strptime(date_string,"%Y-%m-%d").date()
    license_type = decrypted_data.split("_")[3]
    sites = decrypted_data.split("_")[4]
    if license_type == "trial":
        is_trial = True
    else:
        is_trial = False
    save_registration_data(company=company,
                           license_type=license_type,
                           license_end_date = license_end_date,
                           sites=sites,
                           is_trial=is_trial,
                           action_type="update")



def print_container_status(container_name, tail):
    try:
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - -')
        print(f'{container_name} status....')
        client = docker.from_env()
        ctainer = client.containers.get(container_name)
        ctainer_status = typer.style(ctainer.status, fg=typer.colors.WHITE, bg=typer.colors.GREEN)
        typer.echo(f"{container_name}: {ctainer_status}")
        logs = ctainer.logs(tail=tail)
        log_message= logs.decode("utf-8")
        print(log_message)
        web_service_port_message = typer.style(json.dumps(ctainer.ports), fg=typer.colors.WHITE, bg=typer.colors.GREEN)
        typer.echo(web_service_port_message)
        print('- - - - - - - - - - - - - - - - - - - - - - - - - - -')

    except docker.errors.NotFound:
        message = typer.style(f"{container_name} not running", fg=typer.colors.WHITE, bg=typer.colors.RED)
        typer.echo(message)