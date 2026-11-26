# Day 7: Set up my Ubuntu work laptop

## Laptop
- Lenovo ThinkPad L14 Gen 1, Ubuntu 20.04.6 LTS, user: bigstep (has sudo)

## What I set up
1. Installed git and curl: sudo apt update, sudo apt install -y git curl (git 2.25.1)
2. Git identity: git config --global user.name / user.email (company email), core.editor nano
3. SSH key: ssh-keygen -t ed25519, added the .pub key to GitHub account prishadureja-dot, tested with ssh -T git@github.com
4. Cloned my training repo to ~/workspace/DevOps_Training
5. Installed Docker: sudo apt install -y docker.io, sudo systemctl enable --now docker
6. Added myself to the docker group: sudo usermod -aG docker $USER, newgrp docker
7. Tested Docker: docker run hello-world
8. Recreated daysave in /usr/local/bin (now pulls first, and reports if the push fails)

## Differences from my Mac setup
- This laptop IS Linux, so no ubuntu-up / ubuntu-down / ubuntu-save
- systemctl works directly (with sudo)
- Normal user ($), not root (#), so admin commands need sudo
- Git 2.25 names new branches master, so I use git checkout -b main after git init

## Lessons
- Placeholder text like your-email@example.com must be replaced with my real value
- Spaces matter: user.email"x" is not the same as user.email "x"
- In the terminal, copy and paste is Ctrl+Shift+C / Ctrl+Shift+V
