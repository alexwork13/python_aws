#!/bin/bash

sudo mkdir /mnt/ForNewPartition
sudo mkfs.ext4 /dev/xvdy
sudo mount /dev/xvdy /mnt/ForNewPartition
sudo touch /mnt/ForNewPartition/FileInNewPartition