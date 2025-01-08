# Online store

The idea of an online store, which will have 2 services: one to receive data from the outside (adding and exchanging products, etc.), the second to work with products, categories, brands, etc.

## Installation

Create .env file

```bash
POSTGRES_DB=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...

SECRET_KEY=...
ALGORITHM=HS256
```
After creating the .env file, start the containers 
```bash
docker compose up
```
Go to the docs_backend_app container  
```bash
docker exec -it docs_backend_app bash
```
Activate migration
```bash
alembic upgrade head
```
Primary data is stitched into the migration


## Already implemented
REF for reference information\
JWT AUTH with access and refresh token

## Planned
Registration for users \
Categories models and API\
Brands models and API\
Products models and API
