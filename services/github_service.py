from functools import lru_cache

from services.api_service import ApiService


class GitHubService:
    """Retrieves and normalizes repository data from the GitHub API."""

    def __init__(self, base_url, timeout=6):
        self.api = ApiService(base_url, timeout=timeout)

    def get_repository_stats(self, repository_path):
        data = self.api.get(repository_path)
        return {
            "repo_name": data.get("full_name"),
            "stars": data.get("stargazers_count"),
            "language": data.get("language"),
        }


@lru_cache(maxsize=8)
def fetch_github_stats(base_url, repository_path):
    """Return cached statistics for a GitHub repository API path."""
    service = GitHubService(base_url)
    return service.get_repository_stats(repository_path)
