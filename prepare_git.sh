#!/bin/bash

# AntiGravity Git Setup Script
# ----------------------------

echo "🚀 Preparing project for GitHub..."

# 1. Initialize Git if needed
if [ ! -d ".git" ]; then
    echo "📦 Initializing existing directory as Git repository..."
    git init -b main
else
    echo "✅ Git repository already initialized."
fi

# 2. Add files (respecting .gitignore)
echo "➕ Adding files..."
git add .

# 3. Status Check
echo "📊 Staging status:"
git status

# 4. Commit
echo ""
read -p "📝 Do you want to commit these changes? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter commit message (default: 'v1.1 Release'): " commit_msg
    commit_msg=${commit_msg:-"v1.1 Release"}
    git commit -m "$commit_msg"
    echo "✅ Committed."
else
    echo "❌ Commit aborted."
    exit 0
fi

# 5. Remote Setup
echo ""
echo "🌍 To push to GitHub, you need to link a remote repository."
echo "   If you haven't created one, go to https://github.com/new and create an empty repository."
echo ""
read -p "Do you have a GitHub repository URL to add now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter Remote URL (e.g., https://github.com/user/repo.git): " remote_url
    if [ -n "$remote_url" ]; then
        # Remove existing origin if exists
        git remote remove origin 2>/dev/null
        git remote add origin "$remote_url"
        echo "🔗 Remote 'origin' added."
        
        echo "🚀 Pushing to main..."
        git push -u origin main
    else
        echo "❌ No URL provided."
    fi
fi

echo ""
echo "🎉 Done! You can always push later with: git push origin main"
