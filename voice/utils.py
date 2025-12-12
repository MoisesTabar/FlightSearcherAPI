from pathlib import Path
from voice.constants.prompts import BASE_EXTRACTION_PROMPT


def build_extraction_prompt(template_content: str | None = None) -> str:
    base_prompt = BASE_EXTRACTION_PROMPT 
    
    if template_content:
        base_prompt += f"\n\nREFERENCE EXAMPLES FROM TEMPLATE:\n{template_content}"
    
    return base_prompt


def load_template(template_path: Path) -> str | None:
    if template_path.exists():
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()

    return None
