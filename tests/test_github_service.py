from unittest.mock import Mock

from services.github_service import GitHubService


def test_get_repository_stats():
    service = GitHubService("https://api.github.com")
    service.api = Mock()
    service.api.get.return_value = {
        "full_name": "bpthoms/it401_project_template",
        "stargazers_count": 4,
        "language": "Python",
        "forks_count": 12,
    }

    stats = service.get_repository_stats(
        "repos/bpthoms/it401_project_template"
    )

    service.api.get.assert_called_once_with(
        "repos/bpthoms/it401_project_template"
    )
    assert stats == {
        "repo_name": "bpthoms/it401_project_template",
        "stars": 4,
        "language": "Python",
    }
