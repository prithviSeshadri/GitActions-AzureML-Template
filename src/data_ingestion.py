import argparse
import os
from datetime import datetime
from datetime import timezone
import warnings
import pandas as pd
import numpy as np
import azureml.core
from azureml.core import (
    Workspace,
    Experiment,
    Dataset,
    Datastore,
    Environment,
    ScriptRunConfig,
    RunConfiguration,
    Run
)
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import ClientSecretCredential,EnvironmentCredential
from pandas import read_csv
from azureml.core import Run, Dataset
from azure.storage.filedatalake import DataLakeServiceClient
from azure.storage.filedatalake import generate_file_sas
import joblib
import requests
import json


def upload_adls_dataset(TENANT_ID, CLIENT_ID, CLIENT_SECRET, dataset_name, dataset):
    TENANT_ID = ""
    # Your Service Principal App ID (Client ID)
    CLIENT_ID = ""
    ws = Workspace.from_config()  
    # Reading from keyvault    
    keyvault = ws.get_default_keyvault()    
    client_secret = keyvault.get_secret('')    
    CLIENT_SECRET = client_secret    
    try:
        credentials = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    except Exception as e:
        print(f"Error creating ClientSecretCredential: {e}")
        return None

    storage_account_name = ""
    service_client = DataLakeServiceClient(
        account_url="{}://{}.dfs.core.windows.net".format("https", storage_account_name),
        credential=credentials
    )

    # Save dataset to CSV
    dataset.to_csv(dataset_name, index=False)

    # Upload files to directory
    file_system_client = service_client.get_file_system_client(file_system="azureml")
    directory_client = file_system_client.get_directory_client(
        ""
    )

    for file_name in [dataset_name]:
        try:
            file_client = directory_client.create_file(file_name)
            with open(file_name, 'r') as local_file:
                file_contents = local_file.read()
                file_client.append_data(data=file_contents, offset=0, length=len(file_contents))
                file_client.flush_data(len(file_contents))
            print(f"Uploaded {file_name} to ADLS successfully.")
        except Exception as e:
            print(f"Error uploading {file_name} to ADLS: {e}")

def download_from_adls(TENANT_ID, CLIENT_ID, CLIENT_SECRET, storage_account_name, container, file_name):
    try:
        credentials = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    except Exception as e:
        print(f"Error creating ClientSecretCredential: {e}")
        return None

    storage_url = "{}://{}.dfs.core.windows.net".format("https", storage_account_name)
    try:
        blob_service_client_instance = BlobServiceClient(storage_url, credential=credentials)
        blob_client_instance = blob_service_client_instance.get_blob_client(container, file_name, snapshot=None)
        with open(file_name, "wb") as my_blob:
            blob_data = blob_client_instance.download_blob()
            blob_data.readinto(my_blob)
        print(f"Downloaded {file_name} from ADLS successfully.")
    except Exception as e:
        print(f"Error downloading {file_name} from ADLS: {e}")
        return None

    try:
        df = pd.read_csv(file_name)
        return df
    except Exception as e:
        print(f"Error reading {file_name} into DataFrame: {e}")
        return None

class Ingestion:
    def __init__(self):
        self.ingest=True
        
def main(start_date_str,end_date_str, frequency, client_id, client_secret, tenant_id):
    run = Run.get_context()
    ws = Workspace.from_config() 
    start_date=pd.to_datetime(start_date_str)
    end_date=pd.to_datetime(end_date_str)

    ingestion = Ingestion()

    
    ##Ingest Data Code below
    

def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_date_param', dest='start_date_param',type=str,
                        help='The start date of  data to ingest in YYYY-MM-DD format')
    parser.add_argument('--end_date_param', dest='end_date_param',type=str,
                        help='The end date of  data to ingest in YYYY-MM-DD format')
    parser.add_argument('--frequency_param',dest='frequency_param', type=str,
                        help='Frequency of dataset')
    parser.add_argument('--client_id', dest='client_id', type=str,help='Client ID for Azure AD')
    parser.add_argument('--client_secret', dest='client_secret', type=str,help='Client secret for Azure AD')
    parser.add_argument('--tenant_id', dest='tenant_id', type=str,help='Tenant ID for Azure AD')
    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == '__main__':
    args = parse_args()

    main(
        start_date_str=args.start_date_param,
        end_date_str=args.end_date_param,
        frequency=args.frequency_param,
        client_id=args.client_id,
        client_secret=args.client_secret,
        tenant_id=args.tenant_id
    )