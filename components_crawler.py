import base64
import yaml
import requests
from global_settings import GITHUB_API_PARAMETER



class ComponentsCrawler:
    def __init__(self, repo, access_token):
        self.repo = repo
        self.access_token = access_token
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"token {access_token}",
        }
        self.app_components_dict = {}
        

    def scan_components(self):
        print("\nStart to scan components.\n")
        url = f"https://api.github.com/repos/{self.repo}/contents/tests/config/"
        response = requests.get(url, headers=self.headers, params=GITHUB_API_PARAMETER)
        content = response.json()  
        for file in content:  
            print("loading " + file['name'] + "...")
            try:
                file_url = url + file['name']
                response = requests.get(file_url, headers=self.headers, params=GITHUB_API_PARAMETER)
                content = response.json()['content']   
                yaml_string = base64.b64decode(content).decode('utf-8')

                yaml_split_string = yaml_string.split("---")
                for s in yaml_split_string:
                    data = yaml.safe_load(s)
                    if data['kind'] != "Component":
                        continue

                    components_name = data['spec']['type']
                    for name in data['scopes']:
                        if name not in self.app_components_dict:
                            self.app_components_dict[name]=[]
                        self.app_components_dict[name].append(components_name)
            except:
                print("Fail to parse " + file['name'] + ", skip.")

        for key in self.app_components_dict:
            self.app_components_dict[key] = set(self.app_components_dict[key])       

