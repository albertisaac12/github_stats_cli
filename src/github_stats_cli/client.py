"""GitHub API client for fetching user and repository statistics."""

import requests
from collections import Counter
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class GitHubStatsClient:
    """Client for interacting with GitHub API."""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, username: str, token: Optional[str] = None):
        """
        Initialize the GitHub stats client.
        
        Args:
            username: GitHub username to fetch stats for
            token: Optional GitHub personal access token for higher rate limits
        """
        self.username = username
        self.headers = {'Accept': 'application/vnd.github.v3+json'}
        if token:
            self.headers['Authorization'] = f'token {token}'
    
    def _make_request(self, url: str, params: Optional[Dict] = None) -> requests.Response:
        """Make a request to the GitHub API with error handling."""
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise ValueError(f"User '{self.username}' not found")
            elif response.status_code == 403:
                raise ValueError("API rate limit exceeded. Use a GitHub token for higher limits.")
            else:
                raise ValueError(f"GitHub API error: {e}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Network error: {e}")
    
    def get_user_info(self) -> Dict:
        """Fetch basic user information."""
        url = f"{self.BASE_URL}/users/{self.username}"
        response = self._make_request(url)
        return response.json()
    
    def get_repos(self, include_forks: bool = False) -> List[Dict]:
        """
        Fetch all repositories for the user.
        
        Args:
            include_forks: Whether to include forked repositories
            
        Returns:
            List of repository dictionaries
        """
        url = f"{self.BASE_URL}/users/{self.username}/repos"
        repos = []
        page = 1
        
        while True:
            response = self._make_request(url, params={
                'page': page,
                'per_page': 100,
                'sort': 'updated',
                'direction': 'desc'
            })
            data = response.json()
            if not data:
                break
            
            if not include_forks:
                data = [repo for repo in data if not repo['fork']]
            
            repos.extend(data)
            page += 1
            
            # Break if we've fetched all repos
            if len(data) < 100:
                break
        
        return repos
    
    def get_language_stats(self, include_forks: bool = False) -> Dict[str, float]:
        """
        Calculate language statistics across all repositories.
        
        Args:
            include_forks: Whether to include forked repositories
            
        Returns:
            Dictionary mapping language names to percentage of total code
        """
        repos = self.get_repos(include_forks=include_forks)
        languages = Counter()
        
        for repo in repos:
            lang_url = repo['languages_url']
            response = self._make_request(lang_url)
            repo_languages = response.json()
            
            for lang, bytes_count in repo_languages.items():
                languages[lang] += bytes_count
        
        # Convert to percentages
        total = sum(languages.values())
        if total == 0:
            return {}
        
        return {lang: (count/total)*100 for lang, count in languages.most_common()}
    
    def get_repo_stats(self, include_forks: bool = False) -> Dict:
        """
        Get aggregate repository statistics.
        
        Args:
            include_forks: Whether to include forked repositories
            
        Returns:
            Dictionary with total stars, forks, watchers, etc.
        """
        repos = self.get_repos(include_forks=include_forks)
        
        total_stars = sum(repo['stargazers_count'] for repo in repos)
        total_forks = sum(repo['forks_count'] for repo in repos)
        total_watchers = sum(repo['watchers_count'] for repo in repos)
        total_size = sum(repo['size'] for repo in repos)
        
        return {
            'total_repos': len(repos),
            'total_stars': total_stars,
            'total_forks': total_forks,
            'total_watchers': total_watchers,
            'total_size_kb': total_size,
        }
    
    def get_top_repos(self, limit: int = 10, sort_by: str = 'stars', 
                     include_forks: bool = False) -> List[Dict]:
        """
        Get top repositories by a given metric.
        
        Args:
            limit: Number of repositories to return
            sort_by: Metric to sort by ('stars', 'forks', 'watchers', 'size')
            include_forks: Whether to include forked repositories
            
        Returns:
            List of top repositories
        """
        repos = self.get_repos(include_forks=include_forks)
        
        sort_keys = {
            'stars': 'stargazers_count',
            'forks': 'forks_count',
            'watchers': 'watchers_count',
            'size': 'size',
            'updated': 'updated_at'
        }
        
        sort_key = sort_keys.get(sort_by, 'stargazers_count')
        
        sorted_repos = sorted(
            repos,
            key=lambda x: x[sort_key] if sort_key != 'updated_at' else x[sort_key],
            reverse=True
        )
        
        return sorted_repos[:limit]
    
    def get_rate_limit(self) -> Tuple[int, int]:
        """
        Get current API rate limit status.
        
        Returns:
            Tuple of (remaining requests, total limit)
        """
        url = f"{self.BASE_URL}/rate_limit"
        response = self._make_request(url)
        data = response.json()
        
        remaining = data['rate']['remaining']
        limit = data['rate']['limit']
        
        return remaining, limit