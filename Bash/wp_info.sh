#!/bin/bash

### Constants
today=$(date +%A\ %F\ %T)
red=`tput setaf 1`
green=`tput setaf 2`
purple=`tput setaf 5`
yellow=`tput setaf 3`
cyan=`tput setaf 6`
reset=`tput sgr0`
bold=`tput bold`

### Variables
installs=$(find /home/*/public_html/ -type f -iname wp-config.php|sed -r 's/\/wp-config\.php$//g')
installs=($installs)

# Check if wp-cli is installed or not
echo "Checking for dependencies..."
if [ "$(which wp)" == "" ] ; then
  echo "${red}WP-CLI not installed! Please install and re-run this script!${reset}"
  exit 0
else
  echo "${green}WP-CLI found! Proceeding...${reset}"
  clear
fi

# First find all wordpress installations
echo "${cyan}Wordpress Installations:${reset}"
printf %"s\n" ${installs[@]}
echo

wp_info () {
  cpuser=$(pwd | cut -d/ -f3)
  wp="sudo -u $cpuser -i -- wp"
read -p "Which installation would you like information for? " path ; 
#  version="$wp core version $path"
#  core_update="$wp core check-update $path"
##  checksum="$wp core verify-checksums $path"
#  plugins="$wp plugin list $path"
#  themes="$wp theme list $path"
#  site_url="$wp option get siteurl $path"
cd $path
  cpuser=$(pwd | cut -d/ -f3)
  wp="sudo -u $cpuser -i -- wp"
  version="$wp core version $path"
echo "${yellow}Installation: $path ${reset}"
echo "${cyan}Version: "${reset} ; echo "${yellow}"; $version ; echo "${reset}"
  core_update="$wp core check-update $path"
if [ `$core_update | egrep -i 'up to date|at the latest'|wc -l` -eq 1 ] ; then
  echo "Wordpress is up to date!" 
else
  echo "Wordpress core update available"
fi
  DBNAME="awk '/DB_N/ {print $2}'  $path/wp-config.php|cut -d\' -f2" 
  DBPASS="awk '/DB_P/ {print $2}'  $path/wp-config.php|cut -d\' -f2"
  DBUSER="awk '/DB_U/ {print $2}'  $path/wp-config.php|cut -d\' -f2"
echo "Database Information:"
echo "Datbase: $DBNAME"
echo "User: $DBUSER"
echo "Password: $DBPASS"
echo
  site_url="$wp option get siteurl $path"
echo "Site URL: $site_url"
echo
  plugins="$wp plugin list $path"
echo "Plugins: $plugins"
echo
  themes="$wp theme list $path"
echo "Themes: $themes"
}

wp_info

