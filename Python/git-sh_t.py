"""
Script Name: git-sh_t.py
Description: This script searches the current directory for Git repositories.
             If a repository is found, it performs a 'git pull' to update it.
             After completion, it lists the directories that were updated.
Author: VarthDader (https://github.com/varthdader) 
"""
import os
import subprocess

def is_git_repo(path):
    return os.path.isdir(os.path.join(path, '.git'))

def update_git_repos(base_dir):
    updated_dirs = []

    for root, dirs, files in os.walk(base_dir):
        if is_git_repo(root):
            print(f"Updating repository in: {root}")
            try:
                subprocess.run(['git', 'pull'], cwd=root, check=True)
                updated_dirs.append(root)
            except subprocess.CalledProcessError:
                print(f"Failed to update repository in: {root}")

    return updated_dirs

if __name__ == "__main__":
    current_directory = os.getcwd()
    updated_repositories = update_git_repos(current_directory)

    if updated_repositories:
        print("\nUpdated directories:")
        for directory in updated_repositories:
            print(directory)
    else:
        print("No Git repositories found or updated.")
