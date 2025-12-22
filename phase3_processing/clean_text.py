import re

def clean_markdown(text: str) -> str:
    # Remove multiple newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove excessive whitespace
    text = re.sub(r"[ \t]+", " ", text)

    # Remove markdown navigation-like lines
    lines = [
        line for line in text.splitlines()
        if len(line.strip()) > 3
    ]

    return "\n".join(lines).strip()
