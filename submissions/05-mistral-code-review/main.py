"""
Mistral AI Code Review Bot
Showcases: Codestral + Function Calling
1-hour hackathon submission

This demo uses Codestral for intelligent code review with structured output.
"""
import os
import sys
import json
from pathlib import Path
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

# Code review function schema for structured output
REVIEW_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "submit_code_review",
            "description": "Submit a structured code review with issues and suggestions",
            "parameters": {
                "type": "object",
                "properties": {
                    "overall_quality": {
                        "type": "string",
                        "enum": ["excellent", "good", "needs_improvement", "poor"],
                        "description": "Overall code quality assessment"
                    },
                    "issues": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "severity": {"type": "string", "enum": ["critical", "warning", "info"]},
                                "line": {"type": "integer"},
                                "description": {"type": "string"},
                                "suggestion": {"type": "string"}
                            },
                            "required": ["severity", "description"]
                        },
                        "description": "List of issues found in the code"
                    },
                    "improvements": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "General improvement suggestions"
                    },
                    "summary": {
                        "type": "string",
                        "description": "Brief summary of the review"
                    }
                },
                "required": ["overall_quality", "issues", "improvements", "summary"]
            }
        }
    }
]


def load_code(file_path: str) -> tuple[str, str]:
    """Load code from file and detect language"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Detect language from extension
    lang_map = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".go": "Go",
        ".rs": "Rust",
        ".rb": "Ruby",
        ".php": "PHP"
    }

    language = lang_map.get(path.suffix.lower(), "Unknown")

    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    return code, language


def review_code(code: str, language: str, filename: str) -> dict:
    """Review code using Codestral with function calling"""
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

    prompt = f"""You are an expert code reviewer. Review the following {language} code from file '{filename}'.

Analyze the code for:
1. Bugs and potential issues
2. Security vulnerabilities
3. Performance problems
4. Code style and best practices
5. Readability and maintainability

Code to review:
```{language.lower()}
{code}
```

Use the submit_code_review function to provide your structured review."""

    response = client.chat.complete(
        model="codestral-latest",
        messages=[{"role": "user", "content": prompt}],
        tools=REVIEW_TOOLS,
        tool_choice="any"
    )

    # Extract function call result
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        return json.loads(tool_call.function.arguments)

    # Fallback if no function call
    return {
        "overall_quality": "unknown",
        "issues": [],
        "improvements": ["Could not generate structured review"],
        "summary": response.choices[0].message.content
    }


def format_review(review: dict) -> str:
    """Format the review for display"""
    output = []

    # Quality badge
    quality_emoji = {
        "excellent": "🌟",
        "good": "✅",
        "needs_improvement": "⚠️",
        "poor": "❌"
    }
    emoji = quality_emoji.get(review["overall_quality"], "❓")
    output.append(f"\n{emoji} Overall Quality: {review['overall_quality'].upper()}")

    # Summary
    output.append(f"\n📋 Summary: {review['summary']}")

    # Issues
    if review["issues"]:
        output.append("\n🔍 Issues Found:")
        for i, issue in enumerate(review["issues"], 1):
            severity_icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(issue["severity"], "⚪")
            line_info = f" (line {issue['line']})" if issue.get("line") else ""
            output.append(f"  {i}. {severity_icon} [{issue['severity'].upper()}]{line_info}")
            output.append(f"     {issue['description']}")
            if issue.get("suggestion"):
                output.append(f"     💡 Suggestion: {issue['suggestion']}")
    else:
        output.append("\n✨ No issues found!")

    # Improvements
    if review["improvements"]:
        output.append("\n💡 Improvement Suggestions:")
        for improvement in review["improvements"]:
            output.append(f"  • {improvement}")

    return "\n".join(output)


def main():
    print("=" * 50)
    print("Mistral AI Code Review Bot")
    print("Showcasing: Codestral + Function Calling")
    print("=" * 50)

    # Check API key
    if not os.getenv("MISTRAL_API_KEY"):
        print("\nError: MISTRAL_API_KEY not found")
        print("Get your API key from https://console.mistral.ai/")
        sys.exit(1)

    # Get file to review
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        print("\nUsage: python main.py <code_file>")
        print("Example: python main.py app.py")
        print("\nRunning demo review...")
        demo_review()
        return

    try:
        code, language = load_code(file_path)
        print(f"\nReviewing: {file_path}")
        print(f"Language: {language}")
        print(f"Lines: {len(code.splitlines())}")
        print("-" * 50)

        print("\nCodestral is analyzing your code...")
        review = review_code(code, language, file_path)

        formatted = format_review(review)
        print(formatted)

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during review: {e}")
        sys.exit(1)


def demo_review():
    """Run a demo review on sample code"""
    sample_code = '''
def calculate_average(numbers):
    total = 0
    for n in numbers:
        total = total + n
    average = total / len(numbers)
    return average

# Usage
nums = [1, 2, 3, 4, 5]
print(calculate_average(nums))
print(calculate_average([]))  # This will crash!
'''

    print("\nDemo: Reviewing sample Python code")
    print("-" * 50)
    print(sample_code)
    print("-" * 50)

    print("\nCodestral is analyzing...")

    try:
        review = review_code(sample_code, "Python", "demo.py")
        formatted = format_review(review)
        print(formatted)
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
