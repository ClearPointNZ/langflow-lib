from langflow.custom import Component
from langflow.io import Output, SecretStrInput, MessageTextInput,StrInput,BoolInput
from jira import JIRA
from typing import List
from langflow.schema import Data, DataFrame


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
            name="issues", 
            display_name="List of Issues", 
            method="search_issues",
            info="Matching issues as a list of Data objects."
        ),
        Output(
            display_name="DataFrame of Issues",
            name="dataframe",
            method="build_dataframe",
            info="Matching issues in DataFrame.",
        ),
    ]

    def search_issues(self) -> List[Data]:
        # HACK: make copy of inputs to avoid race condition. not guareenteed to work.  See https://github.com/langflow-ai/langflow/issues/8791
        jql_query = self.jql_query
        issue_fields = self.issue_fields

        # create the JIRA client
        jira = JIRA(server=self.JIRA_SERVER_URL, basic_auth=(self.JIRA_USERNAME, self.JIRA_API_KEY))

        # do the search
        issues = jira.search_issues(jql_query, fields=self.issue_fields,json_result=True)

        # build list of issues, flattening fields if requested
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
    
    def build_dataframe(self) -> DataFrame:
        # trigger the saerch
        issues = self.search_issues()

        # convert results to list of dict
        rows = []
        for issue in issues:
            rows.append(dict(issue.data))

        # convert list of dict to DataFrame
        df_result = DataFrame(rows)

        self.status = df_result  
        return df_result    
