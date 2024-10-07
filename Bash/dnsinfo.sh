#!/bin/bash

# Begin Color Coding
red=$(tput setaf 1)
green=$(tput setaf 2)
purple=$(tput setaf 5)
yellow=$(tput setaf 3)
cyan=$(tput setaf 6)
reset=$(tput sgr0)
# End Color Coding


#           ##################################################
#           ################   FUNCTIONS  ####################
#           ##################################################


### BEGIN Function to display --help page ###

F_HELP () {

    echo -e "\n${yellow} **************************************"
    echo -e "                     ************** DNS INFO **************"
    echo -e " **************************************"
    echo -e "                              Created by: bnewman"
    echo
    echo -e "  Gathers registration, nameserver, and DNS information for a specific domain."
    echo
    echo -e "                             Script Syntax & Usage:"
    echo
    echo -e "                            bash dnsinfo.sh \$DOMAIN"
    echo
    echo -e "  where \$DOMAIN = a registered domain with information in the whois database."
    echo
    echo -e "       If the domain is not registered, the script will exit with error:${reset}"
    echo -e "                         ${red} “Error: Unregistered Domain”${reset}"
    echo
    echo -e "${yellow}If multiple domains are passed as arguments to the script, it will exit with error:${reset}"
    echo -e "                         ${red} “Error: Too Many Arguments”${reset}"
    echo
    echo -e "${yellow}If no domains are passed as arguments to the script, it will exit with error:${reset}"
    echo -e "                         ${red} “Error: No Argument Passed”${reset}"
    echo
    echo -e "${yellow}If no whois server can be found for the specific TLD passed to the script, it will exit with error:${reset}"
    echo -e "                         ${red} “Error: No whois Server Found”${reset}"
    echo
    echo -e "      ${yellow}Email me at bnewman@liquidweb.com with any feedback and/or requests.\n\n${reset}"
    exit 0

}

### END Function to display --help page ###


### BEGIN Function to display basic usage for script to terminal upon syntax/usage error ###

F_USAGE () {

    echo -e "\n${yellow}    Basic Syntax:\n${reset}bash dnsinfo.sh \$DOMAIN.TLD\n\nRun script with --help for more info\n"
    exit 0

}

### END Function to display basic usage for script to terminal upon syntax/usage error ###


### BEGIN Function to use jwhois in place of whois ###

F_JWHOIS () {

    # General domain information for the domain

    echo -e "${cyan}General Domain Information for:${reset} $domain\n"
    jwhois $domain|egrep 'Domain\ Name|Registrar:|(Updated|Creation|Expiration)\ Date'

    # Check to see if domain is expired or not

    echo -e "\n${yellow}Checking to see if the domain has expired...${reset}"
    jwhois $domain|awk '/Expiration/ {print $5}'|cut -d\T -f1|

    # compare expiration date in epoch to today's date converted to epoch to see if expiration date > today or not

    while read JEXPDATE; do

        todayepoch=$(date +%s)
        jexpepoch=$(date -d $JEXPDATE +%s)
        let DIFF=$jexpepoch-$todayepoch

            if [ $DIFF -eq 0 ]  then
                echo -e "${red}";echo -e "\n$domain expired today!";echo -e "${reset}"
            elif [ $DIFF -gt 0 ]  then
                echo -e "\n$domain expires in $(expr $DIFF / 60 / 60 / 24 + 1) days"
            else
                echo -e "${red}";echo -e "\n$domain has expired! Renew domain ASAP to restore functionality!";echo -e "${reset}"
                exit 0
            fi
    done

    # Find authoritative nameservers for domain as reported by the registrar

    echo -e "\n${cyan}Authoritative Nameservers:${reset}"
    jwhois $domain|egrep -i "name\ server|nameserver"|head -n2

    ns1=$(jwhois $domain|egrep -i "name\ server|nameserver"|head -n1)

    # Find Nameserver Information via jwhois & if jwhois returns no results then try using whois

    if [ $(jwhois $ns1|grep -o "No match for domain"|wc -l) -eq 1 ]  then
            echo -e "\n${red}No nameserver information found using jwhois.${reset} Trying again using whois..."

            if [ $(whois $ns1|grep -o "No match for"|wc -l) -eq 1 ]  then
                echo -e "${red}No nameserver information found using whois either... Proceeding with DNS information for $domain ${reset}"
            else
                echo -e "\n ${cyan}Nameserver Registration Information:\n ${reset}"
                for n in $(whois $domain|grep -i 'name server'|head -n2|cut -d\: -f2);do whois $n|head -n12|grep -A4 "Server Name:"|egrep -v "Whois|Referral"&&echo "";done
            fi

    fi

}

### END Function to use jwhois instead of whois ###


### BEGIN Function to use whois instead of jwhois ###

