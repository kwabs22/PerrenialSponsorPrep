"""
GitHub PR Bot
Showcases: Dependabot Grouped + Actions
"""
import os
from dotenv import load_dotenv
from github import Github

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPO", "owner/repo")

def get_github_client():
    """Initialize GitHub client."""
    return Github(GITHUB_TOKEN)

def list_dependabot_prs(repo):
    """List Dependabot PRs that could be grouped."""
    prs = repo.get_pulls(state="open")
    dependabot_prs = []

    for pr in prs:
        if pr.user.login == "dependabot[bot]":
            dependabot_prs.append({
                "number": pr.number,
                "title": pr.title,
                "labels": [l.name for l in pr.labels],
                "created": pr.created_at
            })

    return dependabot_prs

def create_grouped_pr_comment(prs: list):
    """Create comment suggesting grouping."""
    if len(prs) < 2:
        return None

    packages = [pr["title"].split(" from ")[0].replace("Bump ", "") for pr in prs]

    return f"""
## Dependabot Grouping Suggestion

Found {len(prs)} open dependency updates that could be grouped:

{chr(10).join(f'- {pkg}' for pkg in packages[:10])}

### Enable Grouping

Add this to `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      production-dependencies:
        patterns:
          - "*"
        exclude-patterns:
          - "eslint*"
          - "prettier*"
      development-dependencies:
        dependency-type: "development"
```

This will batch updates into fewer PRs!
"""

def analyze_pr(repo, pr_number: int):
    """Analyze a PR for potential issues."""
    pr = repo.get_pull(pr_number)

    analysis = {
        "pr_number": pr_number,
        "title": pr.title,
        "files_changed": pr.changed_files,
        "additions": pr.additions,
        "deletions": pr.deletions,
        "checks": []
    }

    # Get check runs
    commits = pr.get_commits()
    last_commit = list(commits)[-1] if commits.totalCount > 0 else None

    if last_commit:
        check_runs = last_commit.get_check_runs()
        for check in check_runs:
            analysis["checks"].append({
                "name": check.name,
                "status": check.status,
                "conclusion": check.conclusion
            })

    return analysis

def main():
    print("=" * 50)
    print("GitHub PR Bot")
    print("=" * 50)

    if not GITHUB_TOKEN:
        print("\nSetup required:")
        print("1. Create GitHub Personal Access Token")
        print("2. Grant 'repo' scope")
        print("3. Copy token to .env file")

        print("\n🔧 Features demonstrated:")
        print("  - Dependabot grouped updates")
        print("  - PR analysis and review")
        print("  - Check run status")
        return

    g = get_github_client()
    print(f"\nAuthenticated as: {g.get_user().login}")

    # Demo with a public repo
    try:
        repo = g.get_repo(REPO_NAME)
        print(f"Repository: {repo.full_name}")
    except:
        print(f"\nUsing demo mode (repo '{REPO_NAME}' not accessible)")

        print("\n📋 Dependabot Grouping Config:")
        print("""
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      python-packages:
        patterns:
          - "*"
        """)

        print("\n🤖 Bot Capabilities:")
        print("  1. List open Dependabot PRs")
        print("  2. Suggest grouping configuration")
        print("  3. Analyze PR changes")
        print("  4. Check CI status")
        print("  5. Auto-merge passing updates")
        return

    # List Dependabot PRs
    print("\n📦 Scanning for Dependabot PRs...")
    dependabot_prs = list_dependabot_prs(repo)

    if dependabot_prs:
        print(f"Found {len(dependabot_prs)} Dependabot PRs:")
        for pr in dependabot_prs[:5]:
            print(f"  #{pr['number']}: {pr['title']}")

        # Suggest grouping
        suggestion = create_grouped_pr_comment(dependabot_prs)
        if suggestion:
            print("\n💡 Grouping Suggestion Generated")
    else:
        print("No open Dependabot PRs found")

    # Analyze recent PR
    open_prs = list(repo.get_pulls(state="open"))[:1]
    if open_prs:
        print(f"\n🔍 Analyzing PR #{open_prs[0].number}...")
        analysis = analyze_pr(repo, open_prs[0].number)
        print(f"  Files: {analysis['files_changed']}")
        print(f"  +{analysis['additions']} -{analysis['deletions']}")

if __name__ == "__main__":
    main()
