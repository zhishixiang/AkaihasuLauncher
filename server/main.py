from flask import Flask
import psutil
import time
import threading
from loguru import logger

app = Flask(__name__)
accurateSpeed = 0
averageSpeed = 0


def getNet():
    while True:
        speedSum = 0
        for i in range(0, 10):
            sent_before = psutil.net_io_counters().bytes_sent  # 已发送的流量
            recv_before = psutil.net_io_counters().bytes_recv  # 已接收的流量
            time.sleep(2)
            sent_now = psutil.net_io_counters().bytes_sent
            recv_now = psutil.net_io_counters().bytes_recv
            sent = (sent_now - sent_before) / 1024  # 算出1秒后的差值
            recv = (recv_now - recv_before) / 1024
            logger.info(time.strftime(" [%Y-%m-%d %H:%M:%S] ", time.localtime()))
            logger.info("上传：{0}KB/s".format("%.2f" % sent))
            logger.info("下载：{0}KB/s".format("%.2f" % recv))
            global accurateSpeed
            accurateSpeed = round((sent + recv) / 2, 2)
            logger.info("平均速度：%sKB/s" % accurateSpeed)
            logger.info('-' * 32)
            speedSum += accurateSpeed
        print("10轮平均速度：%sKB/s" % round(speedSum / 10, 2))
        global averageSpeed
        averageSpeed = round(speedSum / 10, 2)


@app.route('/accurate')
def accurate():
    return str(accurateSpeed)


@app.route('/average')
def average():
    return str(averageSpeed)


if __name__ == "__main__":
    t1 = threading.Thread(target=getNet)
    t1.start()
    app.run(host="0.0.0.0", port=8080, debug=True)
