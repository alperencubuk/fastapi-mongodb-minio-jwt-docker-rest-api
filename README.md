# FastAPI MongoDB MinIO JWT Docker REST API

### Summary:

This API provides file upload/download operations on cloud storage. Includes local MinIO storage.
But also supports Google Cloud Storage and AWS S3 with HMAC (access/secret) keys authentication.

### Tech Stack:

**[FastAPI](https://fastapi.tiangolo.com/)** web framework for building REST API  
**[MongoDB](https://www.mongodb.com/)** for database  
**[MinIO](https://min.io/)** for cloud storage  
**[JWT](https://jwt.io/)** for authentication  
**[Docker](https://docs.docker.com/)** for containerization  
**[Docker Compose](https://docs.docker.com/compose/)** for defining and running multi-container

---

### Requirements:

```
docker
docker-compose
```

### How to Run:

```
docker-compose up --build
```

### Docs:

```
localhost:8000/docs
```

### Endpoints:

```http request
POST  /auth/token                  # get token
POST  /auth/refresh                # refresh token

GET   /files                       # download file
POST  /files                       # upload file

GET   /storages                    # get storage list
POST  /storages                    # add storage
GET   /storages/{storage_id}       # get storage
PATCH /storages/{storage_id}       # update storage

GET   /users                       # get user
POST  /users                       # add user
PATCH /users                       # update user
GET   /users/username/{username}   # check username

GET   /users/{username}            # get user (admin)
PATCH /users/{username}            # update user (admin)

GET   /                            # check health
```

---

**Alperen Cubuk**