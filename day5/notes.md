# Lab: fix 3 broken services

## My troubleshooting method
1. Look: systemctl status <name> --no-pager -l
2. Read the log: journalctl -u <name> -n 20 --no-pager
3. Read the unit file: systemctl cat <name>
4. Investigate the clue: ls -l (permissions), ss -tlnp (ports), systemd-analyze verify (unit file)
5. Fix, daemon-reload if I edited a unit file, restart, prove it works

## 1. reporter: permission issue
- Symptom: activating (auto-restart), status=1/FAILURE, restart loop
- Log: line 4: /var/log/reporter/report.log: Permission denied
- Cause: service runs as User=reporter, but /var/log/reporter was drwxr-xr-x root root, so reporter could not write
- Fix: chown reporter:reporter /var/log/reporter
- Why not chmod 777: that lets every user write there, which is a security hole
- Proof: active, and report lines every 10 seconds in report.log
- No daemon-reload needed: I changed folder ownership, not the unit file

## 2. shop-web: port conflict
- Symptom: auto-restart loop, but ExecStartPre (nginx -t) passed, so the config syntax was fine
- Log: bind() to 0.0.0.0:80 failed (98: Unknown error), still could not bind()
- Error 98 means "address already in use" (this minimal image does not have the text for the code)
- The restart counter had reached 7362 because I left it broken overnight
- Cause: ss -tlnp showed nginx PIDs 56 and 59 on :80, and nginx-lab's MainPID was 56
- Fix: moved shop-web to port 8082 with sed, tested with nginx -t, restarted
- Why move shop-web: nginx-lab was working, so never break a working service to fix a new one
- Proof: curl localhost:8082 shows the shop page, curl localhost still shows nginx-lab, ss shows :80 and :8082
- No daemon-reload needed: I changed nginx's config, not the unit file

## 3. greeter: bad config
- Symptom: Loaded: bad-setting, inactive (dead), so systemd refused to even try
- Log: greeter.service:7: Unknown key name 'ExecStrat' ... Service has no ExecStart= ... Refusing.
- systemd-analyze verify showed the same error, and grep -n showed line 7: ExecStrat
- Cause: typo in the unit file (ExecStrat instead of ExecStart)
- Fix: sed to correct it, verify printed nothing, daemon-reload, start
- Proof: active (running), hello lines every 15 seconds in journalctl

## Final checks
- Enabled all three only after they worked
- All 5 services (reporter, shop-web, greeter, nginx-lab, heartbeat) active and enabled
- docker restart: all 5 came back active by themselves

## Lessons
- Read the log before guessing: it named every problem
- Loaded: bad-setting means the unit file itself is wrong; loaded but failing means the problem is elsewhere
- daemon-reload is only needed after editing a unit file
- Fix the smallest thing (chown, not chmod 777; move the new service, not the working one)
- Fix broken services quickly: a restart loop keeps retrying forever
