# Day 8: Docker lab - two web apps and one shared database

## Task
1. Run two different web apps in two containers on two different ports
2. Run a database in its own container and connect both apps to it

## What I built
- app1 (Visitor Counter) on http://localhost:8081 - saves a visit and shows the total
- app2 (Visit Log) on http://localhost:8082 - saves a visit and lists the last 10 from both apps
- db (PostgreSQL 16) - one shared database, NOT published to the laptop
- All three on a private Docker network called labnet, so they find each other by name

## Commands and what they do
- docker network create labnet : private network, containers reach each other by name
- docker volume create db-data : storage that keeps the database data even if the container is deleted
- docker run -d --name db --network labnet -e POSTGRES_USER/PASSWORD/DB -v db-data:/var/lib/postgresql/data postgres:16 : start the database (no -p, so it is private)
- docker logs db : check it says "database system is ready to accept connections"
- docker build -t app1-image ./app1 : build an image from the Dockerfile
- docker run -d --name app1 --network labnet -p 8081:5000 -e DB_HOST=db ... app1-image : start app1, laptop port 8081 -> container port 5000
- docker run -d --name app2 --network labnet -p 8082:5000 -e DB_HOST=db ... app2-image : start app2 on 8082
- docker ps : list running containers and their ports
- curl http://localhost:8081 : visit app1 from the terminal
- docker exec -it db psql -U labuser -d appdb -c "SELECT * FROM visits;" : look inside the database

## Proof it works
- app1 count went 1, 2, 3 with each visit
- The visits table had rows from BOTH app1 and app2 (43 rows), so both apps share one database

## Key ideas
- Image = packaged app (recipe result); container = a running copy of an image
- Dockerfile = recipe: FROM, WORKDIR, COPY, RUN, EXPOSE, CMD
- -p HOST:CONTAINER - both apps use 5000 inside; only the laptop ports must differ (8081, 8082)
- The apps use DB_HOST=db: Docker's network lets containers find each other by name
- Database has no -p, so it is not reachable from outside - more secure
- Environment variables (-e) pass settings like the DB password into the container
- app2 built faster because Docker reused cached layers from app1

## Problems I hit
- docker ps said "permission denied": I was added to the docker group but had not restarted.
  Fix for now: newgrp docker. Permanent fix: restart the laptop.
- psql output opened in a pager showing (END): press q to exit
