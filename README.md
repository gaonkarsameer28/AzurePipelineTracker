# AzurePipelineTracker
AzurePipelineTracker is a tool designed to fetch and integrate pipeline run and commit details from Azure DevOps. This code provides a comprehensive view of pipeline runs, associated commits, and their details, making it easier to track and manage your DevOps workflows.

## Features
Fetch pipeline run details from Azure DevOps.
Retrieve commit details associated with each pipeline run.
Integrate pull request details linked to commits.
Store the fetched data in a SQL Server database.
Easily extendable to support other database systems.
## Requirements
Python 3.x
requests library
pyodbc library
sqlalchemy library
Azure DevOps Personal Access Token (PAT)
SQL Server database
## Installation
Clone the repository:

### bash
Copy code
git clone https://github.com/yourusername/AzurePipelineTracker.git
cd AzurePipelineTracker
Install the required Python packages:

### bash
Copy code
pip install requests pyodbc sqlalchemy
Configuration
Set up your database:
Ensure you have a SQL Server database set up with the following table:

### sql
Copy code
USE [ReleaseLensDB]
GO

CREATE TABLE [dbo].[pipeline_runs](
    [id] [bigint] IDENTITY(1,1) NOT NULL,
    [timestamp] [datetime] NULL,
      NULL,
    [pipelinerunid] [int] NULL,
    [definitionid] [int] NULL,
    [definitionname] [nvarchar](200) NULL,
      NULL,
      NULL,
      NULL,
    [commitmessage] [nvarchar](500) NULL,
      NULL,
    [commitdate] [datetime] NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[pipeline_runs] ADD  CONSTRAINT [DF_pipeline_runs_timestamp]  DEFAULT (getdate()) FOR [timestamp]
GO
Set up your Azure DevOps Personal Access Token (PAT):

Generate a PAT from your Azure DevOps account.
Replace 'YOUR_PAT' in the code with your actual PAT.
Usage
Fetch and store pipeline run and commit details:

python
Copy code
from azure_devops_api import AzureDevOpsAPI
from db_factory import MSSQLDatabase

## Initialize the main.py

organization = ""
project = ""
#pipeline_id =
base_url = f"https://dev.azure.com/{organization}/{project}/_apis/"
pipelines_url = base_url + f"build/builds?definitions?api-version=6.0"
commits_url = base_url + f"build/changes?api-version=6.0"
personal_access_token = 'YOUR_PET'
### Use the base64 encoded PAT token . use base64tioken.py to generate the token. 

Run main.py & Query your SQL Server database to view the stored pipeline run and commit details.
