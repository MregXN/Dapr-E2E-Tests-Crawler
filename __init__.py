from global_settings import *
from workflow_scan import WorkFlowScaner


if __name__ == "__main__":
    work_flow_scaner = WorkFlowScaner(REPO, WORKFLOW_NAME, ACCSS_TOKEM)
    print(
        f"Dapr E2E Tests Crawler start: \nScan repo is {REPO}  Worklow is {WORKFLOW_NAME}."
    )
    work_flow_scaner.scan_workflow()
    print(
        f"Pass rate of {WORKFLOW_NAME} is "
        + "{:.2%}".format(work_flow_scaner.get_pass_rate())
    )
    print("\n")
    print("Failure Workflow crawling start:")
    work_flow_scaner.list_failure_case()
