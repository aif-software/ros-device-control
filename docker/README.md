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

## Docker setup for orin/nano/pi

To build the container for pi, either:

```
cd docker/pi
docker compose build
docker compose up
```

or from the root folder of the repository:

```
docker compose -f docker/pi/lidar.yml build
docker compose -f docker/pi/lidar.yml up
```

Containers for nano and pi are more lean, and contain only drivers for the sensors they're supposed to run. The orin container has foxglove bridge and rosbag recording capabilities as well.
