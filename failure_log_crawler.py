import requests
import json
import xml.etree.ElementTree as ET
import zipfile
from io import BytesIO


class TestCaseInfo:
    fail_times = 1
    os = ""
    name = ""
    fail_rate = 0
    latest_url = ""

    def __init__(self, name, os, latest_url):
        self.name = name
        self.os = os
        self.latest_url = latest_url

    # linux or windows or both
    def update_os(self, os):
        if self.os != os:
            self.os = "linux/windows"

    def increase_fail_times(self):
        self.fail_times += 1

    # to do
    def get_fail_rate(self, workflow_len):
        self.fail_rate = self.fail_times / workflow_len
        return self.fail_rate

    def to_json(self):
        return json.dumps(self)


class FailureLogCrawler:
    headres = {}
    fail_testcase_dict = {}
    fail_testcase_dict_sorted_list = []

    def __init__(self, repo, access_token):
        self.repo = repo
        self.access_token = access_token
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"token {access_token}",
        }

    def crawl(self, failure_id, workflow_len):
        failure_id_len = len(failure_id)
        for index, id in enumerate(failure_id):
            print(
                f"({index+1}/{failure_id_len}) crawling failure workflow... workflow id is "
                + str(id)
            )
            url = (
                f"https://api.github.com/repos/{self.repo}/actions/runs/{id}/artifacts"
            )
            response = requests.get(url, headers=self.headers)
            artifacts = response.json()["artifacts"]
            for artifact in artifacts:
                # todo： function
                if (
                    artifact["name"] == "linux_amd64_e2e.json"
                    or artifact["name"] == "windows_amd64_e2e.json"
                ):
                    self.parse_artifact(artifact, id)

        for v in self.fail_testcase_dict.values():
            v.get_fail_rate(workflow_len)
        self.fail_testcase_dict_sorted_list = sorted(
            self.fail_testcase_dict.values(),
            key=lambda case: case.fail_rate,
            reverse=True
        )

    def parse_artifact(self, artifact, id):
        url = artifact["archive_download_url"]
        print("downloading artifact " + artifact["name"])
        response = requests.get(url, headers=self.headers)
        zip_file = zipfile.ZipFile(BytesIO(response.content))
        extracted_file = zip_file.extract("test_report_e2e.xml")
        tree = ET.parse(extracted_file)

        root = tree.getroot()
        for testsuite in root:
            failures = int(testsuite.attrib["failures"])
            if failures:
                fail_testcases = testsuite.findall("testcase")
                for fail_testcase in fail_testcases[:failures]:
                    os = artifact["name"].split("_")[0]
                    name = fail_testcase.attrib["name"]
                    if name in self.fail_testcase_dict:
                        self.fail_testcase_dict[name].update_os(os)
                        self.fail_testcase_dict[name].increase_fail_times()
                    else:
                        latest_url = f"https://github.com/{self.repo}/actions/runs/{id}"
                        testcase_info = TestCaseInfo(name, os, latest_url)
                        self.fail_testcase_dict[name] = testcase_info

    def list_failure_testcase(self):
        print("\n")
        print("Failed Test Cases:")
        for case in self.fail_testcase_dict_sorted_list:
            print(
                "Fail Rate: "
                + "{:.2%}".format(float(case.fail_rate))
                + "     "
                + "Test Case: "
                + str(case.name)
                + "\n"
                + "Operating System: "
                + str(case.os)
                + "     "
                + "Latest URL: "
                + str(case.latest_url)
                + "\n"
            )
