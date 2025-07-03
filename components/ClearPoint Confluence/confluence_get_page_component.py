from langflow.custom import Component
from langflow.io import Output, SecretStrInput, MessageTextInput,StrInput,BoolInput
from atlassian import Confluence
from typing import List
from langflow.schema import Data, DataFrame


class ConfluenceGetPageComponent(Component):
    display_name = "Confluence Get Page"
    description = (
        "Fetches the content of a Confluence page by its page ID."
    )
    icon = "file"
    name = "ConfluenceGetPageComponent"

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
            info="The ID of the page to fetch from Confluence.",
            tool_mode=True,
        )
    ]

    outputs = [
        Output(
            name="page_content", 
            display_name="Page", 
            method="get_page",
            info="The page content as a Data object."
        )        
    ]

    def get_page(self) -> List[Data]:
        # HACK: make copy of inputs to avoid race condition. not guareenteed to work.  See https://github.com/langflow-ai/langflow/issues/8791
        page_id = self.page_id
       
        # create the confluence client
        confluence = Confluence( url=self.CONFLUENCE_SERVER_URL,
                                username=self.CONFLUENCE_USERNAME,
                                password=self.CONFLUENCE_API_KEY)
        
        # Get the page by ID and expand the body and children
        page = confluence.get_page_by_id(page_id=page_id, expand='body.storage')

        page_content = {
            'id': page['id'],
            'title': page['title'],
            'content': page['body']['storage']['value'],
        }
        
        self.status = page_content
        return Data(data=page_content)
