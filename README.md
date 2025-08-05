# Lochat
A simple social network project used for learning `Socket Shannel`, `Redis` and `Redis Queue` in `Django` project. This project can be used for chatting in realtime and target to **Vietnamese** users.
---
### Main features
- Login, registry and authorization users
- Custom profile informations
- Search other users and start a conversation with them
- Realtime chatting
- Create group conversation and group chatting
- Send file and media file to others
---
### Technologies used
- Backend: Python with Django, Redis, Socket Channel, JWT, AWS S3 
- Frontend:
- Database: Postgres
- Deployment: Docker, AWS
- Architecture: MVC architecture
- Pattern: Singleton, prototype, builder, observer, service-repository
---
### Installation
> ***Step 1: Clone repository***
- Open cmd and run this command `git clone https://github.com/tuanhao2003/lochat-server.git`
- Then `cd lochat-server` 
> ***Step 2: Run docker desktop***
- Open `Docker desktop`, if you don't have it, please install at `https://docs.docker.com/desktop/setup/install/windows-install/` 
> ***Step 3: Run project***
- Open cmd and run `docker-compose up -d --build`
### Structure of the project
```
lochat-server
├── .github/
├── app/
│   ├── consumers/
│   ├── controllers/
│   ├── entities/
│   ├── enums/
│   ├── mapping/
│   ├── middlewares/
│   ├── migrations/
│   ├── repositories/
│   ├── services/
│   ├── utils/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── ws_urls.py
├── compositions/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── fe-requirements.txt
├── LICENSE
├── manage.py
├── README.md
├── requirements.txt
```
