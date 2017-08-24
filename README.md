# RuuviRelay
a script to send RuuviTag data in to a database. Usable via cron.

uses a slightly modified ruuvitag-sensor python library to listen for value from the tags
from: https://github.com/ttu/ruuvitag-sensor

#requires

python3
mysql-server

## bluez

        sudo apt install bluez-hcidump


## mysql-extra

        sudo apt-get install libmysqlclient-dev
        sudo apt-get install python3-dev
        pip install mysqlclient

## libraries

        pip install dataset
        pip install psutil
