import requests
from datetime import datetime

class ADOPipelines:
    def __init__(self, pipelines_url, Authheaders):        
        self.headers = Authheaders
        self.pipelines_url = pipelines_url

    def get_all_PipelinesRuns(self, start_date,end_date):
        Pipelines = []
       
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
        pipelines_response = requests.get(self.pipelines_url, headers=self.headers,params=query_params)
        response = pipelines_response.json()
        #data = response.json()
        Pipelines.extend(response['value'])
        return Pipelines

   
