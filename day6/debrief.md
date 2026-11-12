# Debrief: Fix the Broken Web Server

## 1. Which step helped most, and which did I skip?
Most helpful: reading the evidence. In scenario 1 the error log said "Permission denied", in scenario 2 the "Server: Apache" header and ss -tlnp showed the wrong program on port 80, and in scenario 3 nginx -t named the file and line.
What I skipped or rushed: forming my own guess before getting help. In scenario 1 my first guess (wrong port) did not fit the evidence, and in scenario 3 I only looked at the line nginx named, not the setting above it.

## 2. Why each fix works, and what a sloppy fix would do
- Scenario 1: chmod 755 lets everyone (including www-data) read and enter the folder, but only root can write. chmod 777 would let any user change the website (the checker calls it UNSAFE). chown www-data would let the web server edit its own files, which is risky if it gets hacked.
- Scenario 2: stopping Apache with service apache2 stop frees port 80 properly, then nginx can start. kill -9 on random processes skips a clean shutdown, and reinstalling nginx would not help because the port would still be taken.
- Scenario 3: putting back the missing ; fixes the real mistake, and nginx -t proves it before starting. Reinstalling nginx or rewriting the config would hide what went wrong and could lose other settings.
- Bonus: giving web2 its own Mac port keeps both sites working. Stopping or removing lab would "fix" web2 by breaking the other site.

## 3. Why do systemctl and journalctl not work in this container?
They need systemd as process 1 (PID 1). lab.sh starts the container with "sleep infinity", so PID 1 is sleep, not systemd. That is why I used service (the older init.d scripts) and read log files like /var/log/nginx/error.log directly.

## 4. What do the two numbers in -p 8080:80 mean?
-p HOST:CONTAINER. 8080 is the port on my Mac (what I type in the browser). 80 is the port inside the container (where nginx listens). Every container has its own private port 80, but my Mac has only one port 8080, so two containers cannot both use 8080.

## 5. Where did AI help, and where did it mislead me?
Helped: explaining what 403, "Server: Apache", error 98 and ss -tlnp mean; noticing that scenario 2 had only half set up, and suggesting ./lab.sh setup to refresh the lab image.
Misled or needed correcting: in scenario 3 it first pointed me at lines 36-41, which were only comments; the real mistake was line 22. Lesson: check the evidence myself and never run a command I cannot explain.
