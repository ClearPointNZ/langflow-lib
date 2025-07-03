from langflow.custom import Component
from langflow.io import Output, SecretStrInput, MessageTextInput,StrInput,MultilineInput
from atlassian import Confluence
from typing import List
from langflow.schema import Data, DataFrame


class ConfluenceUpdatePageComponent(Component):
    display_name = "Confluence Update Page"
    description = (
        "Updates the content of a Confluence page."
    )
    icon = "file-pen-line"
    name = "ConfluenceUpdatePageComponent"

    inputs = [
         StrInput(
            name="CONFLUENCE_SERVER_URL",
            display_name="Confluence Server URL",
            required=True,
        ),
        StrInput(
            name="CONFLUENCE_USERNAME",
            display_name="Confluence Username",
            required=True,
        ),
        SecretStrInput(
            name="CONFLUENCE_API_KEY",
            display_name="Confluence API Key",
            required=True,
        ),
        MessageTextInput(
            name="page_id",
            display_name="Page ID",
            info="The ID of the page to update in Confluence.",
            tool_mode=True,
        ),
        MultilineInput(
            name="content",
            display_name="Page Content",
            info="The content to update the Confluence page with. Content must be formatted using Confluence's storage format.",
            tool_mode=True,
        )
    ]

    outputs = [
        Output(
            name="results", 
            display_name="Results", 
            method="update_page",
            info="The results of the Confluence update page content operation."
        )
    ]

    def update_page(self) -> List[Data]:
        # HACK: make copy of inputs to avoid race condition. not guareenteed to work.  See https://github.com/langflow-ai/langflow/issues/8791
        page_id = self.page_id
        content = self.content
       
        # create the confluence client
        confluence = Confluence( url=self.CONFLUENCE_SERVER_URL,
                                username=self.CONFLUENCE_USERNAME,
                                password=self.CONFLUENCE_API_KEY)
        
        # page title is required for update so fetch current page title
        page = confluence.get_page_by_id(page_id=page_id)
        page_title= page['title']

        # Update the page
        updated_page = confluence.update_page(
            page_id=page_id,    
            title=page_title,
            body=content,
            representation='storage'
        )
        
        # build a results payload
        results = {"page_id": page_id, "status": "Content updated successfully"}
    
        self.status = results
        return Data(data=results)
