import socket
import time
import select
from datetime import datetime

# Create a TCP/IP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('127.0.0.1', 8083)
print('connecting to %s port %s' % server_address)
try:
    client.connect(server_address)
except Exception as e:
    print(e)

epoll = select.epoll()
epoll.register(client.fileno(), select.EPOLLIN)

while True:

    # Receive data
    # new_line = client.recv(1024).decode()
    events = epoll.poll(1)
    print(datetime.now(), events)
    for fileno, event in events:
        if fileno == client.fileno():
            print(event)
            new_line = client.recv().decode()
            # if new_line:
            #     print(new_line)
            #     data = new_line.split(',')
            #     # print('%s yesterday price is: %s AND latest price is %s' % (data[1], data[6], data[10]))
            #     code = data[0]
            #     count = data[-1]
            #     if data[2].startswith('T'):
            #         price = round(float(data[6]), 2)
            #         swing = (float(data[8]) - float(data[9])) / price * 100
            #         if swing > 10:
            #             ct = datetime.now().strftime('%m月%d日') + \
            #                  '%s点%s分' % tuple(data[3][:5].split(':'))
            #             content = '{t}振幅达到{c}%，当前价{cp}，最高价{hp}，最低价{lp}，' \
            #                       '请关注公司股价波动原因'.format(t=ct, c=round(swing, 2), cp=price,
            #                                            hp=round(float(data[8]), 2),
            #                                            lp=round(float(data[9]), 2))
            #             print('【{c}】 {t}: {n} SWING {x} percent '.format(c=count, t=ct, n=data[1], x=swing))
            #         change = (float(data[10]) - price) / price * 100
            #
            #         if change > 7 or change < -7:
            #             ct = datetime.now().strftime('%m月%d日') + \
            #                  '%s点%s分' % tuple(data[3][:5].split(':'))
            #             if change >= 9.9 or change <= -9.9:
            #                 content = '{t}{d}，最新价{x}，请关注公司股价变化原因'.format(
            #                     t=ct, d='涨停' if change > 0 else '跌停', x=price)
            #             else:
            #                 content = '{t}{d}达到{x}%，请关注公司股价变化原因'.format(
            #                     t=ct, d='上涨' if change > 0 else '下跌', x=round(change, 2))
            #                 print('【{c}】 {t}: {n} CHANGE as {x} percent '.format(c=count, t=ct, n=data[1], x=change))
            time.sleep(0.5)

    # finally:
    #     print('closing socket')
    #     client.close()
