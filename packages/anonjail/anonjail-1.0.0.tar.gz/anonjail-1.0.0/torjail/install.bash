#!/bin/bash
sudo apt-get -y install bc tor firejail python3-pip gksu
sudo systemctl enable tor --now
sudo systemctl enable apparmor --now
sudo sed -i 's/restricted-network yes/restricted-network no/g' /etc/firejail/firejail.config