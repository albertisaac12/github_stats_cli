"""Command-line interface for GitHub Stats CLI."""

import click
import os
from .client import GitHubStatsClient
from .display import (
    display_user_info,
    display_language_stats,
    display_repo_stats,
    display_top_repos,
    display_rate_limit,
    display_error,
    display_success,
    display_info,
    console
)


@click.group()
@click.version_option(version='0.1.0')
def main():
    """
    GitHub Stats CLI - Fetch and display GitHub user and repository statistics.
    
    Set GITHUB_TOKEN environment variable for higher API rate limits.
    """
    pass


@main.command()
@click.argument('username')
@click.option('--token', '-t', envvar='GITHUB_TOKEN', help='GitHub personal access token')
def user(username, token):
    """Display user profile information."""
    try:
        client = GitHubStatsClient(username, token)
        user_data = client.get_user_info()
        display_user_info(user_data)
        
        # Show rate limit
        remaining, limit = client.get_rate_limit()
        display_rate_limit(remaining, limit)
        
    except ValueError as e:
        display_error(str(e))
        raise click.Abort()


@main.command()
@click.argument('username')
@click.option('--token', '-t', envvar='GITHUB_TOKEN', help='GitHub personal access token')
@click.option('--limit', '-l', default=10, help='Number of languages to display (default: 10)')
@click.option('--forks/--no-forks', default=False, help='Include forked repositories')
def languages(username, token, limit, forks):
    """Display programming language statistics."""
    try:
        with console.status(f"[bold green]Fetching language stats for {username}...", spinner="dots"):
            client = GitHubStatsClient(username, token)
            lang_stats = client.get_language_stats(include_forks=forks)
        
        if not lang_stats:
            display_info("No language data found for this user")
            return
        
        display_language_stats(lang_stats, limit=limit)
        
        # Show rate limit
        remaining, limit_total = client.get_rate_limit()
        display_rate_limit(remaining, limit_total)
        
    except ValueError as e:
        display_error(str(e))
        raise click.Abort()


@main.command()
@click.argument('username')
@click.option('--token', '-t', envvar='GITHUB_TOKEN', help='GitHub personal access token')
@click.option('--forks/--no-forks', default=False, help='Include forked repositories')
def repos(username, token, forks):
    """Display repository statistics summary."""
    try:
        with console.status(f"[bold green]Fetching repository stats for {username}...", spinner="dots"):
            client = GitHubStatsClient(username, token)
            repo_stats = client.get_repo_stats(include_forks=forks)
        
        display_repo_stats(repo_stats)
        
        # Show rate limit
        remaining, limit = client.get_rate_limit()
        display_rate_limit(remaining, limit)
        
    except ValueError as e:
        display_error(str(e))
        raise click.Abort()


@main.command()
@click.argument('username')
@click.option('--token', '-t', envvar='GITHUB_TOKEN', help='GitHub personal access token')
@click.option('--limit', '-l', default=10, help='Number of repositories to display (default: 10)')
@click.option('--sort', '-s', 
              type=click.Choice(['stars', 'forks', 'watchers', 'size', 'updated']),
              default='stars',
              help='Sort repositories by metric (default: stars)')
@click.option('--forks/--no-forks', default=False, help='Include forked repositories')
def top(username, token, limit, sort, forks):
    """Display top repositories by various metrics."""
    try:
        with console.status(f"[bold green]Fetching top repositories for {username}...", spinner="dots"):
            client = GitHubStatsClient(username, token)
            top_repos = client.get_top_repos(limit=limit, sort_by=sort, include_forks=forks)
        
        display_top_repos(top_repos, sort_by=sort)
        
        # Show rate limit
        remaining, limit_total = client.get_rate_limit()
        display_rate_limit(remaining, limit_total)
        
    except ValueError as e:
        display_error(str(e))
        raise click.Abort()


@main.command()
@click.argument('username')
@click.option('--token', '-t', envvar='GITHUB_TOKEN', help='GitHub personal access token')
@click.option('--top-repos', '-r', default=5, help='Number of top repos to show (default: 5)')
@click.option('--top-langs', '-l', default=10, help='Number of top languages to show (default: 10)')
@click.option('--forks/--no-forks', default=False, help='Include forked repositories')
def overview(username, token, top_repos, top_langs, forks):
    """Display a complete overview of user stats (profile + repos + languages)."""
    try:
        client = GitHubStatsClient(username, token)
        
        with console.status(f"[bold green]Fetching complete overview for {username}...", spinner="dots"):
            # Fetch all data
            user_data = client.get_user_info()
            repo_stats = client.get_repo_stats(include_forks=forks)
            lang_stats = client.get_language_stats(include_forks=forks)
            top_repositories = client.get_top_repos(limit=top_repos, sort_by='stars', include_forks=forks)
        
        # Display everything
        display_user_info(user_data)
        display_repo_stats(repo_stats)
        display_language_stats(lang_stats, limit=top_langs)
        display_top_repos(top_repositories, sort_by='stars')
        
        # Show rate limit
        remaining, limit = client.get_rate_limit()
        display_rate_limit(remaining, limit)
        
    except ValueError as e:
        display_error(str(e))
        raise click.Abort()


@main.command()
@click.option('--token', '-t', envvar='GITHUB_TOKEN', help='GitHub personal access token')
def rate_limit(token):
    """Check current API rate limit status."""
    try:
        # Use a dummy username just to initialize client
        client = GitHubStatsClient('dummy', token)
        remaining, limit = client.get_rate_limit()
        
        console.print(f"\n[bold cyan]GitHub API Rate Limit Status[/bold cyan]\n")
        console.print(f"Remaining requests: [bold green]{remaining}[/bold green]")
        console.print(f"Total limit: [bold blue]{limit}[/bold blue]")
        console.print(f"Percentage used: [bold yellow]{((limit-remaining)/limit*100):.1f}%[/bold yellow]\n")
        
        if not token:
            display_info("💡 Tip: Use a GitHub token (--token or GITHUB_TOKEN env var) for 5000 requests/hour instead of 60")
        
    except ValueError as e:
        display_error(str(e))
        raise click.Abort()


if __name__ == '__main__':
    main()