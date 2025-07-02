from langflow.custom import Component
from langflow.io import Output, SecretStrInput, MessageTextInput,StrInput,BoolInput
from atlassian import Confluence
from typing import List
from langflow.schema import Data, DataFrame


class ConfluenceSearchPagesComponent(Component):
    display_name = "Confluence Search Pages"
    description = (
        "Returns the matching pages in Confluence based on the provided CQL search query."
    )
    icon = "file-search"
    name = "ConfluenceSearchPagesComponent"

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
            name="cql_query",
            display_name="CQL query ",
            info="The CQL query to use to search for pages in Confluence.",
            tool_mode=True,
        ),
        MessageTextInput(
            name="expand_properties",
            display_name="Properties to Expand",
            info="A comma-separated list of properties to expand on in the search result.",
            tool_mode=True,
        )
    ]

    outputs = [
        Output(
            name="pages", 
            display_name="List of Pages", 
            method="search_pages",
            info="Matching pages as a list of Data objects."
        ),
        Output(
            display_name="DataFrame of Pages",
            name="dataframe",
            method="build_dataframe",
            info="Matching pages in a DataFrame.",
        ),
    ]

    def search_pages(self) -> List[Data]:
        # HACK: make copy of inputs to avoid race condition. not guareenteed to work.  See https://github.com/langflow-ai/langflow/issues/8791
        cql_query = self.cql_query
        expand_properties = self.expand_properties
        

        # create the confluence client
        confluence = Confluence( url=self.CONFLUENCE_SERVER_URL,
                                username=self.CONFLUENCE_USERNAME,
                                password=self.CONFLUENCE_API_KEY)
        
        if expand_properties.strip() == "":
            expand_properties = None
        else:
            # split the properties by comma and strip whitespace
            expand_properties_list = [prop.strip() for prop in expand_properties.split(",") if prop.strip()]    
        
        # see https://github.com/atlassian-api/atlassian-python-api/blob/705b26f8674334d663847774e21a38d718cf0dd3/atlassian/confluence/__init__.py#L2748
        response = confluence.cql(cql_query,expand=expand_properties)
        print(response)


        # build list of pages
        pages_list = []        
        for page in response["results"]:

            page_data = {
                "id": page["content"]["id"],
                "title": page["content"]["title"],
                "excerpt": page.get("excerpt", ""),
            }

            if expand_properties:
                for prop in expand_properties_list:
                    prop_nodes = prop.split(".")
                    # traverse the nested properties
                    value = page    
                    for node in prop_nodes:
                        if isinstance(value, dict) and node in value:
                            value = value[node]
                        else:
                            value = None
                            break

                    # if value is not None, add it to the page data
                    if value:
                        page_data[prop.replace(".","_")] = value   # can't have dots in key names, value get's lost in langflow

            pages_list.append(Data(data=page_data))
        
        self.status = pages_list
        return pages_list

        
    
    def build_dataframe(self) -> DataFrame:
        # trigger the saerch
        issues = self.search_pages()

        # convert results to list of dict
        rows = []
        for issue in issues:
            rows.append(dict(issue.data))

        # convert list of dict to DataFrame
        df_result = DataFrame(rows)

        self.status = df_result  
        return df_result 
