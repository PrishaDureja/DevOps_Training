# Day 9: Docker Compose (Tasks 4 and 5)

## Task 4: What Docker Compose is
- Docker Compose lets me describe a whole multi-container setup in ONE file
  (docker-compose.yml) and start everything with ONE command.
- Each container in the file is called a service.
- The file is YAML: structure is shown with indentation (spaces only, never tabs).
- Compose does not replace Docker; it runs Docker for me from the file.
- Installed with: sudo apt install -y docker-compose-v2 (version 2.27.1)

## Normal Docker vs Docker Compose
| Normal Docker | Docker Compose |
|---|---|
| One long docker run per container | One file, one command |
| I create the network myself | Network created automatically (projectname_default) |
| I remember the start order | depends_on sets the order |
| Share a list of commands | Share one file |
| docker stop each container | docker compose down |
| Good for one container or quick tests | Good for apps with several containers |

## Compose file keywords
- services: the containers
- image: use a ready-made image
- build: build an image from a Dockerfile in that folder
- ports: "HOST:CONTAINER" (same as -p)
- environment: settings (same as -e)
- volumes: named volume (name:/path) or bind mount (./folder:/path)
- depends_on: start these services first
- command: override the image's start command
- volumes (top level): create named volumes

## Compose commands (run in the folder with docker-compose.yml)
- docker compose config : check the file and show what Compose understood
- docker compose up -d --build : build and start everything in the background
- docker compose ps : this project's containers
- docker compose logs SERVICE : one service's logs
- docker compose down : stop and DELETE containers and network (volumes kept)
- docker compose down -v : also delete volumes (deletes data)

## Task 5: Hypothetical scenario - college TechFest
- frontend: nginx:alpine on port 8090, shows the fest homepage (bind mount of ./frontend)
- api: my Flask app on port 8091, gives each student a registration number
- redis: redis:7-alpine, stores the registration counter, private (no ports),
  data saved to the named volume redis-data (appendonly yes = save every change)

## Demo results
- docker compose up -d --build created network compose-lab_default,
  volume compose-lab_redis-data, and started redis -> api -> frontend (depends_on order)
- Container names: compose-lab-api-1 = project-service-number
- curl localhost:8091 three times gave numbers 1, 2, 3
- curl localhost:8091/count showed the total
- docker compose logs api showed each GET request
- docker compose down removed all containers and the network
- docker compose up -d brought everything back, and the count was still there
  because the redis volume survived

## Key lessons
- Compose = the same Docker ideas (images, containers, ports, env, volumes,
  networks), written in one file instead of many commands
- Services find each other by service name (the api used REDIS_HOST=redis)
- Containers are temporary; volumes keep data
- Always check with docker compose config before running
