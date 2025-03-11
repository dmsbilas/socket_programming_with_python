sudo apt-get install jq

current_dir=$(pwd)

echo "Current directory: $current_dir"

# Read the service name from the config.json file
service_name=$(jq -r '.name' config.json)
file_to_run=$(jq -r '.command_to_run_file' config.json)
echo "Service name: $service_name"

# Create the service file
service_file="$current_dir/$service_name.service"
echo "Creating service file: $service_file"

# Create the service file
cat <<EOF > $service_file
[Unit]
Description=$service_name
After=network.target

[Service]
ExecStart=$file_to_run
WorkingDirectory=$current_dir
StandardOutput=append:/var/log/$service_name.log
StandardError=append:/var/log/$service_name.log
SyslogIdentifier=$service_name
Restart=always
User=root
Environment=PYTHONUNBUFFERED=1


[Install]
WantedBy=multi-user.target
EOF

echo "Service file created: $service_file"

# Copy the service file to the systemd directory
sudo cp $service_file /etc/systemd/system/

# Reload the systemd daemon
sudo systemctl daemon-reload

# Enable the service
sudo systemctl enable $service_name

# Start the service
sudo systemctl start $service_name
