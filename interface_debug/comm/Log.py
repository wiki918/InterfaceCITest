import os
import readConfig as readConfig
import logging
from datetime import datetime
import threading

localReadConfig = readConfig.ReadConfig()


class Log:
    def __init__(self):
        global logPath, resultPath, proDir
        proDir = readConfig.proDir
        resultPath = os.path.join(proDir, "result")
        if not os.path.exists(resultPath):  # create result file if it doesn't exist
            os.mkdir(resultPath)
        logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d%H%M%S"))) #定义log存放路径
        if not os.path.exists(logPath):# create log file if it doesn't exist
            os.mkdir(logPath)
        self.logger = logging.getLogger() # defined logger
        self.logger.setLevel(logging.INFO) # defined log level

        # defined handler
        handler = logging.FileHandler(os.path.join(logPath, "output.log"))
        # defined formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        """
        get logger
        :return:
        """
        return self.logger

    def build_start_line(self, case_no):
        """
        write start line
        :return:
        """
        self.logger.info("--------" + case_no + " START--------")

    def build_end_line(self, case_no):
        """
        write end line
        :return:
        """
        self.logger.info("--------" + case_no + " END--------")

    def build_case_line(self, case_name, code, msg):
        """
        write test case line
        :param case_name:
        :param code:
        :param msg:
        :return:
        """
        self.logger.info(case_name+" - Code:"+code+" - msg:"+msg)

    def get_report_path(self):
        """
        get report file path
        :return:
        """
        report_path = os.path.join(logPath, "report.html")
        return report_path

    def get_result_path(self):
        """
        get test result path
        :return:
        """
        return logPath

    def write_result(self, result):
        """

        :param result:
        :return:
        """
        result_path = os.path.join(logPath, "report.txt")
        fb = open(result_path, "wb")
        try:
            fb.write(result)
        except FileNotFoundError as ex:
            logger.error(str(ex))

#单独启用了一个线程，这样在整个运行过程中，我们在写log的时候也会比较方便
#对输出的日志的所有操作了，主要是对输出格式的规定，输出等级的定义以及其他一些输出的定义等等。总之，你想对log做的任何事情，都可以放到这里来。我们来看下代码，没有比这个更直接有效的了。
class MyLog:
    log = None

    #.lock()” 互斥锁” 的标记，这个标记用来保证在任一时刻，只能有一个线程访问该对象。
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod  #静态方法
    def get_log():

        if MyLog.log is None:
            MyLog.mutex.acquire()  #抢占这把锁
            MyLog.log = Log()
            MyLog.mutex.release()

        return MyLog.log

if __name__ == "__main__":
    log = MyLog.get_log()  #得到log对象
    logger = log.get_logger()
    logger.debug("test debug")
    logger.info("test info")

