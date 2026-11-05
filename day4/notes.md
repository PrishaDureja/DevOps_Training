# Practical: AI-written unit file, explained before use

Rule: never run a command you cannot explain.

## What a unit file is
A text file of instructions for systemd: what to run, as which user, when to start, and what to do if it crashes.
- [Unit]: what the service is and when it starts
- [Service]: how to run it
- [Install]: whether it starts at boot (used by systemctl enable)
My own unit files go in /etc/systemd/system/.

## What I asked the AI
A unit file for a script that logs the time every 10 seconds, running as a low-privilege user, restarting on crash, starting at boot.

## Line by line
- Description: name shown in systemctl status
- After=network.target: start after networking is ready
- Type=simple: the ExecStart command is the service and stays in the foreground
- ExecStart=/usr/local/bin/heartbeat.sh: the program to run (full path)
- User=heartbeat: a dedicated system user that only this service uses and cannot log in
- Restart=on-failure: restart if it crashes, not if I stop it
- RestartSec=5: wait 5 seconds before restarting
- WantedBy=multi-user.target: start at normal boot when enabled
- Output goes to the journal: journalctl -u heartbeat

## Problem I caught in the AI's answer
The AI used User=nobody. systemd-analyze verify warned: "Special user nobody configured, this is not safe!"
nobody is shared by other programs, so it is not a safe choice for a service.
Fix: useradd --system --no-create-home --shell /usr/sbin/nologin heartbeat, changed the line to User=heartbeat, then verify printed nothing.
Lesson: always check AI output before using it.

## Tests and results
1. Ran the script by hand first: printed every 10 seconds.
2. systemd-analyze verify: no warnings after the fix.
3. ps showed USER heartbeat, so the service is not running as root.
4. kill -9: PID changed from 345 to 354, so systemd restarted it (Restart=on-failure, RestartSec=5).
5. systemctl stop: stayed inactive, so a deliberate stop is respected.
