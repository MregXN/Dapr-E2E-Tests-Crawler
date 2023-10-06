from global_settings import REPO, WORKFLOW_NAME, ACCESS_TOKEN
from workflow_scan import WorkFlowScaner
from components_crawler import ComponentsCrawler

if __name__ == "__main__":
    print(
        f"Dapr E2E Tests Crawler start. \nREPO : {REPO}  WORKFLOW_NAME : {WORKFLOW_NAME}"
    )
    components_crawler = ComponentsCrawler(REPO,ACCESS_TOKEN)
    workflow_scaner = WorkFlowScaner(REPO, WORKFLOW_NAME, ACCESS_TOKEN)

    workflow_scaner.scan_workflow(components_crawler.scan_components())
    print("\nFailure Workflow crawling start:")
    workflow_scaner.list_failure_case()
    