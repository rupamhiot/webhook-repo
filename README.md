
*******************
## Introduction
Now webhook application is composed of three service layers. Web layer, Backend layer, and database layer. Nginx served as the web layer, python flask served as the backend, and mondgodb as db layer. 
All are comsed as one service with docker compose yml file. Now docker-compose up -d will run three docker containers.
## Setup

* run docker compose  to start the application
```bash
docker compose up -d
```
* To stop the the application
```
docker compose down
```

* The endpoint is at:

```bash
POST http://127.0.0.1:8081/webhook/receiver
```

* The UI endpoint is:


```bash
http://127.0.0.1:8081/webhook/ui
```


*******************
