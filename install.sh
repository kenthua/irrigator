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
python -c "import gpiozero"
if [ $? -gt 0 ]
then
    echo "Installing requirements..."
    python -m pip install -r requirements.txt
    if [ $? -gt 0 ]
    then
        # if pip command fails install pip and then try again
        opkg update && opkg install python3-pip
        python -m pip install -r requirements.txt
    fi
fi

# update import
echo "Comment colorsys from conversions"
CONVERSIONS_SCRIPT_FILE=/usr/lib/python3.8/site-packages/colorzero/conversions.py
sed -i -e 's/^import colorsys/#import colorsys/' $CONVERSIONS_SCRIPT_FILE

# check relay
STRING_CHECK=relay_2
GPIO_FILE=/etc/venus/gpio_list

if [[ -z $(grep "$STRING_CHECK" "$GPIO_FILE") ]];
then
	echo "Relay missing..."
	echo "2 out relay_2" >> $GPIO_FILE; 
fi

# create sym-link to run script in deamon
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

# if not alreay added, then add to rc.local
grep -qxF "bash $SCRIPT_DIR/install.sh" $filename || echo "bash $SCRIPT_DIR/install.sh" >> $filename

echo
