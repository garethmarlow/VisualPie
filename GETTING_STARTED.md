# 🚀 Quick Start: Get This Running in 5 Minutes

## Step 1: Create GitHub Repository (2 minutes)

1. Go to https://github.com/new
2. Repository name: `vinyl-visualizer`
3. Description: "Psychedelic music visualizer for Raspberry Pi"
4. Choose Public or Private
5. **Don't** check "Initialize with README"
6. Click "Create repository"
7. **Copy the repository URL** (looks like: `https://github.com/yourusername/vinyl-visualizer.git`)

## Step 2: Initialize Git & Push (1 minute)

Extract the archive and run:

```bash
tar xzf vinyl-visualizer.tar.gz
cd vinyl-visualizer
./init-git.sh
# Paste your GitHub repo URL when prompted
```

Done! Your code is now on GitHub.

## Step 3: Deploy to Raspberry Pi (2 minutes)

SSH to your Pi and run:

```bash
git clone https://github.com/yourusername/vinyl-visualizer.git
cd vinyl-visualizer
./deploy.sh
```

The script will:
- ✓ Install all dependencies
- ✓ Ask for your Icecast stream URL
- ✓ Offer to test the visualizer
- ✓ Set up auto-start service

**That's it!** Your visualizer is running.

## Making Changes

**On your dev machine:**
```bash
cd vinyl-visualizer
vi config.yaml              # Make changes
git add .
git commit -m "Changed color speed"
git push
```

**On your Pi:**
```bash
cd ~/vinyl-visualizer
git pull
sudo systemctl restart vinyl-visualizer
```

## Efficient Workflow Tip

Add to your Pi's `~/.bashrc`:

```bash
alias vv-update='cd ~/vinyl-visualizer && git pull && sudo systemctl restart vinyl-visualizer'
```

Then just type `vv-update` to deploy latest changes!

## Documentation

- **README.md** - Project overview
- **GIT_WORKFLOW.md** - Git commands reference
- **QUICKREF.md** - Command cheat sheet
- **DEPLOYMENT.md** - Detailed Pi setup guide

## Need Help?

```bash
# View logs
sudo journalctl -u vinyl-visualizer -f

# Test manually
./test.sh

# Check service status
sudo systemctl status vinyl-visualizer
```

Enjoy! 🎵✨
