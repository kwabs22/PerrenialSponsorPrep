"""
GitLab AI Code Review
Showcases: GitLab Duo AI
"""
import os
from dotenv import load_dotenv
import gitlab

load_dotenv()

GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.com")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")

def get_gitlab_client():
    """Initialize GitLab client."""
    return gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)

def get_merge_request_diff(gl, project_id: int, mr_iid: int):
    """Get merge request changes."""
    project = gl.projects.get(project_id)
    mr = project.mergerequests.get(mr_iid)

    return {
        "title": mr.title,
        "description": mr.description,
        "source_branch": mr.source_branch,
        "target_branch": mr.target_branch,
        "changes": mr.changes()
    }

def analyze_code_changes(changes: dict):
    """Analyze code changes for review."""
    analysis = {
        "files_changed": len(changes.get("changes", [])),
        "suggestions": [],
        "security_notes": [],
        "style_notes": []
    }

    for change in changes.get("changes", []):
        filename = change.get("new_path", "")
        diff = change.get("diff", "")

        # Simple pattern detection
        if "password" in diff.lower() or "secret" in diff.lower():
            analysis["security_notes"].append(
                f"Potential sensitive data in {filename}"
            )

        if "TODO" in diff or "FIXME" in diff:
            analysis["suggestions"].append(
                f"Found TODO/FIXME comments in {filename}"
            )

        if len(diff.split("\n")) > 200:
            analysis["suggestions"].append(
                f"Large diff in {filename} - consider splitting"
            )

    return analysis

def generate_mr_summary(mr_data: dict, analysis: dict):
    """Generate AI-style MR summary."""
    return f"""
## Merge Request Summary

**{mr_data['title']}**

### Changes Overview
- **Files Changed**: {analysis['files_changed']}
- **Source Branch**: {mr_data['source_branch']}
- **Target Branch**: {mr_data['target_branch']}

### Review Notes

#### Suggestions
{chr(10).join(f'- {s}' for s in analysis['suggestions']) or '- No suggestions'}

#### Security Notes
{chr(10).join(f'- {s}' for s in analysis['security_notes']) or '- No security concerns detected'}

---
*Generated with GitLab Duo AI*
"""

def main():
    print("=" * 50)
    print("GitLab AI Code Review")
    print("=" * 50)

    if not GITLAB_TOKEN:
        print("\nSetup required:")
        print("1. Create GitLab Personal Access Token")
        print("2. Grant 'api' and 'read_repository' scopes")
        print("3. Enable GitLab Duo in project settings")
        print("4. Copy credentials to .env file")

        print("\n🤖 GitLab Duo Features:")
        print("  - Code Suggestions (AI completions)")
        print("  - MR Summaries (auto-descriptions)")
        print("  - Vulnerability Detection")
        print("  - Test Generation")

        print("\n📋 Example Duo Commands:")
        print("""
# In GitLab IDE
/duo explain      - Explain selected code
/duo refactor     - Suggest refactoring
/duo test         - Generate tests
/duo fix          - Fix issues
        """)
        return

    gl = get_gitlab_client()
    print(f"\nConnected to: {GITLAB_URL}")

    if PROJECT_ID:
        try:
            project = gl.projects.get(PROJECT_ID)
            print(f"Project: {project.name}")

            # Get open MRs
            mrs = project.mergerequests.list(state="opened")
            print(f"\nOpen MRs: {len(mrs)}")

            if mrs:
                mr = mrs[0]
                print(f"\n🔍 Analyzing MR !{mr.iid}: {mr.title}")

                mr_data = get_merge_request_diff(gl, PROJECT_ID, mr.iid)
                analysis = analyze_code_changes(mr_data)

                summary = generate_mr_summary(mr_data, analysis)
                print(summary)

        except Exception as e:
            print(f"Error: {e}")
    else:
        print("\nDemo mode (no PROJECT_ID set)")

        # Demo analysis
        demo_analysis = {
            "files_changed": 5,
            "suggestions": ["Consider adding tests for new function"],
            "security_notes": []
        }

        demo_mr = {
            "title": "Add user authentication",
            "source_branch": "feature/auth",
            "target_branch": "main"
        }

        print(generate_mr_summary(demo_mr, demo_analysis))

if __name__ == "__main__":
    main()
