#!/bin/bash

cd ..

docker rmi enct-gpu:latest
docker build -t enct-gpu:latest -f ./docker/Dockerfile-gpu .
