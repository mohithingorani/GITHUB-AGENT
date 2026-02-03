import requests
import os
from dotenv import load_dotenv
import pprint
from langchain.tools import tool

load_dotenv()

GITHUB_API = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
    "Accept": "application/vnd.github+json"
}


def summarize(data):
    # Simple summary function
    if "error" in data:
        return f"Error fetching data for user {data['username']}: {data['error']}"
    
    summary = f"GitHub User: {data['username']}\n"
    summary += f"Total Public Repositories: {data['repo_count']}\n"
    language_count = {}
    for repo in data['repos']:
        lang = repo['language']
        if lang:
            language_count[lang] = language_count.get(lang, 0) + 1
    
    summary += "Languages Used:\n"
    for lang, count in language_count.items():
        summary += f"- {lang}: {count} repositories\n"
    
    return summary

# summarize function with dict response
def summarize_dict(data):
    if "error" in data:
        return {
            "error": data["error"],
            "username": data["username"]
        }
    
    language_count = {}
    for repo in data['repos']:
        lang = repo['language']
        if lang:
            language_count[lang] = language_count.get(lang, 0) + 1
    
    summary = {
        "username": data['username'],
        "repo_count": data['repo_count'],
        "languages_used": language_count
    }
    
    return summary

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

    data = {
        "username": username,
        "repo_count": len(cleaned_repos),
        "repos": cleaned_repos
    }
    summary = summarize_dict(data)
    return summary


data = fetch_github_profile("mohithingorani")
print(data)
# # Pretty print the fetched data
# pprint.pprint(data)
