import datetime
from github import Github
import os

# SUCCESS_IMAGE_URL = (
#     "https://github.com/dagster-io/cloud-branch-deployments-action/blob/main/assets/success.svg"
# )
# PENDING_IMAGE_URL = (
#     "https://github.com/dagster-io/cloud-branch-deployments-action/blob/main/assets/pending.svg"
# )
# FAILED_IMAGE_URL = (
#     "https://github.com/dagster-io/cloud-branch-deployments-action/blob/main/assets/failed.svg"
# )

SUCCESS_IMAGE_URL = "https://raw.githubusercontent.com/dagster-io/dagster/master/js_modules/dagit/packages/app/public/favicon-run-success.svg"
PENDING_IMAGE_URL = "https://raw.githubusercontent.com/dagster-io/dagster/master/js_modules/dagit/packages/app/public/favicon-run-pending.svg"
FAILED_IMAGE_URL = "https://raw.githubusercontent.com/dagster-io/dagster/master/js_modules/dagit/packages/app/public/favicon-run-failed.svg"


def main():
    g = Github(os.getenv("GITHUB_TOKEN"))
    pr_id = int(os.getenv("INPUT_PR"))
    repo_id = os.getenv("GITHUB_REPOSITORY")
    action = os.getenv("INPUT_ACTION")
    deployment_name = os.getenv("DEPLOYMENT_NAME")

    org_url = os.getenv("DAGSTER_CLOUD_URL")
    github_run_url = os.getenv("GITHUB_RUN_URL")

    location_name = os.getenv("LOCATION_NAME")

    repo = g.get_repo(repo_id)
    pr = repo.get_pull(pr_id)

    comments = pr.get_issue_comments()
    comment_to_update = None
    for comment in comments:
        if (
            comment.user.login == "github-actions[bot]"
            and "Dagster Cloud" in comment.body
            and f"`{location_name}`" in comment.body
        ):
            comment_to_update = comment
            break

    deployment_url = f"{org_url}/{deployment_name}/"

    link = f"[View in Cloud]({deployment_url})" if action != "pending" else "Building..."

    image_url = (
        SUCCESS_IMAGE_URL
        if action == "complete"
        else (FAILED_IMAGE_URL if action == "failed" else PENDING_IMAGE_URL)
    )
    status_image = f'[<img src="{image_url}" width=25 height=25/>]({github_run_url})'

    time_str = datetime.datetime.now(datetime.timezone.utc).strftime("%b %d, %Y at %I:%M %p (%Z)")

    message = f"""
Your pull request is automatically being deployed to Dagster Cloud.

| Location          | Status          | Link    | Updated         |
| ----------------- | --------------- | ------- | --------------- | 
| `{location_name}` | {status_image}  | {link}  | {time_str}      |
    """

    if comment_to_update:
        comment_to_update.edit(message)
    else:
        pr.create_issue_comment(message)


if __name__ == "__main__":
    main()
