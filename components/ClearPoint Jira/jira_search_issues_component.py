from langflow.custom import Component
from langflow.io import Output, SecretStrInput, MessageTextInput,StrInput,BoolInput
from jira import JIRA
from typing import List


class JiraSearchIssuesComponent(Component):
    display_name = "Jira Search Issues"
    description = (
        "Returns issues in Jira based on the provided JQL query."
    )
    icon = "jira"
    name = "JiraSearchIssuesComponent"

    inputs = [
         StrInput(
            name="JIRA_SERVER_URL",
            display_name="Jira Server URL",
            required=True,
        ),
        StrInput(
            name="JIRA_USERNAME",
            display_name="Jira Username",
            required=True,
        ),
        SecretStrInput(
            name="JIRA_API_KEY",
            display_name="Jira API Key",
            required=True,
        ),
        MessageTextInput(
            name="jql_query",
            display_name="JQL query ",
            info="The JQL query to use to search for issues in Jira.",
            tool_mode=True,
        ),
        MessageTextInput(
            name="issue_fields",
            display_name="Issue fields",
            info="A comma-seperated list of issues fields to return. If not provided, all fields will be returned.",
            tool_mode=True,
        ),
        BoolInput(
            name="flatten_fields",
            display_name="Flatten Fields",
            info="If true, the fields will be flattened as top level attributes.",
            value=True,
        )
    ]

    outputs = [
        Output(
            name="issues", display_name="List of Issues", method="search_issues"
        )
    ]

    def search_issues(self) -> List[Data]:
        jira = JIRA(server=self.JIRA_SERVER_URL, basic_auth=(self.JIRA_USERNAME, self.JIRA_API_KEY))

        
        issues = jira.search_issues(self.jql_query, fields=self.issue_fields,json_result=True)

        issues_list = []        
        for issue in issues["issues"]:

            if self.flatten_fields:
                # Flatten the fields to top level attributes, prefixed with "fields_"
                flattened_issue = {f"fields_{k}": v for k, v in issue["fields"].items()}                
                issue.update(flattened_issue)                
                del issue["fields"]

            issues_list.append(Data(data=issue))
        
        self.status = issues_list
        return issues_list
