# ECELd-NetSys

## System Requirements
ECEL should run from a variety of Linux Distros, but it has been primarily tested on:
* Kali Linux 2020.2 64-bit
* Ubuntu 20.04 LTS
* [Python 3 >= 3.5](https://www.python.org/downloads/release/python-369/)

## Setting up from source

1. Clone the repository and run the installer as superuser
```
sudo ./install.sh
```
This will install all dependecies, including [eceld] (https://github.com/ARL-UTEP-OC/eceld)

## Run the GUI
1. Open a separate terminal and start the eceld service
```
sudo eceld/eceld_service
```
Allow some time for the service to instantiate (this usually takes 5-10 seconds)
2. Instantiate the GUI
```
sudo ./eceld-netsys-gui
```
