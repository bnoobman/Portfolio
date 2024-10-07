####################################################################################################################
#########################                 Wordpress Auto-Uptdate Script                    #########################
#########################            Created by bnewman, jcrisovan, and ahouston           #########################
#########################          Please send feature requests and bug reports to:        #########################
#########################                        bnoobman@gmail.com                        #########################
####################################################################################################################

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
#logfile="/var/log/wordpress_autoupdate.log"

### Variables
installs=$(find /home/*/public_html/ -type f -iname wp-config.php|sed -r 's/\/wp-config\.php$//g')
installs=($installs)

# First find all wordpress installations
echo "${cyan}Wordpress Installations:${reset}"
printf %"s\n" ${installs[@]}

# Define Wordpress AutoUpdate Functions

autoupdate_version() {
  read -p "Press ${green}y${reset} to update or ${red}n${reset} to skip:  " wpver
  if [ $wpver = y ] ; then
    echo "Updating version now: " ;
    $wp core update $path &&
    echo "${cyan}New version is:${reset} ";${yellow} $version ${reset} ; 
  else
    echo "No version update selected. Checking plugins next..."
  fi
}

autoupdate_plugins() {
  read -p "Press ${green}y${reset} to update or ${red}n${reset} to skip:  " wpplug
  if [ $wpplug = y ] ; then
    echo "Updating plugins now: " ;
    $wp plugin update --all $path 2>/dev/null &&
    echo "${cyan}All available updates applied!${reset}" ; 
  else
    echo "No update selected. Checking themes next..."
  fi
}

autoupdate_themes() {
  read -p "Press ${green}y${reset} to update or ${red}n${reset} to skip:  " wpthemes
  if [ $wpthemes = y ] ; then
    echo "Updating themes now: " ;
    $wp theme update --all $path 2>/dev/null &&
    echo "${cyan}All available updates applied!${reset}" ;   
  else
    echo "No update selected."
  fi
  echo "${yellow}Updating database to apply all updates:${reset} "
  $wp core update-db $path &&
  echo "${yellow}Database update complete. Moving on to next installation.${reset}"
  echo
  clear
}

# Define function to complete the updates for each site

wp_update () {
  cpuser=$(pwd | cut -d/ -f3)
  wp="sudo -u $cpuser -i -- wp"
  path="--path=$i"
  version="$wp core version $path"
  echo "${yellow}Installation: $i ${reset}";
  echo
  read -p "${yellow}Would you like to create a database backup?${reset} Press ${green}y${reset} for yes or ${red}n${reset} for no:  " dbback
  if [ $dbback = y ] ; then
    echo "Dumping Database..."
    $wp db export $path $i/db.backup ;
  else
    echo "No database backup created. Proceeding..."
  fi
  echo 
  echo "${cyan}Version: "${reset} ; echo "${yellow}"; $version ; echo "${reset}";
  if [ `$wp core check-update $path | egrep -i 'up to date|at the latest'|wc -l` -eq 1 ] ; then
    echo "Wordpress is up to date, checking plugins next..." ; 
  else
    echo "Wordpress not up to date!"
    autoupdate_version
  fi
  plugins="$wp plugin list $path"
  echo "${yellow}Plugin List:${reset} "
  echo
  $plugins
  echo
  echo "${yellow}Would you like to apply all available updates?${reset}"
  autoupdate_plugins
  themes="$wp theme list $path"
  echo "${yellow}Theme List:${reset} "
  echo
  $themes
  echo
  echo "${yellow}Would you like to apply all available updates?${reset}"
  autoupdate_themes
}

# actually run the updates interavtively

#exec >> $logfile
for i in "${installs[@]}" ; do cd $i ; wp_update ; done
#exit 0

