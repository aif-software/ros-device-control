# Kuksa setup

Create network for the kuksa components

```
docker network create kuksa-docker
```

Create .env file for controlling the execution
and fill the following in the file

```
FLIR_1_PATH=<Path of flir 1 (left?)>
FLIR_2_PATH=<Path of flir 2 (right?)>
HOST_BAG_PATH=<The path for ros2 bags>
DOCKER_DUMPFILE_PATH=<Path of the dumpfile>
```

Run the

```
docker compose -f ros-compose.yaml up
```
