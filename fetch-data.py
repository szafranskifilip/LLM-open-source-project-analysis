import requests

# GitHub API endpoint for repository search
search_url = "https://api.github.com/search/repositories"

# Search parameters
query = "stars:>=500"  # Repositories with at least 500 stars
sort = "stars"  # Sort by the number of stars in descending order
order = "desc"
per_page = 100  # Number of results per page

# GitHub API token (optional, but recommended to avoid rate limiting)
headers = {
    "Authorization": "Bearer YOUR_GITHUB_ACCESS_TOKEN"
}

# Send a GET request to the GitHub API
response = requests.get(search_url, params={"q": query, "sort": sort, "order": order, "per_page": per_page}, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Extract the JSON data from the response
    data = response.json()

    # Get the total count of repositories matching the search criteria
    total_count = data["total_count"]
    print(f"Total repositories found: {total_count}")

    # Iterate over the repositories
    for repo in data["items"]:
        name = repo["full_name"]
        stars = repo["stargazers_count"]
        url = repo["html_url"]
        print(f"Repository: {name}")
        print(f"Stars: {stars}")
        print(f"URL: {url}")
        print("---")
else:
    print("Failed to retrieve data from the GitHub API.")
