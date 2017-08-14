import sys
import argparse
from relay import sendData, insertMacs, trimDb
from ruuvitag_sensor.ruuvi  import RuuviTagSensor

def save_log():
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='insertMacs', nargs='*', help='insert trusted mac addresses')
    parser.add_argument('-s', '--save', action='store_true', help='save current logs to db')
    parser.add_argument('-t', '--trim', action='store_true', help='trim older logs from db')

    args = parser.parse_args()

    if args.insertMacs:
        macs = ['FF:74:4E:5D:1D:9D'] # for testing
        macDict = {"mac":x for x in macs}
        insertMacs(macDict)
    elif args.save:
        sendData()
    elif args.trim:
        trimDb()
    else:
        parser.print_usage()
