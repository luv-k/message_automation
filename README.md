# Message Automation

Automates sending messages using the script `Message automation.py`.

**Preview:**

![Interface](interface.png)

**Files:**
- `Message automation.py` — main script that automates messaging.
- `interface.png` — screenshot of the interface used in this project.

## Requirements
- Python 3.8+
- Any additional Python packages used by `Message automation.py` (see the top of the script for imports).

## Usage
1. Open a terminal in this folder.
2. (Optional) Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install any dependencies (if needed):

```powershell
pip install -r requirements.txt
```

4. Run the script:

```powershell
python "Message automation.py"
```

## Publish to GitHub
1. Initialize and commit locally (already done if you followed steps below):

```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
```

2a. Create a GitHub repo and push using GitHub CLI:

```powershell
gh repo create <your-username>/<repo-name> --public --source=. --remote=origin --push
```

2b. Or create a repo on GitHub.com, then add remote and push:

```powershell
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

Replace `<your-username>` and `<repo-name>` with your GitHub details.

---

If you'd like, I can create the local git commit now and attempt to publish using the GitHub CLI if it's available. Want me to do that? 
