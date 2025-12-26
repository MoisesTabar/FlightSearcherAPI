from pathlib import Path


def build_prompt(base_prompt: str, template_content: str | None = None) -> str:
    if template_content:
        base_prompt += f"\n\nREFERENCE EXAMPLES FROM TEMPLATE:\n{template_content}"
    
    return base_prompt


def load_template(template_path: Path) -> str | None:
    if template_path.exists():
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()

    return None
