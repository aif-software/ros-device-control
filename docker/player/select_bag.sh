#!/bin/bash

select bag in /mnt/Burak2/ros-device-control/bags/*
do
    break
done

BAG="/bags/$(basename "$bag")" docker compose up
