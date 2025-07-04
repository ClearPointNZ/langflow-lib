from langflow.custom import Component
from langflow.io import Output, SecretStrInput, MessageTextInput,StrInput,BoolInput,MultilineInput
from jira import JIRA
from typing import List
from langflow.schema import Data, DataFrame


class JiraAddCommentComponent(Component):
    display_name = "Jira Add comment"
    description = (
        "Adds a comment to a Jira issue."
    )
    icon = "jira"
    name = "JiraAddCommentComponent"

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
            info="The key of the issue to update.",
            required=True,
            tool_mode=True,
        ),
        MultilineInput(name="comment_text", 
                       display_name="Comment Text",
                       info="Text of the comment to add to the issue.",
                       required=True,
                       tool_mode=True),       
    ]

    outputs = [
        Output(
            name="results", 
            display_name="Results", 
            method="add_comment_to_issue",
            info="The results of the Jira comment add operation."
        )
    ]

    def add_comment_to_issue(self) -> Data:
        # HACK: make copy of inputs to avoid race condition. not guareenteed to work.  See https://github.com/langflow-ai/langflow/issues/8791
        issue_key = self.issue_key
        comment_text = self.comment_text

        # create the JIRA client
        jira = JIRA(server=self.JIRA_SERVER_URL, basic_auth=(self.JIRA_USERNAME, self.JIRA_API_KEY))
        
        # add the comment to the issue
        response = jira.add_comment(issue_key, comment_text)                                   

        # build a results payload
        results = {"comment_id": response["id"], "status": "Comment added successfully"}
    
        self.status = results.results
        return Data(data=results.results)
    