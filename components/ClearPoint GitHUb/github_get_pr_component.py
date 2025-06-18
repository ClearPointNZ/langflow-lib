from langflow.custom import Component
from langflow.io import Output, SecretStrInput, MessageTextInput
from langflow.schema import Data
from github import Github, Auth, PullRequest, File


class GitHubGetPrChangesComponent(Component):
    display_name = "Github Get PR Changes"
    description = (
        "Returns the title, description, file names and the diffs of a pull request from a GitHub repository."
    )
    icon = "github"
    name = "GitHubGetPrChangesComponent"

    inputs = [
        SecretStrInput(
            name="GITHUB_API_TOKEN",
            display_name="GitHub API Token",
            required=True,
        ),
        MessageTextInput(
            name="github_repo_name",
            display_name="GitHub Repository Name",
            info="The name of the GitHub repository to interact with in the form owner/repo.",
            tool_mode=True,
        ),
        MessageTextInput(
            name="pr_number",
            display_name="Pull Request Number",
            info="The number of the pull request to retrieve.",
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(
            name="pull_request", display_name="Pull Request", method="get_pull_request"
        )
    ]

    def get_pull_request(self) -> Data:
        auth = Auth.Token(self.GITHUB_API_TOKEN)
        github = Github(auth=auth)

        repo = github.get_repo(self.github_repo_name)
        # Get the pull request
        pr = repo.get_pull(int(self.pr_number))

        # Create a dictionary to hold the pull request details
        pr_dict = {}
        pr_dict["title"] = pr.title
        pr_dict["body"] = pr.body
        pr_dict["files"] = []
        for file in pr.get_files():
            file_dict = {"filename": file.filename, "patch": file.patch}
            pr_dict["files"].append(file_dict)

        data = Data(value=pr_dict)
        self.status = data
        return data