F_WHOIS () {

    # General domain information for the domain

    echo -e "${cyan}Domain Registration Information:\n${reset}"
    whois $domain|grep -B12 ">>>"|head -n13|egrep -vi 'name\ server|nameserver|whois\ server|sponsoring|referral'|grep -v ">>>"

    # Make sure domain isn't expired

    echo -e "\n${cyan}Checking to see if domain is expired...${reset}"

    # Get domain expiration date and convert it to epoch

    whois $domain|grep -B12 ">>>"|head -n13|egrep -vi 'name\ server'|awk '/Expiration/ {print $3}'|

    # compare expiration date in epoch to today's date converted to epoch to see if expiration date > today or not

    while read EXPDATE  do

        todayepoch=$(date +%s)
        expepoch=$(date -d $EXPDATE +%s)
        let DIFF=$jexpepoch-$todayepoch

            if [ $DIFF -eq 0 ]  then
                echo -e "${red}";echo -e "\n$domain expired today!";echo -e "${reset}"
            elif [ $DIFF -gt 0 ]  then
                echo -e "\n$domain expires in $(expr $DIFF / 60 / 60 / 24 + 1) days"
            else
                echo -e "${red}";echo -e "\n$domain has expired! Renew domain ASAP to restore functionality!";echo -e "${reset}"
                exit 0
            fi
    done

    # Find Authoritative Nameservers for the domain that are set at the registrar level

    echo -e "\n${cyan}Authoritative Nameservers:${reset}"
    whois $domain |grep -i 'name server' |head -n2

    # Find Nameserver Information via whois

    echo -e "\n${cyan}Nameserver Info:\n${reset}"
    for ns in `whois $domain|grep -i 'name server'|head -n2|cut -d\: -f2` ;
    do whois $ns|head -n12|grep -A4 "Server Name:"|egrep -v "Whois|Referral"&&echo "" ;
    done

}

### END Function to use whois instead of jwhois ###


### BEGIN Function to gather DNS information for $domain ###

F_DNS () {

    # Show IP that A record points to

    echo -e "${cyan}A Record Points To: ${reset}"
    dig +short $domain

    # Check for PTR record (rDNS) for A record & associated server hostname

    if [ "$(dig -x $(dig +short $domain) +noadditional +noauthority +noedns|grep flags|cut -d\, -f2|awk '{print $2}')" -eq 0 ]  then
            echo -e "\n${red}No PTR record found!${reset} Set up rDNS for $(dig +short $domain) that points to the correct server's hostname."
    else
            echo -e "\n${green}Found PTR record for: ${reset}$(dig +short $domain). IP is allocated to:\n"
            dig -x $(dig +short $domain) +noall +answer|grep -v ";"|awk '/PTR/ {print $5}'
    fi

    # Show MX Records for domain

    echo -e "\n${cyan}MX Records: ${reset}"
    dig +short mx $domain|sort -n

    # Figure out if mail exchange in WHM should be set to local or remote and output answer to terminal

    if [ "$(dig +short mx $domain|sort -n|head -n1|awk '{print $2}'|cut -d\. -f1,2)" != $domain ]  then
            echo -e "\nMail exchange should be set to ${red}REMOTE${reset} in WHM"
    else
            echo -e "\nMail exchange should be set to ${red}LOCAL${reset} in WHM"
    fi

    # Check for TXT records and output them to the terminal

    echo -e "\n${cyan}Checking for TXT records...${reset}"
    dig +nocomments +noquestion +noauthority +noadditional +nostats TXT $domain|grep -v ";"

    # See if there are any SPF records, if so see if any of them have additional included authenticated domains/IPs

    if [ "$(dig +nocomments +noquestion +noauthority +noadditional +nostats TXT $domain|grep -v ";"|grep -i "spf"|wc -l)" -ge 1 ]  then
            echo -e "\n${green}SPF RECORDS FOUND!${reset}"
    else
            echo -e "\n${red}SPF RECORDS NOT FOUND!${reset} Default SPF record for $domain:\nv=spf1 +a +mx +ip4:$(dig +short $domain) ~all"
    fi

}

### END Function to gather DNS information for $domain ###



#               ##################################################
#               ##################   SCRIPT ######################
#               ##################################################



# Define $domain variable from first argument to script and turn all arugments passed into bash array for error handling

args=("$@")
domain="$1"

# Error handling if arguments to script are not correct

if [ $(echo $#) = 0 ]  then
        echo -e "${red}Error: No Argument Passed${reset} "
        sleep 1
        F_USAGE
else

        if [ $(echo $#) -ge 2 ]  then
            echo -e "${red}Error: Too Many Arguments${reset}\nNumber of arguments passed: $#  "
            sleep 1
            F_USAGE
        else

            if [ $(whois $domain|grep -i "No match for"|wc -l) -eq 1 ]  then
                echo -e "${red}Error: Unregistered Domain${reset}"
                whois $domain|grep -A1 "No match for"
                sleep 1
                F_USAGE
            else

                if [ $(whois $domain|egrep -i "No whois server is known"|wc -l) -eq 1 ]  then
                echo -e "${red}Error: No whois Server Found${reset}"
            sleep 1
            F_USAGE
            else
                    if [ $1 = --help ]  then
                        F_HELP
                    else
                        echo -e "\n${cyan}Gathering domain & DNS information for:${reset} $domain\n"
            fi
                fi
            fi
        fi
fi

# Check to see if jwhois installed

if [ -e $(which jwhois) ]  then
        echo -e "Found jwhois! Would you like to use it instead of "whois"?\n"
        echo -e "1) Yes"
        echo -e "2) No"
        echo -e "3) Exit\n"
        read -p "Please enter choice (1-3):  " choice;
        case $choice in
            1) echo -e "Using jwhois instead of whois...\n" ; F_JWHOIS && F_DNS ;;
        2) echo -e "Using whois instead of jwhois...\n" ; F_WHOIS && F_DNS ;;
        3) exit 0
        esac
else
        echo -e "jwhois not installed, consider installing jwhois for better results. Proceeding using whois...\n"
        F_WHOIS && F_DNS
fi
