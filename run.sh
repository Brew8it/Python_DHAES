#!/usr/bin/env bash
# add pynacl install to script
while true; do
    read -p "Do you wish to check that all dependency's are installed so that the program runs correctly? [Y/N] " y
    case $y in
        [Yy]* )
            echo "** Checking if python 2.7 is installed **"
            command -v python2.7 >/dev/null 2>&1 || { echo "I require python2.7 but it's not installed, Installing Python 2.7" >&2; sudo apt-get install python2.7; }
            echo "** Checking if pip is installed! **"
            command -v pip >/dev/null 2>&1 || { echo "I require pip but it's not installed, Installing pip" >&2; sudo apt-get install python-pip; }

            while true; do
                read -p "Do you have PyNaCL installed? [Y/N] " yn
                case $yn in
                    [Yy]* )  break;;
                    [Nn]* ) pip install pyOpenSSL; break;;
                    * ) echo "Please answer yes or no.";;
                esac
            done
                break;;
        [Nn]* ) break;;
    esac
done

echo  "** Starting up Server.py **"
gnome-terminal -e "python server.py"
echo  "** Starting up Client.py **"
gnome-terminal -e "python client.py"