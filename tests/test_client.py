"""Basic tests for GitHub Stats CLI."""

import pytest
from github_stats_cli.client import GitHubStatsClient


def test_client_initialization():
    """Test that client can be initialized."""
    client = GitHubStatsClient('octocat')
    assert client.username == 'octocat'
    assert client.BASE_URL == 'https://api.github.com'


def test_invalid_user():
    """Test that invalid username raises error."""
    client = GitHubStatsClient('this_user_definitely_does_not_exist_12345')
    with pytest.raises(ValueError, match="not found"):
        client.get_user_info()


# Note: More comprehensive tests would require mocking the API
# or using actual API calls (which would need network access)