#!/bin/bash
# Modified from https://github.com/GoogleCloudPlatform/getting-started-php/blob/master/optional-compute-engine/gce/startup-script.sh

# [START all]
set -e
export HOME=/root

# [START php]
apt-get update
apt-get install -y git apache2 php5 php5-mysql php5-dev php-pear pkg-config mysql-client


# Fetch the project ID from the Metadata server
PROJECTID=$(curl -s "http://metadata.google.internal/computeMetadata/v1/project/project-id" -H "Metadata-Flavor: Google")

# Get the application source code
git config --global credential.helper gcloud.sh
git clone https://source.developers.google.com/p/gcp-cookbook/r/gcpcookbook  /opt/src -b master
#ln -s /opt/src/optional-compute-engine /opt/app
cp /opt/src/Chapter01/php-app/pdo/* /var/www/html -r
# [END php]

systemctl restart apache2
iptables -A INPUT -i eth0 -p tcp -m tcp --dport 3306 -j ACCEPT

# [START project_config]
# Fetch the application config file from the Metadata server and add it to the project
#curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/project-config" \
#  -H "Metadata-Flavor: Google" >> /opt/app/config/settings.yml
# [END project_config]
# [START logging]
# Install Fluentd
sudo curl -s "https://storage.googleapis.com/signals-agents/logging/google-fluentd-install.sh" | bash

# Start Fluentd
service google-fluentd restart &
# [END logging]
# [END all]
