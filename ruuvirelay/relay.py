from ruuvitag_sensor.ruuvi import RuuviTagSensor
from ruuvitag_sensor.common import Config

from datetime import datetime
import dataset
import yaml

previousData = None
cfg = None
db = None

TRIM_ROWS_TO = 100

# MAC FF:74:4E:5D:1D:9D
# {'acceleration': 1012.0459475735279,
#  'pressure': 1005.37,
#  'temperature': 24.42,
#  'acceleration_y': 0,
#  'acceleration_x': -46,
#  'battery': 3019,
#  'acceleration_z': 1011,
#  'humidity': 52.5}
def openConn():

    import os, sys
    path = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open('%s/config.yaml' %path, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return dataset.connect('mysql://%s:%s@%s/%s' %( cfg['mysql']['user'],
                                                    cfg['mysql']['passwd'],
                                                    cfg['mysql']['host'],
                                                    cfg['mysql']['db']))

def sendData(db=openConn()):

    table = db['device']
    logTable = db['ruuvi_log']
    rows = table.all()
    macs = [{'mac': x['mac'], 'id': x['id']} for x in rows]
    print(macs)
    data = RuuviTagSensor.get_data_for_sensors([ mac['mac'] for mac in macs], search_duratio_sec=5)
    print(data)
    for mac in macs:
        if mac['mac'] in data and data[mac["mac"]] != None:
            data[mac["mac"]]['device_id'] = mac['id']
            data[mac["mac"]]["created"] = datetime.now()
            try:
                logTable.insert(data[mac["mac"]])
            except Exception as e:
                print(e)
        else:
            print("no data")

def trimDb(db=openConn()):
    ''' trim the db table to only hold TRIM_ROWS_TO amount of rows per mac in devices -table '''

    # create table saved_ids(id int);
    # insert into saved_ids (id) (SELECT ruuvi_log_id FROM ruuvi_log ORDER BY created desc LIMIT 10);
    # delete from ruuvi_log where ruuvi_log_id not in (select id from saved_ids);
    # drop table saved_ids;

    res = db.query('DROP TABLE saved_ids')
    logs = db['ruuvi_log'].count()
    macTable = db['device']
    rows = macTable.count()
    if(logs > (TRIM_ROWS_TO * rows) ):
        res = db.query('create table saved_ids(id int)')
        for mac in macTable.all():
            try:
                res = db.query('insert into saved_ids (id) (SELECT id \
                               FROM ruuvi_log WHERE device_id = %s ORDER BY \
                               created desc LIMIT %s);' % ( mac['id'], TRIM_ROWS_TO ))
            except Exception as e:
                print(e)
        res = db.query('delete from ruuvi_log where id not in (select id from saved_ids)')
        res = db.query('DROP TABLE saved_ids')



def insertMacs(macs,db=openConn()):
    '''
        insert valid macs for tags
        macs dict(mac=>'mac')
     '''
    if len(macs) < 1:
        raise Exception('no valid macs to insert')
    else:
        table = db['device']
        try:
            table.insert_many([macs])
        except Exception as e:
            log.error('could not insert MAC')
