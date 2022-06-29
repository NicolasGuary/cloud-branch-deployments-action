from github import Github
import os

SUCCESS_IMAGE_URL = (
    "https://github.com/dagster-io/cloud-branch-deployments-action/blob/main/assets/success.svg"
)
PENDING_IMAGE_URL = (
    "https://github.com/dagster-io/cloud-branch-deployments-action/blob/main/assets/pending.svg"
)
FAILED_IMAGE_URL = (
    "https://github.com/dagster-io/cloud-branch-deployments-action/blob/main/assets/failed.svg"
)


def main():
    g = Github(os.getenv("GITHUB_TOKEN"))
    pr_id = int(os.getenv("INPUT_PR"))
    repo_id = os.getenv("GITHUB_REPOSITORY")
    action = os.getenv("INPUT_ACTION")
    deployment_name = os.getenv("DEPLOYMENT_NAME")

    repo = g.get_repo(repo_id)
    pr = repo.get_pull(pr_id)

    comments = pr.get_issue_comments()
    comment_to_update = None
    for comment in comments:
        if comment.user.login == "github-actions[bot]" and "Dagster Cloud" in comment.body:
            comment_to_update = comment
            break

    deployment_url = f"https://7151-136-24-32-204.ngrok.io/1/{deployment_name}/"

    image_url = SUCCESS_IMAGE_URL if action == "completed" else PENDING_IMAGE_URL
    status_image = f'<img src="{image_url}" width=25 height=25/>'

    message = f"""
    Your pull request is automatically being deployed to Dagster Cloud.

    | Location      | Status          | Link              |
    | ------------- | --------------- | ----------------- |
    | `my_location` | {status_image}  | {deployment_url}  |
    """

    if comment_to_update:
        comment_to_update.edit(message)
    else:
        pr.create_issue_comment(message)


if __name__ == "__main__":
    main()
