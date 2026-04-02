# Guide to recording with the ros2 devices

This is a simple guide to recording with the ros2 devices on the car. This is still a work in progress project, and changes frequently but this is the current rough guideline to using and recording the devices.

## Setup and cabling

Currently we use ssh to connect to the devices remotely to control them. The devices can be used directly with a monitor and keyboard/mouse except for the Raspberry Pi, due to it having only micro hdmi port for video out.

Attaching the sensors should be done carefully and ensured that the screws holding them down are tight. After attaching the sensors, you should drive for a while, and check again that the screws have not shaken loose. This should be done every once in a while, at least every time the car is parked. The sensors on the roof are expensive and heavy, and if they come loose, they may fall on the car driving behind you and cause a serious accident.

The FLIR cameras should be attached to the two L-shaped brackets, with the camera labeled "Flir Left" going on the left bracket, and the "Flir Right" camera going on the right bracket. You should also ensure that the cameras point forward, and will not come loose/shake during the recording.

The Multisense/Lidar setup should be carefully lifted on top of the roof rack, with the Multisense lenses pointing forward.
Place the setup on top of the driver side custom bracket, and its screws lined up by a few rotations. After the screws are loosely attached, line the passenger side bracket with the screws on the camera setup. Attach the screws on that side loosely, making sure not to crossthread the screws. After all screws are attached, tighten them securely, preferably with a ratchet wrench to ensure enough force is used.
After the screws are tightened securely, you should be able to grab the setup and move it around, with the setup not shaking/rattling. You should be able to sway the car while holding from the setup.

Attach the cables on the Multisense camera. Plug the green cable on the matching port on the back right side of the camera, making sure to match the notch inside the connector to the port, as it can be plugged in only one way. After plugging it in, screw the nut around the cable tightly. If the screw stops turning with reasonable force, try to push the cable in deeper, and if it moves in, tighten the screw again.
Next, plug the power cable of the Multisense camera to the grey port, mathcing the notches on the cable to the port. The clips on the side of the cable should snap/click into place once the cable is properly attached. If the clips do not click correctly, the cable is not properly attached, and may come loose.

Route the cables on top of the roof to the cable passthrough. DETAILED EXPLANATION SHOULD BE WRITTEN HERE ONCE ENSURED THE DETAILS!!

Once the cables have been routed into the car, plug them in following the guide:

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

For Nano and Raspberry Pi, the ros-device-control/ directory should be at the desktop, you can open up the directory by typing:

```bash
cd ros-device-control/
```

For Orin, type:

```bash
cd /mnt/Burak2/ros-device-control
```

Inside each device, run their respective docker compose files inside the docker directory.

```bash
docker compose up
```

## Starting the recording

When each of the containers are up, detach from the one running on Orin by pressing D, and go inside the container.

```bash
docker exec -it ros-multisense bash
```

Start the recording inside the container.

```bash
source install/setup.bash

ros2 bag record --max-bag-duration 10 --max-cache-size 20000000000 --compression-mode file --compression-format zstd --output bags/FILE_NAME --topics /lidar_points /flir_left/image_raw /flir_right/image_raw /aux/image_color /left/cost /left/depth /left/image_rect /right/image_rect /imu
```

This will start the recording, saving the files inside the bags/ directory. This can be stopped by pressing CTRL + C inside the container. The recording should _ALWAYS_ be stopped in this way, as if it is not stopped gracefully (for example, stopping the container without stopping the recording first) will lead into the recording being corrupted.
