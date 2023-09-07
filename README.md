# Dapr E2E Tests Crawler
This is a Python script scrapes the Dapr E2E tests results. It use Github API to retrieve the relevant Github Action scheduled workflow, download the log generated by each execution and tally the number of failed test cases.

This crawler is able to calculate the following characteristics:
- Conclusions and pass rate of recent E2E tests workflows
- List of Failed test case
- Failure rate of each failed test case and its latest workflow URL
  
By utilizing this script, identifying flaky tests becomes a simpler task. It can be used after making repairs to the test environment to gauge the extent of improvement brought about by the modifications.

## Usage
**1. Clone the repository:**

```shell
git clone https://github.com/username/dapr-e2e-test-scraper.git 
```

**2. Replace values in global_settings.py** 
```python
# Follow the style of "<OWNER>/<REPO>"
REPO = "dapr/dapr"

# yml file name of github action workflow"
WORKFLOW_NAME = "dapr-test.yml"

# Github access token. Must cover the scope of dapr repo"
# Replace it when running locally
ACCSS_TOKEM = os.getenv("GITHUB_TOKEN")

# Parameters brought when accessing github API
GITHUB_API_PARAMETER = {"per_page": "100"}

# Target to output logs
OUTPUT_TARGET = "log.txt"
```

**3. Install dependencies:**
```shell
pip install -r requirements.pip
```

**4. Run the script:**
```shell
python3 __init__.py 
```

## Result
This script will generate results in log.txt:
```

Pass rate of dapr-test.yml is 5.00%


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