#!/bin/bash
set -e

ECEL_NETSYS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

OUTPUT_PREFIX="ECELD_NETSYS INSTALLER:"
OUTPUT_ERROR_PREFIX="$OUTPUT_PREFIX ERROR:"

PYTHON_EXEC="python3"

### Helper functions
#
prompt_accepted_Yn() {
    read -r -p "$1 [Y/n] " yn
    case $yn in
        [nN]*) return 1 ;;
        *) return 0 ;;
    esac
}

# Updates
#echo "Running apt-get update"
#apt-get -y update
#echo "Running apt-get upgrade"
#apt-get upgrade

### Check if running as root
#
if [ "$EUID" -ne 0 ]; then
    echo "$OUTPUT_ERROR_PREFIX Please run this installation as root"
    exit 1
fi

### Install dependencies
#
REQUIRED_PROGRAMS="wireshark suricata python3-pip python3-venv git"
REQUIRED_PYTHON_PACKAGES="PyQt5 Pyro4 Pillow jinja2"

        plugin_prompt="eceld found, remove it and reinstall?"
        if [ -d $ECEL_NETSYS_DIR/eceld ]; then
           if prompt_accepted_Yn "$plugin_prompt"; then
              rm $ECEL_NETSYS_DIR/eceld -rf
   	      git clone https://github.com/ARL-UTEP-OC/eceld "$ECEL_NETSYS_DIR"/eceld
   	      pushd "$ECEL_NETSYS_DIR"/eceld
	      chmod +x install.sh
	      ./install.sh
	      popd
           fi
    	else
	   git clone https://github.com/ARL-UTEP-OC/eceld "$ECEL_NETSYS_DIR"/eceld
   	   pushd "$ECEL_NETSYS_DIR"/eceld
	   chmod +x install.sh
	   ./install.sh
	   popd
       fi

    if [ ! -d $ECEL_NETSYS_DIR/eceld ]; then
	echo "Download and installation of $plugin not successful (can't execute program) quitting..."
	exit 1
    fi 

echo "$OUTPUT_PREFIX Installing Additional Dependecies"
if [ -x "/usr/bin/apt-get" ]; then
    apt-get -y install $REQUIRED_PROGRAMS
elif [ -x "/usr/bin/yum" ]; then
    yum install -y $REQUIRED_PROGRAMS
else
    echo "$OUTPUT_ERROR_PREFIX Distribution not supported"
    exit 1
fi

### Create virtualenv if it doesn't currently exist
echo "$OUTPUT_PREFIX Installing python dependencies"
if [ ! -d "venv" ]; then
    $PYTHON_EXEC -m venv venv
fi
source venv/bin/activate
pip install pip --upgrade
pip install $REQUIRED_PYTHON_PACKAGES


### Creating executable
#
echo "$OUTPUT_PREFIX Creating executables"
cat > "$ECEL_NETSYS_DIR"/eceld-netsys-gui <<-'EOFeceld-netsys-gui'
	#!/bin/bash
	ECEL_NETSYS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
	if [ "$EUID" -ne 0 ]; then
		echo "ECELD-NETSYS must be run as root"
		exit 1
	fi
    cd "$ECEL_NETSYS_DIR"
	venv/bin/python3 main.py
EOFeceld-netsys-gui

chmod +x "$ECEL_NETSYS_DIR"/eceld-netsys-gui
echo "$OUTPUT_PREFIX Installation Complete"
echo "To run the GUI, start the service (takes roughly 10 seconds):"
echo "sudo eceld/eceld_service"
echo "Afterwards, invoke:"
echo "sudo ./eceld-netsys-gui "
