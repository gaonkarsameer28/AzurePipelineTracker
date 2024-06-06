import requests
from datetime import datetime
##from ..DbFactory.MsSqlServer import MSSQLDatabase
from  DbFactory.MsSqlServer import MSSQLDatabase
from ADOCommits import ADOCommits

# Azure DevOps API endpoints
organization = "scmdevops"
project = "leo.usermanagement.api"
#pipeline_id =5278
base_url = f"https://dev.azure.com/{organization}/{project}/_apis/"
pipelines_url = base_url + f"build/builds?definitions?api-version=6.0"

# Authentication
personal_access_token = 'OjZzaHkzcXJtMnQ3ZW9oZXJ6YzRrMmh1dGpoNTducms3dmNxYnJ4bWRzdGJqMmsyYm1iN2E='
headers = {
    'Authorization': 'Basic ' + personal_access_token,
    'Content-Type': 'application/json'
}

# Set date range (format: YYYY-MM-DD)
start_date = '2024-05-15'
end_date = '2024-05-21'

# Convert dates to UTC format
start_date_utc = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%dT00:00:00Z')
end_date_utc = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%dT23:59:59Z')

# Get pipeline runs with filtering directly in the URL
query_params = {    
    'minTime': start_date_utc,
    'maxTime': end_date_utc
}
# Get all pipelines within the project
#project = 'YOUR_PROJECT_NAME'
pipelines_response = requests.get(pipelines_url, headers=headers,params=query_params)
pipelines_data = pipelines_response.json()

# Iterate over each pipeline to retrieve pipeline runs and associated commits
for pipeline in pipelines_data['value']:
    pipeline_runid = pipeline['id']
    pipeline_definition_id = pipeline['definition']['id']    
    pipeline_project_name = pipeline['project']['name']
    pipeline_definition_name = pipeline['definition']['name']
    pipeline_buildNumber = pipeline['buildNumber']
    print(f"Pipeline: {pipeline_project_name} pipeline_definition_name:{pipeline_definition_name} pipeline_buildNumber: {pipeline_buildNumber}")
        
    # Get pipeline runs
    pipeline_runs_url = base_url + f"build/builds?definitions={pipeline_definition_id}&api-version=6.0"
    pipeline_runs_response = requests.get(pipeline_runs_url, headers=headers)
    pipeline_runs_data = pipeline_runs_response.json()
    
    # Extract pipeline runs within the specified date range
    pipelines_within_range = pipeline_runs_data
    #pipelines_within_range = []
    #for run in pipeline_runs_data['value']:
    #   run_start_time = datetime.strptime(run['startTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
    #  if start_date_utc <= run_start_time <= end_date_utc:
    #     pipelines_within_range.append(run)

    # Extract associated commits for pipeline runs within the date range
    ##for run in pipelines_within_range['value']:
        # Retrieve commits for each run        
        #commits_url = run['url'] + "/commits?api-version=6.0" 
    run_id = pipeline_runid
    commits_url = base_url + "build/changes?api-version=6.0"     
    commits_response = requests.get(commits_url, headers=headers,params={'fromBuildId': run_id, 'toBuildId': run_id,'continuationToken':None})
    commits_data = commits_response.json()
    azure_devops = ADOCommits(organization, project, headers)
    # Fetch all commits for the specified run ID
    commits_data = azure_devops.get_all_commits(run_id)   
        
        # Print pipeline run details
        #print("Pipeline Run ID:", run['id'])
        #print("Pipeline Run Start Time:", run['startTime'])
        #print("Pipeline Commits:")
    #for commit in commits_data['value']:
    for commit in commits_data:
            print("- Commit ID:", commit['id'])
            print("  Commit Message:", commit['message'])
            print("  Committer:", commit['author']['id'])
            print("  Commit Date:", commit['timestamp'])
            if 'pullRequestId' in commit:
             print("  pullRequest Date:", commit['pullRequestId'])    

            print("------------------------------------")
            parameters = {
                        'pipelinename': pipeline_definition_name,
                        'pipelinerunid': pipeline_runid,
                        'definitionid': pipeline_definition_id,
                        'definitionname': pipeline_definition_name,
                        'buildnumber': pipeline_buildNumber,
                        'projectname': pipeline_project_name,
                        'commitid': commit['id'],
                        'commitmessage': commit['message'],
                        'commitauthor': commit['author']['id'],
                        'commitdate': commit['timestamp']  # Use the appropriate date format
                    }
                #connection_string = 'mssql+pyodbc://sa:Password@123@localhost/ReleaseLensDB?driver=ODBC+Driver+17+for+SQL+Server'
            connection_string = f"DRIVER={{SQL Server Native Client 11.0}};SERVER={{localhost}};DATABASE={{ReleaseLensDB}};UID={{sa}};PWD={{Password@123}};Trusted_Connection=no;"

            database = MSSQLDatabase(connection_string)  
                # Execute a stored procedure with parameters
            database.execute_stored_procedure2('InsertPipelineRun', parameters)
            print("commit end")
    print ("pipeline run end")
print("*********pipeline loop******")
      
print("*********finished all******")