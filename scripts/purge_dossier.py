import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXCLUDE_DIRS = {'.git', '.venv', 'node_modules', 'whisper_cache', '__pycache__', '.pytest_cache'}
EXCLUDE_EXTS = {'.png', '.jpg', '.jpeg', '.webp', '.mp4', '.mp3', '.wav', '.ico', '.pdf', '.bin', '.onnx', '.tflite'}

def purge_dossier():
    count = 0
    file_count = 0
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in EXCLUDE_EXTS:
                continue
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as fh:
                    content = fh.read()
            except Exception:
                continue

            if 'article' in content.lower():
                # Replace variations
                new_content = re.sub(r'\bDOSSIER\b', 'ARTICLE', content)
                new_content = re.sub(r'\bDossier\b', 'Article', new_content)
                new_content = re.sub(r'\bdossiers\b', 'articles', new_content)
                new_content = re.sub(r'\bDossiers\b', 'Articles', new_content)
                new_content = re.sub(r'\bdossier\b', 'article', new_content)

                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as fh:
                        fh.write(new_content)
                    matches = len(re.findall(r'article', content, flags=re.IGNORECASE))
                    count += matches
                    file_count += 1
                    print(f"Purged {matches} instances in {os.path.relpath(path, ROOT)}")

    print(f"\nTotal purged: {count} instances across {file_count} files.")

if __name__ == '__main__':
    purge_dossier()
