# GitHub Stats CLI - Usage Examples

## Command Examples with Expected Outputs

### 1. User Profile Command

```bash
ghstats user torvalds
```

**Expected Output:**
```
╭─────────────────────────────── 👤 User Profile ───────────────────────────────╮
│ Name: Linus Torvalds                                                          │
│ Username: torvalds                                                            │
│ Bio: N/A                                                                      │
│ Location: Portland, OR                                                        │
│ Company: Linux Foundation                                                     │
│ Website: N/A                                                                  │
│ Followers: 180000 | Following: 0                                             │
│ Public Repositories: 6                                                        │
│ Account Created: 2011-09-03                                                   │
╰───────────────────────────────────────────────────────────────────────────────╯

API Rate Limit: 59/60 requests remaining (98.3%)
```

---

### 2. Language Breakdown Command

```bash
ghstats languages torvalds --limit 5
```

**Expected Output:**
```
📊 Language Breakdown (Top 5)

C              ████████████████████████████████████████ 96.8%
Assembly       ███ 2.1%
Shell          █ 0.8%
Python         █ 0.3%
Makefile       █ 0.0%

API Rate Limit: 53/60 requests remaining (88.3%)
```

With color coding:
- Blue: C, Python
- Yellow: JavaScript
- Cyan: Go, TypeScript
- Red: Java, Ruby, Rust

---

### 3. Repository Statistics Command

```bash
ghstats repos octocat
```

**Expected Output:**
```
╭─────────────────────── 📈 Repository Statistics ───────────────────────╮
│ Metric              │ Value                                            │
├─────────────────────┼──────────────────────────────────────────────────┤
│ Total Repositories  │ 8                                                │
│ Total Stars         │ ⭐ 3456                                          │
│ Total Forks         │ 🍴 1234                                          │
│ Total Watchers      │ 👁️  2345                                         │
│ Total Size          │ 45,678 KB                                        │
╰─────────────────────┴──────────────────────────────────────────────────╯

API Rate Limit: 52/60 requests remaining (86.7%)
```

---

### 4. Top Repositories Command

```bash
ghstats top github --sort stars --limit 5
```

**Expected Output:**
```
╭──────────────────────────── ⭐ Top Repositories (by stars) ─────────────────────────────╮
│ Repository      │ Description                      │ Language   │ ⭐ Stars │ 🍴 Forks │
├─────────────────┼──────────────────────────────────┼────────────┼──────────┼──────────┤
│ docs            │ The open-source repo for docs    │ JavaScript │    14500 │     8900 │
│ github          │ GitHub's public roadmap          │ N/A        │    12300 │     2100 │
│ feedback        │ Public feedback discussions      │ N/A        │    11000 │      890 │
│ copilot.vim     │ Neovim plugin for GitHub Copilot │ Vim script │     8900 │      450 │
│ explore         │ Community-curated topic pages    │ Ruby       │     7800 │     1200 │
╰─────────────────┴──────────────────────────────────┴────────────┴──────────┴──────────╯

API Rate Limit: 51/60 requests remaining (85.0%)
```

---

### 5. Complete Overview Command

```bash
ghstats overview octocat --top-repos 3 --top-langs 5
```

**Expected Output:**
```
╭─────────────────────────────── 👤 User Profile ───────────────────────────────╮
│ Name: The Octocat                                                             │
│ Username: octocat                                                             │
│ Bio: N/A                                                                      │
│ Location: San Francisco                                                       │
│ Company: @github                                                              │
│ Website: https://github.blog                                                  │
│ Followers: 9000 | Following: 9                                               │
│ Public Repositories: 8                                                        │
│ Account Created: 2011-01-25                                                   │
╰───────────────────────────────────────────────────────────────────────────────╯

╭─────────────────────── 📈 Repository Statistics ───────────────────────╮
│ Metric              │ Value                                            │
├─────────────────────┼──────────────────────────────────────────────────┤
│ Total Repositories  │ 8                                                │
│ Total Stars         │ ⭐ 3456                                          │
│ Total Forks         │ 🍴 1234                                          │
│ Total Watchers      │ 👁️  2345                                         │
│ Total Size          │ 45,678 KB                                        │
╰─────────────────────┴──────────────────────────────────────────────────╯

📊 Language Breakdown (Top 5)

Ruby           ████████████████████████████████████████ 45.2%
JavaScript     ███████████████████████ 32.1%
HTML           ██████████ 15.3%
CSS            ████ 5.8%
Shell          █ 1.6%

╭────────────────────── ⭐ Top Repositories (by stars) ──────────────────────╮
│ Repository │ Description               │ Language   │ ⭐ Stars │ 🍴 Forks │
├────────────┼───────────────────────────┼────────────┼──────────┼──────────┤
│ Hello-Wor  │ My first repository       │ N/A        │     1800 │      890 │
│ Spoon-Kni  │ This repo is for demons.. │ N/A        │      890 │      456 │
│ test       │ Testing repository        │ Ruby       │      450 │      123 │
╰────────────┴───────────────────────────┴────────────┴──────────┴──────────╯

API Rate Limit: 45/60 requests remaining (75.0%)
```

