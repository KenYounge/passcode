import uuid
from datetime import datetime

EMERGENCY_SMS = '1-415-555-1212'
SQL_PASSWORD = "Example!password4SQL"

def golden_ratio():
    ratio = ( 1 + (5 ** 0.5)) / 2
    return ratio

def timestamp_uuid():
    return str(str(datetime.now()) + '_' + str(uuid.uuid4())).replace(' ','_')