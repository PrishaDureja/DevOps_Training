# Lab: nginx as a systemd service with a custom unit file

## What I built
A lab machine where systemd is the first process (PID 1), with nginx installed from apt and a second, custom nginx service that I defined myself in /etc/systemd/system/nginx-lab.service.

## Commands I practised
- systemctl start / stop / restart / reload nginx
- systemctl enable / disable nginx (start at boot or not)
- systemctl is-active / is-enabled nginx
- systemctl status nginx --no-pager
- systemctl cat nginx (read the packaged unit file)
- systemctl daemon-reload (after creating or editing a unit file)
- journalctl -u nginx-lab -n 25 --no-pager (read the service log)

## My unit file, line by line
- ExecStartPre: runs `nginx -t` first, so a broken config stops the start.
- ExecStart with `daemon off`: keeps nginx in the foreground so systemd can watch it (Type=simple).
- ExecReload: sends HUP so nginx re-reads its config without stopping.
- Restart=on-failure and RestartSec=3: systemd restarts it 3 seconds after a crash.
- WantedBy=multi-user.target: starts at boot when enabled.

## Difference from the packaged nginx unit
The packaged one uses Type=forking, a PID file, daemon on and a custom ExecStop. Mine uses Type=simple and daemon off, which is simpler.

## Tests and what I saw
1. kill -9 on the main process: PID changed 1125 to 1148 and the page kept working.
2. Added a junk line to nginx.conf: ExecStartPre failed (status=1/FAILURE) and systemd retried every 3 seconds.
3. Removed the junk line: the next retry started the service.
4. docker restart: the service came back by itself because it is enabled.

## Lessons
- Run daemon-reload after every unit file change.
- Only one program can listen on port 80, so I stopped the packaged nginx first.
- journalctl shows the exact line of a config error.
