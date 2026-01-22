from pathlib import Path
from datetime import datetime
import subprocess

CHANGELOG = Path("CHANGELOG.md")

CATEGORIES = {
    "feat": "Features",
    "fix": "Fixes",
    "docs": "Documentation",
    "chore": "Chores",
    "refactor": "Refactoring",
    "test": "Testing",
}

def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()

def get_commits():
    # Gets commit messages from git log
    raw = run(["git", "log", "--pretty=format:%s"])
    return [line.strip() for line in raw.splitlines() if line.strip()]

def categorize(commits):
    grouped = {title: [] for title in CATEGORIES.values()}
    grouped["Other"] = []

    for msg in commits:
        prefix = msg.split(":")[0].lower().strip()
        if prefix in CATEGORIES:
            grouped[CATEGORIES[prefix]].append(msg)
        else:
            grouped["Other"].append(msg)

    return grouped

def build_markdown(grouped):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    md = f"# Changelog\n\n## {today}\n\n"

    for section, items in grouped.items():
        if not items:
            continue
        md += f"### {section}\n"
        for i in items[:30]:  # limit to keep it short
            md += f"- {i}\n"
        md += "\n"

    return md

def main():
    commits = get_commits()
    grouped = categorize(commits)
    new_content = build_markdown(grouped)

    if CHANGELOG.exists():
        old = CHANGELOG.read_text(encoding="utf-8")
        # Keep previous changelog below the new section
        if old.startswith("# Changelog"):
            old = "\n".join(old.splitlines()[1:]).lstrip()
        CHANGELOG.write_text(new_content + old, encoding="utf-8")
    else:
        CHANGELOG.write_text(new_content, encoding="utf-8")

    print("CHANGELOG.md updated.")

if __name__ == "__main__":
    main()
