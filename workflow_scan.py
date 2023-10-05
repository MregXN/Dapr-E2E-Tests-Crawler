import requests
import json
import sys
import zipfile
import re
from io import BytesIO
from global_settings import GITHUB_API_PARAMETER
from failure_log_crawler import FailureLogCrawler


class WorkFlowScaner:
    def __init__(self, repo, workflow_name, access_token):
        self.repo = repo
        self.workflow_name = workflow_name
        self.access_token = access_token
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"token {access_token}",
        }
        self.runs_len = 0
        self.in_progress_num = 0
        self.success_num = 0
        self.failure_num = 0
        self.failure_id = []
        self.crawler = FailureLogCrawler(repo, access_token)
        self.test_app_dict = {} 

    def scan_workflow(self):
        url = f"https://api.github.com/repos/{self.repo}/actions/workflows/{self.workflow_name}/runs"
        response = requests.get(url, headers=self.headers, params=GITHUB_API_PARAMETER)
        runs = json.loads(response.text)["workflow_runs"]

        # ingore workflows triggered manually
        scheduled_runs = [r for r in runs if r["event"] == "schedule"]
        self.runs_len = len(scheduled_runs)
        print(f"Successfully get {self.runs_len} scheduled runs")

        for run in scheduled_runs:
            if run["status"] == "in_progress":
                self.in_progress_num += 1
            else:
                if run["conclusion"] == "success":
                    self.success_num += 1
                    # get app names in first success workflow
                    if self.success_num == 1:
                        self.get_test_app_name(run["id"])
                elif run["conclusion"] == "failure":
                    self.failure_num += 1
                    self.failure_id.append(run["id"])

        print(
            f"{self.in_progress_num} runs are still in progress, {self.success_num} runs success and {self.failure_num} runs fail"
        )

    def get_pass_rate(self):
        pass_rate = self.success_num / self.runs_len
        return pass_rate

    def list_failure_case(self):
        self.crawler.crawl_failure_workflow(self.failure_id, self.runs_len)
        self.crawler.list_failure_testcase()

    def get_test_app_name(self, id):
        print(f"getting app names in workflow {id}")
        url = f"https://api.github.com/repos/{self.repo}/actions/runs/{id}/artifacts"
        response = requests.get(url, headers=self.headers)
        try:
            artifacts = response.json()["artifacts"]
        except:
            print("JSON decode error occured when get artifacts.")
        for artifact in artifacts:
            if artifact["name"] == "linux_amd64_e2e.json":
                url = artifact["archive_download_url"]
                artifact_name = artifact["name"]
                print("downloading artifact " + artifact_name)

                response = requests.get(url, headers=self.headers)
                try:
                    zip_file = zipfile.ZipFile(BytesIO(response.content))
                    extracted_file = zip_file.extract("test_report_e2e.json")
                except:
                    sys.stderr.write(
                        f"Error occurred when parse {artifact_name}, skiped"
                    )
                    return
                
                pattern_app_name = r'github.com/dapr/dapr/tests/e2e/(.*?)".*?e2e-(.*?):dapr'
                pattern_test_name = r'github.com/dapr/dapr/tests/e2e/(.*?)".*?=== RUN   (.*?)\\n"'
                with open(extracted_file, 'r') as f:  
                    content = f.read()
                    matches_app_name = re.findall(pattern_app_name,content)
                    matched_test_name = re.findall(pattern_test_name,content)
                
                app_dict = {}
                for m in matches_app_name:
                    if m[0] not in app_dict:
                        app_dict[m[0]]=[]
                    app_dict[m[0]].append(m[1])
                
                test_dict = {}
                for m in matched_test_name:
                    test_dict[m[1]]=m[0]

                for k,v in test_dict.items():
                    self.test_app_dict[k] = set(app_dict[v])  

                return self.test_app_dict