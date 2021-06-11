import time
import redis
from datetime import datetime

print("connect to redis...")


def message_handler(message):
    if type(message.get('data')) == str:
        print('---------------------\n' + str(datetime.now()))
        new_line = message.get('data')
        data = new_line.split(',')
        # print('%s yesterday price is: %s AND latest price is %s' % (data[1], data[6], data[10]))
        code = data[0]
        if data[2].startswith('T111'):
            price = round(float(data[6]), 2)
            swing = (float(data[8]) - float(data[9])) / price * 100
            if swing > 10:
                ct = datetime.now().strftime('%m月%d日') + \
                     '%s点%s分' % tuple(data[3][:5].split(':'))
                content = '{t}振幅达到{c}%，当前价{cp}，最高价{hp}，最低价{lp}，' \
                          '请关注公司股价波动原因'.format(t=ct, c=round(swing, 2), cp=price,
                                               hp=round(float(data[8]), 2),
                                               lp=round(float(data[9]), 2))
                print('{t}: {n} SWING {x} percent '.format(t=ct, n=data[1], x=swing))
            change = (float(data[10]) - price) / price * 100
            if change > 7 or change < -7:
                ct = datetime.now().strftime('%m月%d日') + \
                     '%s点%s分' % tuple(data[3][:5].split(':'))
                if change >= 9.9 or change <= -9.9:
                    content = '{t}{d}，最新价{x}，请关注公司股价变化原因'.format(
                        t=ct, d='涨停' if change > 0 else '跌停', x=price)
                else:
                    content = '{t}{d}达到{x}%，请关注公司股价变化原因'.format(
                        t=ct, d='上涨' if change > 0 else '下跌', x=round(change, 2))
                print('{t}: {n} CHANGE {x} percent '.format(t=ct, n=data[1], x=change))


r = redis.Redis(host='127.0.0.1', port=9379, charset='gbk', decode_responses=True)
p = r.pubsub()
p.subscribe('mdl.3.4.*')
print("receiving message...")
while datetime.now().minute < 50:
    message = p.get_message()
    if message:
        message_handler(message)
        # if type(message.get('data')) == str:
        #     print('---------------------\n' + str(datetime.now()))
        #     new_line = message.get('data')
        #     data = new_line.split(',')
        #     # print('%s yesterday price is: %s AND latest price is %s' % (data[1], data[6], data[10]))
        #     code = data[0]
        #     if data[2].startswith('T111'):
        #         price = round(float(data[6]), 2)
        #         swing = (float(data[8]) - float(data[9])) / price * 100
        #         if swing > 10:
        #             ct = datetime.now().strftime('%m月%d日') + \
        #                  '%s点%s分' % tuple(data[3][:5].split(':'))
        #             content = '{t}振幅达到{c}%，当前价{cp}，最高价{hp}，最低价{lp}，' \
        #                       '请关注公司股价波动原因'.format(t=ct, c=round(swing, 2), cp=price,
        #                                            hp=round(float(data[8]), 2),
        #                                            lp=round(float(data[9]), 2))
        #             print('{t}: {n} SWING {x} percent '.format(t=ct, n=data[1], x=swing))
        #         change = (float(data[10]) - price) / price * 100
        #         if change > 7 or change < -7:
        #             ct = datetime.now().strftime('%m月%d日') + \
        #                  '%s点%s分' % tuple(data[3][:5].split(':'))
        #             if change >= 9.9 or change <= -9.9:
        #                 content = '{t}{d}，最新价{x}，请关注公司股价变化原因'.format(
        #                     t=ct, d='涨停' if change > 0 else '跌停', x=price)
        #             else:
        #                 content = '{t}{d}达到{x}%，请关注公司股价变化原因'.format(
        #                     t=ct, d='上涨' if change > 0 else '下跌', x=round(change, 2))
        #             print('{t}: {n} CHANGE {x} percent '.format(t=ct, n=data[1], x=change))
    else:
        # print("waiting message...")
        time.sleep(0.001)
# while datetime.now().minute < 50:
# thread = p.run_in_thread(sleep_time=0.001)
print("END")
# thread.stop()
del p
del r
