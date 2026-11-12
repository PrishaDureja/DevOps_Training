# Lab: Fix the Broken Web Server - incident notes

## Scenario 1
Scenario: 1 - "Users are getting an error page instead of the website."
What I checked: curl -i localhost (403 Forbidden), service nginx status (running), ps aux | grep nginx (workers run as www-data), tail -n 20 /var/log/nginx/error.log, ls -ld /var/www/html
Root cause: /var/www/html was drwx------ root root, so the www-data worker could not enter the folder. Log: "/var/www/html/index.html" is forbidden (13: Permission denied)
Fix: chmod 755 /var/www/html (owner rwx, everyone else read and enter only, no write)
Prevention: keep web folders at 755 and files at 644; check permissions after manual changes; never use 777
AI check: my first guess was "wrong port". But nginx answered with 403, so it was listening on the right port. A wrong port would give "connection refused". The log line "Permission denied" pointed to folder permissions.

## Scenario 2
Scenario: 2 - "The website is showing the wrong page."
What I checked: curl -i localhost (Server: Apache, "Index of /"), service nginx status (not running), ps aux | grep nginx, ss -tlnp (apache2 pid 604 on :80)
Root cause: Apache was installed and started on port 80, and nginx was stopped. Only one program can use a port, so Apache answered with a file list instead of the nginx site. Proof: curl showed "Server: Apache/2.4.58" and ss showed apache2 on 0.0.0.0:80
Fix: service apache2 stop, then service nginx start
Prevention: don't install a second web server on the same port; check ss -tlnp after installing software; remove apache2 if it isn't needed
Note: the first try at this scenario only half worked, with nothing listening. The lab's saved image had an old package list, so installing Apache failed silently. Running ./lab.sh setup again refreshed it.
AI check: I needed help reading the clues. The key was the "Server:" line in curl and ss -tlnp, which showed the wrong program on port 80.

## Scenario 3
Scenario: 3 - "The website is down. Someone edited the config earlier today."
What I checked: curl -i localhost (couldn't connect), service nginx status (not running), ss -tlnp (nothing on :80), tail -n 20 /var/log/nginx/error.log, nginx -t, cat -n + sed -n to view lines 36-41, grep -n "listen"
Root cause: line 22 of /etc/nginx/sites-available/default was "listen 80 default_server" with the ending ";" removed, so nginx refused to start. Log: [emerg] invalid parameter "root" in /etc/nginx/sites-enabled/default:40. nginx reported line 40 because it skips comments and blank lines, and only noticed the problem when it reached "root".
Fix: sed -i 's/listen 80 default_server$/listen 80 default_server;/' /etc/nginx/sites-available/default, then nginx -t (test is successful), then service nginx start
Prevention: always run nginx -t after editing a config and before restarting; keep a backup copy of a config before editing it
AI check: I first looked only at lines 36-41, which were comments. The real mistake was the last real setting above line 40 (line 22). The error line number shows where nginx noticed the problem, not always where it is.

## Bonus
Scenario: Bonus - start a second web server: docker run -d --name web2 -p 8080:80 nginx
What I checked: the error message, docker ps, docker port lab
Root cause: "Bind for 0.0.0.0:8080 failed: port is already allocated". The lab container already used Mac port 8080 (docker port lab: 80/tcp -> 0.0.0.0:8080). Only one container can use a given Mac port.
Fix: docker rm web2 (the failed run still created the container), then docker run -d --name web2 -p 8082:80 nginx. curl -I localhost:8082 gave 200 OK, Server: nginx/1.31.8
Prevention: check docker ps for used ports before choosing one; give each container its own host port
AI check: my guess matched. A typo (an extra ' at the end) left the shell at "quote>"; Ctrl+C cancelled it.
