from langflow.custom import Component
from langflow.io import Output, SecretStrInput, MessageTextInput,StrInput,BoolInput,MultilineInput
from jira import JIRA
from typing import List
from langflow.schema import Data, DataFrame


class JiraAddLabelToIssueComponent(Component):
    display_name = "Jira Add label to issue"
    description = (
        "Adds a label to a Jira issue."
    )
    icon = "jira"
    name = "JiraAddLabelToIssueComponent"

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
            name="issue_key",
            display_name="Issue Key",
            info="The key of the issue to add the label to.",
            required=True,
            tool_mode=True,
        ),
        MessageTextInput(
            name="label",
            display_name="Label",
            info="The label to add to the issue.",
            required=True,
            tool_mode=True,
        ),    
    ]

    outputs = [
        Output(
            name="results", 
            display_name="Results", 
            method="add_label",
            info="The results of the Jira label add operation."
        )
    ]

    def add_label(self) -> Data:
        # HACK: make copy of inputs to avoid race condition. not guareenteed to work.  See https://github.com/langflow-ai/langflow/issues/8791
        issue_key = self.issue_key
        label = self.label

        # create the JIRA client
        jira = JIRA(server=self.JIRA_SERVER_URL, basic_auth=(self.JIRA_USERNAME, self.JIRA_API_KEY))

        # grab the current labels for the issue
        issue = jira.issue(issue_key, fields='labels')
        
        # add the label to the issue
        issue.fields.labels.append(label)

        # update issue with the new label
        issue.update(fields={"labels": issue.fields.labels})   

        # build a results payload
        results = {"issue_key": issue_key, "labels":  issue.fields.labels, "status": "Label added successfully"}
    
        self.status = results
        return Data(data=results)
    