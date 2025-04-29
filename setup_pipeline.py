import argparse
from azureml.core import Workspace, Experiment, Environment
from azureml.pipeline.core import Pipeline
from azureml.pipeline.steps import PythonScriptStep
from azureml.core.runconfig import RunConfiguration
import os

parser = argparse.ArgumentParser(description="Run AzureML Pipeline")
parser.add_argument("--compute-instance", required=True, help="Compute Instance name")
parser.add_argument('--start_date_param', dest='start_date_param',type=str,
                        help='The start date of data to ingest in YYYY-MM-DD format')
parser.add_argument('--end_date_param', dest='end_date_param',type=str,
                        help='The end date of  data to ingest in YYYY-MM-DD format')
parser.add_argument('--frequency_param',dest='frequency_param', type=str,
                    help='Frequency of dataset')
parser.add_argument('--client_id', dest='client_id', type=str,help='Client ID for Azure AD')
parser.add_argument('--client_secret', dest='client_secret', type=str,help='Client secret for Azure AD')
parser.add_argument('--tenant_id', dest='tenant_id', type=str,help='Tenant ID for Azure AD')
args_parsed = parser.parse_args()

ws = Workspace.from_config()
env = Environment.from_conda_specification(name='sample_env', file_path='./src/sample_env.yml')

# Define a run configuration
run_config = RunConfiguration()
run_config.environment = env

data_ingest_step = PythonScriptStep(
    name="Data Ingestion",
    script_name="data_ingestion.py",
    arguments=[
        "--end_date_param", args_parsed.end_date_param,
        "--frequency_param", args_parsed.frequency_param,
        "--client_id", args_parsed.client_id,
        "--client_secret", args_parsed.client_secret,
        "--tenant_id", args_parsed.tenant_id
    ],
    compute_target=args_parsed.compute_instance,
    source_directory="src",
    runconfig=run_config
)

pipeline = Pipeline(workspace=ws, steps=[data_ingest_step])

experiment = Experiment(workspace=ws, name="dataingestion")
pipeline_run = experiment.submit(pipeline)
print("Pipeline submitted. Run ID:", pipeline_run.id)
