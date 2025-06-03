"""
collects various data sources from github to use with markdown files for RAG
"""

import os
import base64
import time
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()

# configuration
OUTPUT_DIR = "."
DELAY = 0.1
REPO_DELAY = 5
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

SOURCES = {
    "manual": {"repo": "opengovfoundation/hr-manual", "paths": ["markdown/"]},
    "docs": {"repo": "basecamp/kamal-site", "paths": ["docs/"]},
    "handbook": {"repo": "basecamp/handbook", "paths": [""]},
}


def get_repo_contents(repo, path=""):
    """get contents of a repository directory"""
    url = f"https://api.github.com/repos/{repo}/contents/{path}"

    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("most likely rate limited")
            return []
    except Exception as e:
        print(f"error: {e}")
        return []


def download_file(repo, file_path, local_path):
    """download a single file from github"""
    url = f"https://api.github.com/repos/{repo}/contents/{file_path}"

    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            file_info = response.json()

            if file_info.get("type") == "file" and file_info.get("content"):
                # decode content
                content = base64.b64decode(file_info["content"]).decode("utf-8")

                # create directory
                os.makedirs(os.path.dirname(local_path), exist_ok=True)

                # save file
                with open(local_path, "w", encoding="utf-8") as f:
                    f.write(content)

                print(f"downloaded: {file_path}")
                return True
    except Exception as e:
        print(f"failed: {file_path}")

    return False


def find_markdown_files(repo, path="", max_depth=3):
    """find all markdown files in a repository path"""
    if max_depth <= 0:
        return []

    markdown_files = []
    contents = get_repo_contents(repo, path)

    print(f"found {len(contents)} items in {repo}/{path}")

    time.sleep(DELAY)

    for item in contents:
        if item["type"] == "file":
            if item["name"].endswith((".md", ".markdown")):
                markdown_files.append(item["path"])
        elif item["type"] == "dir":
            # search subdirectories
            sub_files = find_markdown_files(repo, item["path"], max_depth - 1)
            markdown_files.extend(sub_files)

    return markdown_files


def main():
    print("collecting markdown files... ")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_files = 0

    for i, (source_name, config) in enumerate(SOURCES.items()):
        if i > 0:
            print(f"waiting {REPO_DELAY}s...")
            time.sleep(REPO_DELAY)

        print(f"processing {source_name}")

        source_dir = os.path.join(OUTPUT_DIR, source_name)
        os.makedirs(source_dir, exist_ok=True)

        repo = config["repo"]
        files_collected = 0

        for path in config["paths"]:
            print(f"searching {repo}/{path}")

            markdown_files = find_markdown_files(repo, path)
            print(f"found {len(markdown_files)} files")

            for file_path in markdown_files:
                # create local filename
                local_filename = file_path.replace("/", "_")
                local_path = os.path.join(source_dir, local_filename)

                if download_file(repo, file_path, local_path):
                    files_collected += 1

                time.sleep(DELAY)

        total_files += files_collected
        print(f"collected {files_collected} files")

    print(f"\ndone! {total_files} files saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    # change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    main()
