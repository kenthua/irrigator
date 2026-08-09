#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SERVICE_NAME=$(basename $SCRIPT_DIR)

echo
echo "Installing $SERVICE_NAME..."

# set permissions for script files
echo "Setting permissions..."
chmod 755 $SCRIPT_DIR/*.py
chmod 755 $SCRIPT_DIR/*.sh
chmod 755 $SCRIPT_DIR/service/run
chmod 755 $SCRIPT_DIR/service/log/run

# check dependencies
python3 -c "import schedule" 2>/dev/null
if [ $? -gt 0 ]
then
    echo "Installing requirements..."
    python3 -m pip install -r $SCRIPT_DIR/requirements.txt
    if [ $? -gt 0 ]
    then
        # if pip command fails install pip and then try again
        opkg update && opkg install python3-pip
        python3 -m pip install -r $SCRIPT_DIR/requirements.txt
    fi
fi

# check relay config
echo "Check relay config"
STRING_CHECK=relay_2
GPIO_FILE=/etc/venus/gpio_list

if [[ -f "$GPIO_FILE" ]] && [[ -z $(grep "$STRING_CHECK" "$GPIO_FILE") ]];
then
	echo "Relay missing..."
	echo "2 out relay_2" >> $GPIO_FILE; 
fi

# create sym-link to run script in daemon
if [ ! -L /service/$SERVICE_NAME ]; then
    echo "Creating service..."
    ln -s $SCRIPT_DIR/service /service/$SERVICE_NAME
else
    echo "Service already exists."
fi

# add install-script to rc.local to be ready for firmware update
filename=/data/rc.local
if [ ! -f $filename ]
then
    touch $filename
    chmod 755 $filename
    echo "#!/bin/bash" >> $filename
    echo >> $filename
fi

# if not already added, then add to rc.local
grep -qxF "bash $SCRIPT_DIR/install.sh" $filename || echo "bash $SCRIPT_DIR/install.sh" >> $filename

echo "Installation complete."
echo
