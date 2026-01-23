#!/bin/bash

# AntiGravity Git Update Helper
# -----------------------------

# 1. Check for Git
if [ ! -d ".git" ]; then
    echo "❌ This is not a git repository. Run ./prepare_git.sh first."
    exit 1
fi

# 2. Status
echo "📊 Current Status:"
git status -s
echo ""

# 3. Confirm
read -p "Do you want to stage and commit ALL these changes? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Update aborted."
    exit 0
fi

# 4. Add & Commit
git add .
read -p "📝 Enter commit message (default: 'Small improvements'): " val
commit_msg=${val:-"Small improvements"}

git commit -m "$commit_msg"

# 5. Push
echo "🔄 Syncing with remote..."
git pull --rebase origin main
if [ $? -ne 0 ]; then
    echo "⚠️ Conflict detected or pull failed. Please resolve manually."
    exit 1
fi

echo "🚀 Pushing to remote..."
git push

echo "✅ Update complete!"
