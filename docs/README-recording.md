# Guide to recording with the ros2 devices

This is a simple guide to recording with the ros2 devices on the car. This is still a work in progress project, and changes frequently but this is the current rough guideline to using and recording the devices.

## Setup and cabling

Currently we use ssh to connect to the devices remotely to control them. The devices can be used directly with a monitor and keyboard/mouse except for the Raspberry Pi, due to it having only micro hdmi port for video out.

### Orin

The Orin should always be connected to the SFP-port of the modem, as it will be receiving the most network traffic. In addition, plug the USB-C power cable to the Orin, the USB-C port does not matter which one is used.

### Nano

Plug the network and power cable to the Nano. In addition, attach the two FLIR cameras to it, with one camera being attached via the USB-A port, and one attached to the USB-C dock, with the dock then being plugged into the USB-C port of the Nano.

### Raspberry Pi

Plug the network and power cable to the Raspberry Pi.

### Modem

Plug the Orin to the SFP-port, and the other devices to the other ports. Additionally, plug the power cable to the modem. Make sure to regularly check the temperature of the SFP-port inside the modems control page, under the interfaces-tab. If the temperature ever exceeds 95° Celcius, the SFP-port will be disabled for 10 minutes, and the recording will fail. This temperature limit is not unreasonable, as under no load, the average temperature is 85°-90° Celcius.

## Connecting to the devices

Current addresses to connect to these devices:
m3s@192.168.88.250 Orin
m3s@192.168.88.248 Nano
m3spi@192.168.88.247 Pi

Inside each device, run their respective docker compose files inside the docker directory.

```bash
docker compose up
```

## Starting the recording

When each of the containers are up, detach from the one running on Orin, and go inside the container.

```bash
docker exec -it ros-multisense bash
```

Start the recording inside the container.

```bash
source install/setup.bash

ros2 bag record --max-bag-duration 10 --max-cache-size 20000000000 --compression-mode file --compression-format zstd --output bags/FILE_NAME --topics /lidar_points /flir_left/image_raw /flir_right/image_raw /aux/image_color /left/cost /left/depth /left/image_rect /right/image_rect /lidar_imu
```

This will start the recording, saving the files inside the bags/ directory. This can be stopped by pressing CTRL + C inside the container. The recording should _ALWAYS_ be stopped in this way, as if it is not stopped gracefully (for example, stopping the container without stopping the recording first) will lead into the recording being corrupted.
