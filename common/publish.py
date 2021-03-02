import redis
from datetime import datetime


rc = redis.Redis()
with open('/home/ycw/mdl/linux/msg_backup/20190312/mdl_3_4_0.csv', 'r', encoding='gbk') as f:
    for line in f:
        data = line.split(',')
        if not data[2].startswith('T111'):
            continue
        channel = 'mdl.3.4.' + data[1]
        rc.publish(channel, line)
print(datetime.now())
