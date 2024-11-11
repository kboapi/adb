#!/bin/bash
rm $PREFIX/bin/ngrok
rm -rf $PREFIX/share/ngrok
mkdir -p $PREFIX/share/ngrok
cp get-ngrok.sh $PREFIX/share/ngrok
cp ngrok $PREFIX/bin
apt update && apt upgrade -y
apt install -y proot wget resolv-conf
apt clean
apt autoremove
cd $PREFIX/share/ngrok
bash get-ngrok.sh
echo -e "\e[1;32mNgrok installed sucessfull!"
echo "Run : ngrok "
echo " To use ngrok"


NGROK_CONFIG_FILE="$HOME/.config/ngrok/ngrok.yml"
ngrok config add-authtoken 2jbLcOBiy3lcZwmxDS4lAcRsJDy_5JyfWPnLHEy4uWowuyF54
# Prompt the user to enter the edge label value and port
read -p "Enter the edge label value (e.g., edghts_2nNWk2oF0axtVBmu5QPmtajeqYB): " EDGE_LABEL
read -p "Enter the port number to forward (e.g., 56485): " PORT

# Modify the ngrok configuration file dynamically
cat <<EOL > "$NGROK_CONFIG_FILE"
version: 2
authtoken: 2jbLcOBiy3lcZwmxDS4lAcRsJDy_5JyfWPnLHEy4uWowuyF54
tunnels:
  my_tunnel_name:
    labels:
      - edge=$EDGE_LABEL
    addr: http://localhost:$PORT
EOL

echo "ngrok configuration file has been set up with edge label: $EDGE_LABEL and port: $PORT"

# Start all tunnels defined in the configuration file
ngrok start --all

# NGROK_CONFIG_FILE="$HOME/.ngrok2/ngrok.yml"

# #!/bin/bash

# # Prompt the user to enter the edge label value
# read -p "Enter the edge label value (e.g., edghts_2nNWk2oF0axtVBmu5QPmtajeqYB): " EDGE_LABEL
# read -p "Enter the port number to forward (e.g., 56485): " PORT


# ngrok config edit


# # Create or update ngrok config file
# cat <<EOL > $NGROK_CONFIG_FILE
# version: 2
# authtoken: 2jbLcOBiy3lcZwmxDS4lAcRsJDy_5JyfWPnLHEy4uWowuyF54
# tunnels:
#   my_tunnel_name:
#     labels:
#       - edge=$EDGE_LABEL
#     addr: http://localhost:$PORT
# EOL

# echo "ngrok configuration file has been set up with edge label: $EDGE_LABEL and port: $PORT"

# ngrok start --all