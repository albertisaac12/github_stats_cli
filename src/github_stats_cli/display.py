"""Display formatting for GitHub statistics using rich library."""

from typing import Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from rich import box
from rich.text import Text


console = Console()


def display_user_info(user_data: Dict):
    """Display basic user information."""
    name = user_data.get('name', 'N/A')
    login = user_data['login']
    bio = user_data.get('bio', 'No bio available')
    location = user_data.get('location', 'N/A')
    company = user_data.get('company', 'N/A')
    blog = user_data.get('blog', 'N/A')
    followers = user_data['followers']
    following = user_data['following']
    public_repos = user_data['public_repos']
    created_at = user_data['created_at'][:10]
    
    info_text = f"""[bold cyan]Name:[/bold cyan] {name}
[bold cyan]Username:[/bold cyan] {login}
[bold cyan]Bio:[/bold cyan] {bio}
[bold cyan]Location:[/bold cyan] {location}
[bold cyan]Company:[/bold cyan] {company}
[bold cyan]Website:[/bold cyan] {blog}
[bold cyan]Followers:[/bold cyan] {followers} | [bold cyan]Following:[/bold cyan] {following}
[bold cyan]Public Repositories:[/bold cyan] {public_repos}
[bold cyan]Account Created:[/bold cyan] {created_at}"""
    
    panel = Panel(info_text, title="[bold green]👤 User Profile[/bold green]", border_style="green")
    console.print(panel)


def display_language_stats(languages: Dict[str, float], limit: int = 10):
    """Display language statistics as a bar chart."""
    if not languages:
        console.print("[yellow]No language data available[/yellow]")
        return
    
    console.print(f"\n[bold green]📊 Language Breakdown (Top {limit})[/bold green]\n")
    
    # Get top languages
    top_languages = list(languages.items())[:limit]
    max_percentage = max(pct for _, pct in top_languages) if top_languages else 0
    
    for lang, percentage in top_languages:
        # Create a visual bar
        bar_length = int((percentage / max_percentage) * 40) if max_percentage > 0 else 0
        bar = "█" * bar_length
        
        # Color coding for different languages
        color = _get_language_color(lang)
        console.print(f"[{color}]{lang:15s}[/{color}] [{color}]{bar}[/{color}] {percentage:5.1f}%")


def display_repo_stats(stats: Dict):
    """Display repository statistics."""
    table = Table(title="[bold green]📈 Repository Statistics[/bold green]", 
                  box=box.ROUNDED, show_header=False)
    
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    
    table.add_row("Total Repositories", str(stats['total_repos']))
    table.add_row("Total Stars", f"⭐ {stats['total_stars']}")
    table.add_row("Total Forks", f"🍴 {stats['total_forks']}")
    table.add_row("Total Watchers", f"👁️  {stats['total_watchers']}")
    table.add_row("Total Size", f"{stats['total_size_kb']:,} KB")
    
    console.print("\n")
    console.print(table)


def display_top_repos(repos: List[Dict], sort_by: str = 'stars'):
    """Display top repositories in a table."""
    if not repos:
        console.print("[yellow]No repositories found[/yellow]")
        return
    
    sort_icons = {
        'stars': '⭐',
        'forks': '🍴',
        'watchers': '👁️',
        'size': '📦',
        'updated': '🕐'
    }
    
    icon = sort_icons.get(sort_by, '⭐')
    table = Table(title=f"[bold green]{icon} Top Repositories (by {sort_by})[/bold green]", 
                  box=box.ROUNDED)
    
    table.add_column("Repository", style="cyan", no_wrap=True)
    table.add_column("Description", style="white", max_width=50)
    table.add_column("Language", style="yellow")
    table.add_column("⭐ Stars", justify="right", style="green")
    table.add_column("🍴 Forks", justify="right", style="blue")
    table.add_column("📦 Size (KB)", justify="right", style="magenta")
    
    for repo in repos:
        name = repo['name']
        desc = repo['description'] or "No description"
        lang = repo['language'] or "N/A"
        stars = str(repo['stargazers_count'])
        forks = str(repo['forks_count'])
        size = f"{repo['size']:,}"
        
        table.add_row(name, desc, lang, stars, forks, size)
    
    console.print("\n")
    console.print(table)


def display_rate_limit(remaining: int, limit: int):
    """Display API rate limit information."""
    percentage = (remaining / limit) * 100 if limit > 0 else 0
    
    if percentage > 50:
        color = "green"
    elif percentage > 20:
        color = "yellow"
    else:
        color = "red"
    
    console.print(f"\n[{color}]API Rate Limit: {remaining}/{limit} requests remaining ({percentage:.1f}%)[/{color}]")


def display_error(message: str):
    """Display an error message."""
    console.print(f"\n[bold red]❌ Error:[/bold red] {message}\n")


def display_success(message: str):
    """Display a success message."""
    console.print(f"\n[bold green]✅ {message}[/bold green]\n")


def display_info(message: str):
    """Display an info message."""
    console.print(f"\n[bold blue]ℹ️  {message}[/bold blue]\n")


def _get_language_color(language: str) -> str:
    """Get color for a programming language."""
    colors = {
        'Python': 'blue',
        'JavaScript': 'yellow',
        'TypeScript': 'cyan',
        'Java': 'red',
        'C++': 'magenta',
        'C': 'blue',
        'Go': 'cyan',
        'Rust': 'red',
        'Ruby': 'red',
        'PHP': 'purple',
        'Swift': 'orange1',
        'Kotlin': 'purple',
        'Shell': 'green',
        'HTML': 'red',
        'CSS': 'blue',
        'C#': 'purple',
    }
    return colors.get(language, 'white')