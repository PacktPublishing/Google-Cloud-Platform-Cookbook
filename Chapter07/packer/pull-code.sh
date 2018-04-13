#!/bin/bash
echo "<?php phpinfo(); ?>" | sudo tee --append /var/www/html/info.php
#cd /var/www/html
#sudo git clone https://github.com/banago/simple-php-website.git 
sudo systemctl restart apache2
