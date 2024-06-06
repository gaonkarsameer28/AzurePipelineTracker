from DbFactory.MsSqlServer import MSSQLDatabase
from ADOCommits import ADOCommits
from ADOPipelines import ADOPipelines

# Azure DevOps API endpoints
organization = "YOUR_ORG"
project = "YOUR_PROJECT"
#pipeline_id =
base_url = f"https://dev.azure.com/{organization}/{project}/_apis/"
pipelines_url = base_url + f"build/builds?definitions?api-version=6.0"
commits_url = base_url + f"build/changes?api-version=6.0"
# Authentication
# original pat token will not work 
# Use the base64 encoded PAT token . use base64tioken.py to generate the token.
# do not store the PAT in the code. use environment variable or vault to store the token.
personal_access_token = 'YOUR_PET'
headers = {
    'Authorization': 'Basic ' + personal_access_token,
    'Content-Type': 'application/json'
}
#backend connection in this case its sql
Sqlconnection_string = f"YOUR_CONNECTION_STRING;"

# Set date range to scan build piplines (format: YYYY-MM-DD)
start_date = 'YOUR_STARTDATE'
end_date = 'YOUR_ENDDATE'

ADO_Pipelines = ADOPipelines(pipelines_url,headers)
pipeline_data = ADO_Pipelines.get_all_PipelinesRuns(start_date,end_date)

for pipeline in pipeline_data:
    pipeline_runid = pipeline['id']
    pipeline_definition_id = pipeline['definition']['id']    
    pipeline_project_name = pipeline['project']['name']
    pipeline_definition_name = pipeline['definition']['name']
    pipeline_buildNumber = pipeline['buildNumber']
    #print(f"Pipeline: {pipeline_project_name} pipeline_definition_name:{pipeline_definition_name} pipeline_buildNumber: {pipeline_buildNumber}")

    ADO_Commits = ADOCommits(commits_url, headers)
        # Fetch all commits for the specified run ID
    commits_data = ADO_Commits.get_all_commits(pipeline_runid)  
    for commit in commits_data:
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

        connection_string = Sqlconnection_string

        database = MSSQLDatabase(connection_string)  
                # Execute a stored procedure with parameters
        database.execute_stored_procedure2('InsertPipelineRun', parameters)        
    #print("commit end")    
#print ("pipeline run end") 


print("*********finished all******")
