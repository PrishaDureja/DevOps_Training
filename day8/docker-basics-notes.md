# Day 8 (Task 3): Docker basic commands

## Command syntax
docker <object> <action> [options] <name>
Shortcuts: docker ps = docker container ls, docker images = docker image ls

## Listing
- docker ps : running containers
- docker ps -a : all containers, including stopped (STATUS shows Exited (code))
- docker images : all images and their sizes
- docker network ls / docker volume ls : networks / volumes

What I saw with docker images:
- app1-image and app2-image: 140MB = python:3.12-slim base (119MB) + my libraries (20.6MB)
- postgres:16: 468MB, hello-world: 10.1kB

## Processes and resources
- docker top NAME : processes inside a container
  - app1 had 1 process: python app.py (the CMD from my Dockerfile)
  - db had 6 processes: the main postgres plus 5 helpers (their PPID = the main postgres PID)
- docker stats --no-stream : CPU, memory, network and number of processes (PIDS) per container, printed once
  - app1/app2 used about 22MB RAM each, db about 20MB, db had 6 PIDS

## Inspecting and debugging
- docker logs NAME : the container's messages
- docker inspect NAME : all details as JSON (IP, ports, env variables, volumes)
  - docker inspect app1 | grep IPAddress showed 172.18.0.3 on the labnet network
- docker history IMAGE : the layers of an image (read bottom to top)
  - The bottom rows were the python base image; the top rows were my Dockerfile steps
  - pip install layer was 20.6MB; WORKDIR, EXPOSE, CMD layers were 0B (settings only)
- docker exec -it NAME bash : open a shell inside a running container, exit to leave
  - Inside app1, ls showed app.py and requirements.txt (the files my Dockerfile copied)

## Building an image from scratch: mysite
Files: index.html (my web page) and this Dockerfile:
  FROM nginx:alpine
  COPY index.html /usr/share/nginx/html/index.html
  EXPOSE 80
- FROM: start from the official nginx image (alpine = very small version)
- COPY: put my page in nginx's web folder
- EXPOSE: documents that nginx uses port 80
- No CMD needed: the nginx image already has one that starts the web server

docker build -t mysite:v1 .
- -t NAME:TAG names the image; the tag is a version label (default: latest)
- . means the Dockerfile is in the current folder

docker run -d --name mysite -p 8083:80 mysite:v1
- curl http://localhost:8083 showed my page

## Version 2
- Added a line to index.html
- docker build -t mysite:v2 .
- docker rm -f mysite (stop and delete the old container)
- docker run -d --name mysite -p 8083:80 mysite:v2
- The page now showed "Version 2"
- docker images mysite showed both v1 and v2 (69.1MB each, mostly nginx)

Lesson: editing a file does not change a running container.
Rebuild the image, then run a new container from it.

## Dockerfile instructions
- FROM : base image
- WORKDIR : working folder inside the image
- COPY : copy files from my laptop into the image
- RUN : run a command at BUILD time (e.g. install libraries)
- EXPOSE : document the port
- CMD : the command that runs every time a container STARTS

## docker run options
- -d background, --name name, -p HOST:CONTAINER, -e KEY=VALUE,
  -v VOLUME:PATH, --network NET, -it interactive shell, --rm delete on stop

## Start / stop / remove
- docker start / stop / restart NAME
- docker rm NAME (stopped container), docker rm -f NAME (stop and delete)
- docker rmi IMAGE (delete an image)

## Things I learned
- A custom image = a base image + my own layers on top
- Tags (v1, v2) are versions of the same image
- Stopped containers stay stopped; docker start brings them back
- Exit code 0 = clean stop; 137 = force-stopped (128 + 9, SIGKILL)
- Containers show UTC time; India is UTC + 5:30
