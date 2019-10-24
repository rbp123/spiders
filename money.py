import  threading
import time
import random

gMoney = 1000
Times = 10
times = 0
glock = threading.Condition()
class S(threading.Thread):
    def run(self):
       while True:
           global gMoney,times
           glock.acquire()
           if times > Times:
               glock.release()
               break
           money = random.randint(100, 1000)
           gMoney += money
           glock.notify_all()
           print('%s生产者生产了%d,还剩%d' % (threading.current_thread(), money,gMoney))
           time.sleep(0.5)
           times += 1
           glock.release()

class X(threading.Thread):
    def run(self):
        global gMoney
        while True:
            money = random.randint(100,1000)
            glock.acquire()
            if money <= gMoney :
                glock.wait()
                gMoney -= money
                print('%s消费者消费了%d,还剩%d' %(threading.current_thread(),money,gMoney))
                time.sleep(0.5)
                glock.release()
            else:
                if times > Times:
                    print('钱不够了')
                    glock.release()
                    break



def main():
    for x in range(5):
        t = S(name='生产者%d:'% x)
        t.start()
    for x in range(3):
         t = X(name='消费者%d:'% x)
         t.start()

if __name__ == '__main__':
    main()