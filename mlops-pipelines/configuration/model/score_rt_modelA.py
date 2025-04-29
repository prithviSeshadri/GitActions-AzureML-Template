import os
import json
import numpy as np
import joblib
import pandas as pd
from lime.lime_tabular import LimeTabularExplainer
from azureml.contrib.services.aml_response import AMLResponse
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
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from azure.storage.filedatalake import DataLakeServiceClient
from azure.storage.filedatalake import generate_file_sas
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

# Global variable to hold the loaded model
model = None

# List of required feature columns for the input data
REQUIRED_COLUMNS = [
    'feature1',
    'feature2',
    'feature3',
    'feature4',
    'feature5',
    'feature6',
    'feature7',
    'feature8',
    'feature9',
    'feature10'
]  # Add all required feature columns here

def init():
    """
    Initialize the model by loading it from the specified path.
    This function is called once when the service starts.
    """
    global model
    # Construct the path to the model file using the environment variable
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'modelA.pkl')
    # Load the model using joblib
    model = joblib.load(model_path)

def run(data):
    """
    Run the scoring logic on the input data.
    This function is called for each request to the service.

    Args:
        data (str): JSON string containing the input data.

    Returns:
        str: JSON string containing the prediction results or an error message.
    """
    try:
        # Parse the input JSON data
        data = json.loads(data)
        data_list = data['data']
        # Convert the input data into a pandas DataFrame
        df = pd.DataFrame(data_list, columns=REQUIRED_COLUMNS)
        
        # Check if all required columns are present in the input data
        if not all(col in df.columns for col in REQUIRED_COLUMNS):
            raise ValueError("Input data is missing required columns.")
        
        # Extract the scaler and prediction model from the loaded model
        scaler = model[0][0]
        prediction_model = model[0][3]
        # Scale the input data using the scaler
        data_scaled = scaler.transform(df)
        # Perform predictions using the prediction model
        result = prediction_model.predict(data_scaled)
        
        # Return the prediction results as a JSON string
        return json.dumps(result.tolist())
    except Exception as e:
        # Handle any exceptions and return an error response
        error = str(e)
        return AMLResponse(error, 400)