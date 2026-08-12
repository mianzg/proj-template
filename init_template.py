"""Run once after creating a new repo from this template, then delete this file.

    python init_template.py

Prompts for a project name and repo slug, then replaces the placeholder
tokens (<Project Name>, research-project, research-project-template)
across README.md, environment.yml, and .env.example. Everything else in
the template is left as-is — check README.md's TODOs for the rest.
"""

import re
import sys
from pathlib import Path

FILES_TO_PATCH = ["README.md", "environment.yml", ".env.example"]


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip().lower()).strip("-")
    return slug or "research-project"


def main():
    root = Path(__file__).resolve().parent

    project_name = input("Project name (human-readable, e.g. 'Coral Bleaching Study'): ").strip()
    if not project_name:
        print("No name entered, aborting.")
        sys.exit(1)

    slug = slugify(project_name)
    confirm = input(f"Environment/package slug will be '{slug}' — press enter to accept, "
                     f"or type a different slug: ").strip()
    if confirm:
        slug = slugify(confirm)

    replacements = {
        "<Project Name>": project_name,
        "research-project-template": slug,
        "research-project": slug,
    }

    for filename in FILES_TO_PATCH:
        path = root / filename
        if not path.exists():
            continue
        text = path.read_text()
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text)
        print(f"Updated {filename}")

    print(
        "\nDone. Remaining manual steps:\n"
        "  - Fill in <you>, <org-or-user>, <repo>, and status/date fields in README.md\n"
        "  - Rename the conda environment if you already created one: "
        "conda env create -f environment.yml\n"
        "  - Delete this script (init_template.py) once you're happy with the result\n"
    )


if __name__ == "__main__":
    main()
