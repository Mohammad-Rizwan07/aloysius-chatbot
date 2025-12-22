import os
import re

def safe_filename(url: str) -> str:
    name = url.replace("https://", "").replace("http://", "")
    name = re.sub(r"[^\w\-]", "_", name)
    return name[:150] + ".md"

def save_markdown(content: str, url: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    filename = safe_filename(url)
    path = os.path.join(output_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
