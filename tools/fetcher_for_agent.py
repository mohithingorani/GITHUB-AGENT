import requests
import os
from dotenv import load_dotenv
from langchain.tools import tool
load_dotenv()

GITHUB_API = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
    "Accept": "application/vnd.github+json"
}

# Added pagination to fetch all repositories
@tool
def fetch_github_profile(username: str,) -> dict:
    """
    Fetch public GitHub repositories and README content.
    """
    empty = False
   
    page = 1
    cleaned_repos = []
    while not empty:
        repos_url = f"{GITHUB_API}/users/{username}/repos?per_page=100&page={page}"
        repos_response = requests.get(repos_url, headers=HEADERS)
        repos_data = repos_response.json()

        if repos_response.status_code == 404:
            return {
                "error": "user_not_found",
                "username": username
            }

        if repos_response.status_code == 403:
            return {
                "error": "rate_limited",
                "username": username
            }

        if repos_response.status_code != 200:
            return {
                "error": "unknown_error",
                "status_code": repos_response.status_code,
                "username": username
            }

        
        if len(repos_response.json()) == 0:
            empty = True
            break
        for repo in repos_data:
 
            cleaned_repos.append({
                "name": repo["name"],
                "description": repo["description"],
                "stars": repo["stargazers_count"],
                "language": repo["language"],
                "updated_at": repo["updated_at"],
                # "readme": readme_text
            })
        page += 1

    return {
        "username": username,
        "repo_count": len(cleaned_repos),
        "repos": cleaned_repos
    }


# data = fetch_github_profile("mohithingorani")

# # Pretty print the fetched data
# pprint.pprint(data)
