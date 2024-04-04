#!/usr/bin/env bash
# This script sets up web servers for deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    apt-get update
    apt-get -y install nginx
fi

# Create necessary folders if they don't exist
mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file
echo "<html>
<head>
</head>
<body>
  Holberton School
</body>
</html>" > /data/web_static/releases/test/index.html

# Create or recreate the symbolic link
rm -rf /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group recursively
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
if grep -q "hbnb_static" "$config_file"; then
    sed -i '/location \/hbnb_static/ {n;n;n;n;n;s/index.html/index.html;/}' "$config_file"
else
    sed -i '/^\s*server_name _;/a\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' "$config_file"
fi

# Restart Nginx
service nginx restart

exit 0
