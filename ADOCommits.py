import requests

class ADOCommits:
    def __init__(self, commits_url, Authheaders):        
        self.commits_url = commits_url
        self.headers = Authheaders

    def get_all_commits(self, run_id):
        commits = []
        continuation_token = None
        commits_url = self.commits_url

        while True:
            params = {                
                'fromBuildId': run_id,
                'toBuildId': run_id,
                '$top': 1000 
            }
            if continuation_token:
                params['continuationToken'] = continuation_token

            response = requests.get(commits_url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            commits.extend(data['value'])

            # Fetch the continuation token from response headers
            continuation_token = response.headers.get('x-ms-continuationtoken')
            if not continuation_token:
                break

        return commits

    def get_pull_request_details(self, pull_request_id):
        pull_request_url = f"{self.base_url}git/pullrequests/{pull_request_id}?api-version=6.0"
        response = requests.get(pull_request_url, headers=self.headers)
        response.raise_for_status()
        return response.json()
