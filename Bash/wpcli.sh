#!/bin/bash

## Color Coding
red=`tput setaf 1`
green=`tput setaf 2`
purple=`tput setaf 5`
reset=`tput sgr0`
bold=`tput bold`
## End Color Coding


### First check if wp-cli is already installed

if [ `wp cli version --allow-root 2>/dev/null |grep -ci 'WP-CLI'` -eq 1 ] ; then
	echo "WP-CLI already installed!" ; else
	echo -e "WP-CLI not installed... Installing now:\n"

### Install wp-cli

	curl -s -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar&&chmod +x wp-cli.phar&&mv wp-cli.phar /usr/local/bin/wp;
echo "Installation Complete!"
fi

echo -e "Checking for Suhosin...\n"

### Check if suhosin is enabled

if [ `php -v | grep -ic suhosin` -eq 1 ]; then 
	echo 'Suhosin is enabled... Need to modify PHP configuration?' ;
 
		if [ `egrep -ci '^suhosin.executor.include.whitelist = phar' /usr/local/lib/php.ini` -eq 0 ] ; then 
			echo 'Yes, modification in progress. Backing up current configuration file:'&&cp -avr /usr/local/lib/php.ini /usr/local/lib/php.ini.lwbak_pre_wp-cli_install&&echo "suhosin.executor.include.whitelist = phar" >> /usr/local/lib/php.ini&&echo 'Modification Complete' ; else
			echo 'No, configurations already in place! All set!'
		fi

	else
 	echo 'Suhosin not enabled. All set!';
fi

echo ""
echo -e "To find WP-CLI version run:\n" 
echo -e "wp cli version --allow-root\n"
echo -e "Don't forget to switch to the user when running WP-CLI commands! DO NOT USE "--allow-root"!!! You'll break all the things!"
echo -e "For more help run:\n"
echo -e "wp help\n"
echo -e "or visit http://wp-cli.org/commands/" 

