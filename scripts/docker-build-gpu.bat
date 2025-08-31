cd ..
set IMG=enct-gpu:latest
set DOCKERFILE=./docker/Dockerfile-gpu

docker rmi %IMG%
docker build -t %IMG% -f %DOCKERFILE% .
pause