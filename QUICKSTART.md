# GitHub Stats CLI - Quick Start Guide

## 🚀 Building and Publishing to TestPyPI

### Step 1: Install Build Tools

```bash
pip install build twine
```

### Step 2: Build the Package

Navigate to the package directory and build:

```bash
cd github-stats-cli
python -m build
```

This creates two files in the `dist/` directory:
- `github_stats_cli-0.1.0.tar.gz` (source distribution)
- `github_stats_cli-0.1.0-py3-none-any.whl` (wheel distribution)

### Step 3: Create TestPyPI Account

1. Go to https://test.pypi.org/account/register/
2. Create an account and verify your email

### Step 4: Create API Token

1. Go to https://test.pypi.org/manage/account/
2. Scroll to "API tokens" section
3. Click "Add API token"
4. Set the token name (e.g., "github-stats-cli")
5. Set scope to "Entire account" (for first upload)
6. Click "Add token"
7. **IMPORTANT**: Copy the token immediately (it won't be shown again)

### Step 5: Upload to TestPyPI

```bash
python -m twine upload --repository testpypi dist/*
```

When prompted:
- Username: `__token__`
- Password: (paste your API token, including the `pypi-` prefix)

### Step 6: Install from TestPyPI

Test the installation:

```bash
# Create a new virtual environment (recommended)
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --no-deps github-stats-cli

# Install dependencies from regular PyPI
pip install requests rich click
```

### Step 7: Test the CLI

```bash
# Test basic commands
ghstats user octocat
ghstats languages torvalds --limit 5
ghstats top github --sort stars --limit 10
ghstats overview octocat
```

## 🎯 Using the Package

### Set Up GitHub Token (Optional but Recommended)

For higher rate limits (5000/hour instead of 60/hour):

```bash
# Linux/Mac
export GITHUB_TOKEN=your_token_here

# Or add to ~/.bashrc or ~/.zshrc
echo 'export GITHUB_TOKEN=your_token_here' >> ~/.bashrc
source ~/.bashrc
```

### Available Commands

```bash
# Show help
ghstats --help

# User profile
ghstats user <username>

# Language breakdown
ghstats languages <username>
ghstats languages <username> --limit 15 --forks

# Repository stats
ghstats repos <username>

# Top repositories
ghstats top <username>
ghstats top <username> --sort forks --limit 20
ghstats top <username> --sort updated

# Complete overview
ghstats overview <username>
ghstats overview <username> --top-repos 10 --top-langs 15

# Check rate limit
ghstats rate-limit
```

## 📦 Package Structure

```
github-stats-cli/
├── pyproject.toml          # Package configuration
├── README.md               # Documentation
├── LICENSE                 # MIT License
├── MANIFEST.in            # Files to include in distribution
├── .gitignore             # Git ignore rules
├── src/
│   └── github_stats_cli/
│       ├── __init__.py    # Package initialization
│       ├── client.py      # GitHub API client
│       ├── display.py     # Rich formatting and display
│       └── cli.py         # Click CLI commands
└── tests/
    └── test_client.py     # Basic tests
```

## 🔄 Publishing Updates

When you make changes and want to publish a new version:

1. **Update version** in `pyproject.toml`:
   ```toml
   version = "0.1.1"  # Increment version
   ```

2. **Update version** in `src/github_stats_cli/__init__.py`:
   ```python
   __version__ = "0.1.1"
   ```

3. **Update version** in `src/github_stats_cli/cli.py`:
   ```python
   @click.version_option(version='0.1.1')
   ```

4. **Rebuild and upload**:
   ```bash
   # Remove old distributions
   rm -rf dist/
   
   # Build new distributions
   python -m build
   
   # Upload to TestPyPI
   python -m twine upload --repository testpypi dist/*
   ```

## 🌐 Publishing to Real PyPI (When Ready)

Once you've tested on TestPyPI and everything works:

1. Create account at https://pypi.org
2. Create API token at https://pypi.org/manage/account/
3. Upload to PyPI:
   ```bash
   python -m twine upload dist/*
   ```

4. Install from PyPI:
   ```bash
   pip install github-stats-cli
   ```

## 🐛 Troubleshooting

### "Package already exists"
- Increment the version number in `pyproject.toml`
- You cannot overwrite existing versions

### "Invalid authentication credentials"
- Make sure you're using `__token__` as username (not your account username)
- Ensure you copied the full token including `pypi-` prefix
- Check token hasn't expired

### Rate limit errors
- Use a GitHub token with `--token` or `GITHUB_TOKEN` environment variable
- Check remaining requests: `ghstats rate-limit`

### Dependencies not found
- When installing from TestPyPI, install dependencies separately:
  ```bash
  pip install requests rich click
  ```

## 💡 Tips

1. **Always test locally first**:
   ```bash
   pip install -e .
   ghstats user octocat
   ```

2. **Use semantic versioning**: MAJOR.MINOR.PATCH (e.g., 1.0.0)
   - MAJOR: Breaking changes
   - MINOR: New features (backward compatible)
   - PATCH: Bug fixes

3. **Keep a changelog**: Document changes between versions

4. **Test with different users**: Try popular GitHub users with lots of repos

## 📚 Next Steps

### Features to Add

1. **Export functionality**:
   - Export stats to JSON
   - Export stats to CSV
   - Generate markdown reports

2. **Caching**:
   - Cache API responses locally
   - Add `--refresh` flag to bypass cache

3. **Comparison mode**:
   - Compare two users side-by-side
   - Show differences in language stats

4. **Visualization**:
   - Generate graphs/charts
   - Create GitHub-style contribution graphs

5. **Organization support**:
   - Fetch organization stats
   - Show team contributions

6. **More metrics**:
   - Calculate contribution streaks
   - Show commit activity patterns
   - Find most active repositories by commits

### Example Implementation: JSON Export

Add to `cli.py`:

```python
@main.command()
@click.argument('username')
@click.option('--token', '-t', envvar='GITHUB_TOKEN')
@click.option('--output', '-o', default='stats.json', help='Output file')
def export(username, token, output):
    """Export user stats to JSON file."""
    import json
    
    client = GitHubStatsClient(username, token)
    user_data = client.get_user_info()
    repo_stats = client.get_repo_stats()
    lang_stats = client.get_language_stats()
    
    data = {
        'user': user_data,
        'repository_stats': repo_stats,
        'language_stats': lang_stats
    }
    
    with open(output, 'w') as f:
        json.dump(data, f, indent=2)
    
    display_success(f"Stats exported to {output}")
```

## 🎓 Learning Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [Click Documentation](https://click.palletsprojects.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [GitHub REST API](https://docs.github.com/en/rest)

Happy coding! 🚀