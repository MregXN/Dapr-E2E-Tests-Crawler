# Dapr E2E Tests Crawler
This is a Python script that scrapes the Dapr E2E tests results in Github Action scheduled workflow.



## Usage
**1. Clone the repository:**

```shell
git clone https://github.com/username/dapr-e2e-test-scraper.git 
```

**2. Replace values in global_settings.py** 
```python
# Follow the style of "<OWNER>/<REPO>"
REPO = "MregXN/dapr"

# yml file name of github action workflow"
WORKFLOW_NAME = "dapr-test.yml"

# Github access token. Must cover the scope of dapr repo"
ACCSS_TOKEM = "<REPLACE_WITH_YOUR_TOKEN>"

# Parameters brought when accessing github API
GITHUB_API_PARAMETER = {"per_page": "100"}
```

**3. Run the script:**
```shell
python3 __init__.py 
```

## Result
This script will generate results in console as follow:
```
Dapr E2E Tests Crawler start: 
Scan repo is MregXN/dapr  Worklow is dapr-test.yml.
Successfully get 100 scheduled runs
1 runs are still in progress, 5 runs success and 94 runs fail
Pass rate of dapr-test.yml is 5.00%


Failure Workflow crawling start:
(1/94) crawling failure workflow... workflow id is 5746433829
(2/94) crawling failure workflow... workflow id is 5746412351
(3/94) crawling failure workflow... workflow id is 5746387663
(4/94) crawling failure workflow... workflow id is 5746362541
(5/94) crawling failure workflow... workflow id is 5746339359
(6/94) crawling failure workflow... workflow id is 5746307186
...

Failed Test Cases:
Fail Rate: 38.00%     Test Case: TestActorMetadataEtagRace/Triggers_rebalance_of_reminders_multiple_times_to_validate_eTag_race_on_metadata_record.
Operating System: linux/windows     Latest URL: https://github.com/MregXN/dapr/actions/runs/5746253044

Fail Rate: 38.00%     Test Case: TestActorMetadataEtagRace
Operating System: linux/windows     Latest URL: https://github.com/MregXN/dapr/actions/runs/5746253044

Fail Rate: 25.00%     Test Case: TestServiceInvocationExternally/serviceinvocation-callee-external/Test_HTTP_to_HTTPS_Externally_using_HTTP_Endpoint_CRD
Operating System: windows     Latest URL: https://github.com/MregXN/dapr/actions/runs/5746307186

Fail Rate: 25.00%     Test Case: TestServiceInvocationExternally/serviceinvocation-callee-external
Operating System: windows     Latest URL: https://github.com/MregXN/dapr/actions/runs/5746307186

Fail Rate: 25.00%     Test Case: TestServiceInvocationExternally
Operating System: windows     Latest URL: https://github.com/MregXN/dapr/actions/runs/5746307186

Fail Rate: 21.00%     Test Case: TestActorReminder
Operating System: linux/windows     Latest URL: https://github.com/MregXN/dapr/actions/runs/5746279502

Fail Rate: 18.00%     Test Case: TestActorReminder/Actor_reminder_unregister_then_restart_should_not_trigger_anymore.
Operating System: linux/windows     Latest URL: https://github.com/MregXN/dapr/actions/runs/5746279502

Fail Rate: 6.00%     Test Case: TestActorFeatures
Operating System: windows     Latest URL: https://github.com/MregXN/dapr/actions/runs/5740828818
...
``` 

## License
 
This project is licensed under the [MIT License](http://opensource.org/licenses/MIT).