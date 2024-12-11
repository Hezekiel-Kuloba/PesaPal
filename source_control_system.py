import os
import shutil
import hashlib
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import simpledialog  # Import this module


# Initialize repository
def init_repo():
    os.makedirs('.repo/objects', exist_ok=True)
    os.makedirs('.repo/refs', exist_ok=True)
    os.makedirs('.repo/stage', exist_ok=True)
    with open('.repo/HEAD', 'w') as f:
        f.write('refs/heads/master')
    messagebox.showinfo("Success", "Initialized empty repository in .repo/")

# Add file
def add_file():
    filename = filedialog.askopenfilename(title="Select a file to add")
    if filename:
        staged_file = os.path.join('.repo/stage', os.path.basename(filename))
        shutil.copy(filename, staged_file)
        messagebox.showinfo("Success", f"Added {filename} to staging area.")

# Commit changes

def commit():
    message = simpledialog.askstring("Commit Message", "Enter commit message:")  # Use simpledialog.askstring
    if not message:
        return

    commit_hash = hashlib.sha1(f"{time.time()}-{message}".encode()).hexdigest()
    os.makedirs(f".repo/objects/{commit_hash[:2]}", exist_ok=True)
    with open(f".repo/objects/{commit_hash[:2]}/{commit_hash[2:]}", 'w') as f:
        f.write(message)

    # Move staged files to the commit
    for filename in os.listdir('.repo/stage'):
        staged_path = os.path.join('.repo/stage', filename)
        commit_path = os.path.join(f".repo/objects/{commit_hash[:2]}", filename)
        shutil.move(staged_path, commit_path)

    messagebox.showinfo("Success", f"Committed: {commit_hash}\nMessage: {message}")


# View log
def log():
    logs = []
    for root, dirs, files in os.walk(".repo/objects"):
        for file in files:
            logs.append(f"Commit: {file}")
    messagebox.showinfo("Commit History", "\n".join(logs) if logs else "No commits found.")


def create_branch():
    branch_name = simpledialog.askstring("Branch Name", "Enter branch name:")  # Use simpledialog.askstring
    if branch_name:
        with open(f".repo/refs/{branch_name}", 'w') as f:
            f.write('HEAD')
        messagebox.showinfo("Success", f"Created branch {branch_name}")

# Merge branches
def merge():
    branch = simpledialog.askstring("Merge Branch", "Enter branch to merge:")
    if not branch or not os.path.exists(f".repo/refs/{branch}"):
        messagebox.showerror("Error", f"Branch {branch} does not exist.")
        return

    # Check for conflicts (simplified: any file in stage that differs from target branch files)
    conflicts = []
    for filename in os.listdir('.repo/stage'):
        target_file = os.path.join(f".repo/refs/{branch}", filename)
        staged_file = os.path.join('.repo/stage', filename)
        if os.path.exists(target_file):
            with open(target_file, 'rb') as f1, open(staged_file, 'rb') as f2:
                if f1.read() != f2.read():
                    conflicts.append(filename)

    if conflicts:
        messagebox.showerror("Conflict", f"Conflicting files: {', '.join(conflicts)}")
        return

    messagebox.showinfo("Merge", f"Merging {branch} into current branch.\nNo conflicts detected.")

# Clone repository
def clone_repo():
    dest = filedialog.askdirectory(title="Select Destination for Cloning")
    if dest:
        shutil.copytree('.repo', os.path.join(dest, '.repo'))
        messagebox.showinfo("Success", f"Cloned repository to {dest}")

# Tkinter UI
def build_ui():
    root = tk.Tk()
    root.title("Simple Git GUI")

    tk.Button(root, text="Initialize Repository", command=init_repo).pack(pady=10)
    tk.Button(root, text="Add File", command=add_file).pack(pady=10)
    tk.Button(root, text="Commit Changes", command=commit).pack(pady=10)
    tk.Button(root, text="View Commit Log", command=log).pack(pady=10)
    tk.Button(root, text="Create Branch", command=create_branch).pack(pady=10)
    tk.Button(root, text="Merge Branches", command=merge).pack(pady=10)
    tk.Button(root, text="Clone Repository", command=clone_repo).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    build_ui()