---

### 6. Different Sorting Options

#### By Forks
```bash
ghstats top facebook --sort forks --limit 3
```

#### By Watchers
```bash
ghstats top google --sort watchers --limit 3
```

#### By Last Updated
```bash
ghstats top microsoft --sort updated --limit 5
```

#### By Size
```bash
ghstats top torvalds --sort size --limit 3
```

---

### 7. Including Forked Repositories

```bash
# Without forks (default)
ghstats languages yourusername

# With forks
ghstats languages yourusername --forks
```

---

### 8. Rate Limit Check

```bash
ghstats rate-limit
```

**Without Token:**
```
GitHub API Rate Limit Status

Remaining requests: 45
Total limit: 60
Percentage used: 25.0%

ℹ️  💡 Tip: Use a GitHub token (--token or GITHUB_TOKEN env var) for 5000 
    requests/hour instead of 60
```

**With Token:**
```
GitHub API Rate Limit Status

Remaining requests: 4850
Total limit: 5000
Percentage used: 3.0%
```

---

### 9. Using Token

```bash
# Pass directly
ghstats user torvalds --token ghp_xxxxxxxxxxxxxxxxxxxx

# Using environment variable
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
ghstats user torvalds

# Or in one line
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx ghstats user torvalds
```

---

### 10. Advanced Usage Examples

#### Compare Multiple Users (using shell loop)
```bash
for user in torvalds gvanrossum dhh; do
  echo "========== $user =========="
  ghstats repos $user
  echo ""
done
```

#### Find Top Languages Across Organizations
```bash
ghstats languages google --limit 15
ghstats languages facebook --limit 15
ghstats languages microsoft --limit 15
```

#### Monitor Your Own Stats
```bash
# Create a monitoring script
#!/bin/bash
MYUSER="yourusername"
echo "Daily GitHub Stats Report - $(date)"
echo "=================================="
ghstats overview $MYUSER --top-repos 5 --top-langs 10
```

#### Export and Process (requires adding export feature)
```bash
# Future feature
ghstats export octocat --output octocat.json
cat octocat.json | jq '.language_stats'
```

---

## Error Messages

### User Not Found
```bash
ghstats user nonexistentuser123456
```
```
❌ Error: User 'nonexistentuser123456' not found
```

### Rate Limit Exceeded
```bash
ghstats languages torvalds  # After many requests
```
```
❌ Error: API rate limit exceeded. Use a GitHub token for higher limits.
```

### Network Error
```
❌ Error: Network error: Failed to connect to api.github.com
```

---

## Tips for Best Results

1. **Use a token** - Get 5000 requests/hour instead of 60
2. **Exclude forks** - More accurate language stats (default behavior)
3. **Adjust limits** - Use `--limit` to see more or fewer results
4. **Try different sorts** - Find interesting patterns in repos
5. **Check rate limit** - Use `ghstats rate-limit` before big queries

---

## Real-World Use Cases

### 1. Evaluating a Developer Before Hiring
```bash
ghstats overview candidate_username --top-repos 10
```
See their language proficiency, popular projects, and contribution style.

### 2. Finding Similar Developers
```bash
ghstats languages known_expert --limit 5
# Note their top languages, then search for others
```

### 3. Research for Tech Blog Post
```bash
ghstats languages google --limit 20
ghstats languages facebook --limit 20
# Compare tech stacks of major companies
```

### 4. Portfolio Building
```bash
ghstats overview yourusername --top-repos 10
# Share the formatted output on your website
```

### 5. Open Source Project Discovery
```bash
ghstats top organization_name --sort stars --limit 20
# Find the most popular projects from an organization
```

---

## Color Scheme Reference

The CLI uses rich colors for better readability:

- **Cyan**: Labels, usernames, repository names
- **Green**: Success messages, positive metrics
- **Yellow**: Warnings, JavaScript
- **Red**: Errors, Java, Ruby
- **Blue**: Python, C, general info
- **Magenta**: Secondary metrics
- **Purple**: PHP, Kotlin, C#
- **White**: Default text

Enjoy exploring GitHub with beautiful, informative stats! 🚀