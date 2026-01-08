Python

import flask

import os 

import dotenv

import redis

install redis-cli

redis-cli ping

port= 6379

python3 -m pip install requirements.txt

use .env
    .env.dev
    .env.stage
    .env.prod

python3 app.js

localhost:8000

docker build -t flaskapp:v1

docker run -p 3000:8000 --name flaskapp flaskapp:v1

# browser port =3000
# container port =8000

Now localhost:3000 ----> connection refused for redis #we were using local redis db which is install in our local but docker container is isolated one.
