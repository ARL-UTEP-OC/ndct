# ECELd-NetSys

## System Requirements
ECEL should run from a variety of Linux Distros, but it has been primarily tested on:
* Kali Linux 2019.2 64-bit

## Setting up from source

1. Ensure that [eceld](https://github.com/ARL-UTEP-OC/eceld) is installed and running on your system.
2. Download the code and install python3 venv
```
git clone https://github.com/ARL-UTEP-OC/eceld-netsys
cd eceld-netsys
sudo apt-get install python3-venv
```
1. Set up the venv environment
```
python3 -m venv venv
source venv/bin/activate
```
4. Install python dependencies
```
pip install -r install-requirements.txt
```

## Run the GUI
1. Instantiate the venv container
```
source venv/bin/activate
```
2. Instantiate the GUI
```
fbs run
```
