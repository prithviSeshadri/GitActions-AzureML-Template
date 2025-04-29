
# Sample Pipeline using GitHub Actions and AzureML

This repository contains a sample GitHub Actions workflow for running an Azure Machine Learning pipeline. The workflow is designed to automate tasks such as setting up compute resources, configuring AzureML, and executing pipelines.

## Workflow Trigger

The workflow is triggered manually using the `workflow_dispatch` event. It accepts the following inputs:

- **environment**: Specifies the target environment (e.g., DevInfraTest, DEV, Test, Prod).
- **start_date**: The start date for the pipeline in `mm/dd/yyyy` format.
- **end_date**: The end date for the pipeline in `mm/dd/yyyy` format.
- **frequency**: The frequency of the pipeline run (e.g., 1s, 10s, 1min, 10min, 1h).

## Jobs

### 1. Sample Pipeline Job

This job runs on `ubuntu-latest` and performs the following steps:

1. **Checkout Code**: Uses the `actions/checkout@v3` action to clone the repository.
2. **Set Up Python**: Installs Python 3.10 using `actions/setup-python@v4`.
3. **Install Dependencies**: Upgrades `pip` and installs the `azureml-sdk`.
4. **Add AzureML Config File**: Creates a `config.json` file with Azure subscription, resource group, and workspace details.
5. **Setup Compute**: Configures the compute instance for the pipeline. If the compute instance does not exist, it creates one. If it exists but is stopped, it starts the instance.
6. **Run AzureML Pipeline**: Executes the AzureML pipeline using the `setup_pipeline.py` script with the provided inputs.

## Environment Variables

The following environment variables are used in the workflow:

- `ENVN`: Specifies the environment (e.g., DEV, TST, PRD).
- `TASK`: Specifies the task type (e.g., training, batchinference).
- `COMPUTE_NAME`: Name of the compute cluster.
- `PIPELINE_NAME`: Name of the pipeline.
- `EXPERIMENT_NAME`: Name of the experiment for tracking pipeline runs.
- `WORKSPACE`: AzureML workspace name.
- `RESOURCE_GROUP`: Azure resource group name.

## Secrets

The workflow requires the following secrets to be configured in the repository:

- `AZURE_SUBSCRIPTION_ID`
- `AZURE_RESOURCE_GROUP`
- `AZURE_WORKSPACE_NAME`
- `CLIENT_ID`
- `CLIENT_SECRET`
- `TENANT_ID`

## Notes

- Ensure that the Azure CLI is installed and configured with the necessary extensions.
- Update the `setup_pipeline.py` script to match your pipeline requirements.
- Modify the compute configuration file path as needed for your environment.

For more details, refer to the [Azure Machine Learning documentation](https://learn.microsoft.com/en-us/azure/machine-learning/).

## Adding More Pipelines

To create or add more pipelines, follow these steps:

1. **Create a New Workflow File**: Add a new YAML file in the `.github/workflows` directory. For example, `new_pipeline.yml`.

2. **Define Workflow Triggers**: Specify the trigger for the new workflow. You can use `workflow_dispatch` for manual triggers, other events like `push` or `pull_request`, or even a cron-based schedule.

   - A cron job-based workflow example exists in the [CronJobs branch](https://github.com/sede-x/GOM_GIT_ACTIONS_TEMPLATE/tree/CronJobs) of the repository. This type of workflow runs at specific times defined by a cron expression. 
   - To set the cron expression, you can use tools like [Crontab Generator](https://crontab.cronhub.io/) to ensure the correct syntax. For example, `0 0 * * *` runs the workflow daily at midnight UTC.

3. **Set Up Jobs**: Define the jobs required for the new pipeline. You can reuse steps from the existing workflow, such as setting up Python, installing dependencies, and configuring AzureML.

4. **Customize Pipeline Logic**: Update the steps to include the specific logic for your new pipeline. For example, modify the script or parameters used to execute the pipeline.

5. **Add Required Secrets and Variables**: Ensure that any additional secrets or environment variables required for the new pipeline are added to the repository settings.

6. **Test the Workflow**: Trigger the workflow manually, through the defined event, or wait for the scheduled time (if using a cron job) to ensure it runs as expected.

7. **Document the Workflow**: Update the repository's README file to include details about the new pipeline, its purpose, and how to use it.

By following these steps, you can easily extend the repository to support multiple AzureML pipelines.

## Contributors

- Prithvi Seshadri - [prithvi.seshadri01@gmail.com](mailto:prithvi.seshadri01@gmail.com)

### How to Contribute?

Please reach out to [prithvi.seshadri01@gmail.com](mailto:prithvi.seshadri01@gmail.com) for further information on contributions.

