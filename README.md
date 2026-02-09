# GitHub Stats CLI 📊

A beautiful command-line tool to fetch and display GitHub user and repository statistics with rich formatting.

## Features ✨

- 👤 **User Profile**: Display comprehensive user information
- 📊 **Language Stats**: Visualize programming language breakdown with bar charts
- 📈 **Repository Stats**: View aggregate repository statistics
- 🏆 **Top Repositories**: List top repos by stars, forks, watchers, or size
- 🎯 **Complete Overview**: Get everything in one command
- 🎨 **Beautiful CLI**: Rich formatting with colors, tables, and panels
- ⚡ **Fast**: Efficient API usage with proper rate limit handling

## Installation

### From TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps github-stats-cli
pip install requests rich click  # Install dependencies separately
```

### From Source

```bash
git clone https://github.com/yourusername/github-stats-cli.git
cd github-stats-cli
pip install -e .
```

## Quick Start

### Basic Usage

```bash
# View user profile
ghstats user torvalds

# View language breakdown
ghstats languages torvalds

# View repository statistics
ghstats repos torvalds

# View top repositories
ghstats top torvalds

# Complete overview
ghstats overview torvalds
```

### Using a GitHub Token (Recommended)

For higher rate limits (5000/hour vs 60/hour):

```bash
# Set token as environment variable
export GITHUB_TOKEN=your_token_here

# Or pass it directly
ghstats user torvalds --token your_token_here
```

## Commands

### `ghstats user <username>`

Display user profile information including bio, followers, repositories, etc.

**Options:**
- `--token, -t`: GitHub personal access token

**Example:**
```bash
ghstats user torvalds
```

### `ghstats languages <username>`

Display programming language statistics across all repositories.

**Options:**
- `--token, -t`: GitHub personal access token
- `--limit, -l`: Number of languages to display (default: 10)
- `--forks/--no-forks`: Include forked repositories (default: no)

**Example:**
```bash
ghstats languages torvalds --limit 5
ghstats languages octocat --forks
```

### `ghstats repos <username>`

Display aggregate repository statistics (total stars, forks, watchers, size).

**Options:**
- `--token, -t`: GitHub personal access token
- `--forks/--no-forks`: Include forked repositories (default: no)

**Example:**
```bash
ghstats repos torvalds
```

### `ghstats top <username>`

Display top repositories sorted by various metrics.

**Options:**
- `--token, -t`: GitHub personal access token
- `--limit, -l`: Number of repositories to display (default: 10)
- `--sort, -s`: Sort by metric (choices: stars, forks, watchers, size, updated; default: stars)
- `--forks/--no-forks`: Include forked repositories (default: no)

**Examples:**
```bash
ghstats top torvalds --limit 5
ghstats top octocat --sort forks
ghstats top github --sort updated --limit 20
```

### `ghstats overview <username>`

Display a complete overview including profile, repo stats, languages, and top repos.

**Options:**
- `--token, -t`: GitHub personal access token
- `--top-repos, -r`: Number of top repos to show (default: 5)
- `--top-langs, -l`: Number of top languages to show (default: 10)
- `--forks/--no-forks`: Include forked repositories (default: no)

**Example:**
```bash
ghstats overview torvalds --top-repos 10 --top-langs 5
```

### `ghstats rate-limit`

Check current API rate limit status.

**Options:**
- `--token, -t`: GitHub personal access token

**Example:**
```bash
ghstats rate-limit
```

## GitHub Token Setup

To get a GitHub personal access token:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name (e.g., "GitHub Stats CLI")
4. No special scopes are needed for public data
5. Click "Generate token"
6. Copy the token and set it as an environment variable:

```bash
export GITHUB_TOKEN=your_token_here
```

Or add it to your shell profile (~/.bashrc, ~/.zshrc, etc.):

```bash
echo 'export GITHUB_TOKEN=your_token_here' >> ~/.bashrc
source ~/.bashrc
```

## Examples

### Analyze your own profile

```bash
ghstats overview yourusername --top-repos 10
```

### Compare top repositories

```bash
ghstats top torvalds --sort stars --limit 5
ghstats top guido --sort stars --limit 5
```

### Find language trends

```bash
ghstats languages facebook --limit 15
ghstats languages google --limit 15
```

### Check multiple users quickly

```bash
for user in torvalds gvanrossum dhh; do
  echo "=== $user ==="
  ghstats repos $user
done
```

## Output Examples

### User Profile
```
╭─────────────────── 👤 User Profile ────────────────────╮
│ Name: Linus Torvalds                                   │
│ Username: torvalds                                     │
│ Bio: Creator of Linux                                  │
│ Location: Portland, OR                                 │
│ ...                                                    │
╰────────────────────────────────────────────────────────╯
```

### Language Breakdown
```
📊 Language Breakdown (Top 10)

C              ████████████████████████████████████████ 96.8%
Assembly       ███ 2.1%
Shell          █ 0.8%
Python         █ 0.3%
```

## Dependencies

- `requests`: HTTP library for API calls
- `rich`: Beautiful terminal formatting
- `click`: Command-line interface framework

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Author

Your Name - your.email@example.com

## Links

- GitHub: https://github.com/yourusername/github-stats-cli
- PyPI: https://pypi.org/project/github-stats-cli/
- Issues: https://github.com/yourusername/github-stats-cli/issues