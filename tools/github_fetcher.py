import requests
import os
from dotenv import load_dotenv
import pprint

load_dotenv()

GITHUB_API = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
    "Accept": "application/vnd.github+json"
}


def fetch_github_profile(username: str) -> dict:
    """
    Fetch public GitHub repositories and README content.
    """

    repos_url = f"{GITHUB_API}/users/{username}/repos"
    repos_response = requests.get(repos_url, headers=HEADERS)

    if repos_response.status_code != 200:
        raise Exception("Failed to fetch repositories")

    repos_data = repos_response.json()
    cleaned_repos = []

    for repo in repos_data:
        if repo["fork"]:
            continue  # ignore forks

        readme_text = ""

        readme_url = f"{GITHUB_API}/repos/{username}/{repo['name']}/readme"
        readme_response = requests.get(readme_url, headers=HEADERS)

        if readme_response.status_code == 200:
            readme_text = readme_response.json().get("content", "")

        cleaned_repos.append({
            "name": repo["name"],
            "description": repo["description"],
            "stars": repo["stargazers_count"],
            "language": repo["language"],
            "updated_at": repo["updated_at"],
            # "readme": readme_text
        })

    return {
        "username": username,
        "repo_count": len(cleaned_repos),
        "repos": cleaned_repos
    }


data = fetch_github_profile("mohithingorani")

# Pretty print the fetched data
pprint.pprint(data)
