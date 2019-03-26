
import os
import unittest
from comm.Log import MyLog as Log
import readConfig as readConfig
import HTMLTestRunner
from comm.configEmail import MyEmail

localReadConfig = readConfig.ReadConfig()


class AllTest:
    def __init__(self):
        global log, logger, resultPath, on_off
        log = Log.get_log()
        logger = log.get_logger()
        resultPath = log.get_report_path()
        on_off = localReadConfig.get_email("on_off")
        self.caseListFile = os.path.join(readConfig.proDir, "caselist.txt")  #E:\python自动化测试框架\interfaceTest\caselist.txt
        self.caseFile = os.path.join(readConfig.proDir, "testCase")
        # self.caseFile = None
        self.caseList = []
        self.email = MyEmail.get_email()

    # def set_case_list(self):
    #     """
    #     set case list
    #     :return:
    #     """
    #     fb = open(self.caseListFile)
    #     firstLine=""
    #
    #     lineOne = 1
    #     for value in fb.readlines():
    #         data = str(value)
    #         if (lineOne == 1):
    #             firstLine = data
    #
    #         lineOne += 1
    #
    #         #if data != '' and not data.startswith("#"):  #如果data不是null同时data不要以#开头
    #         self.caseList.append(firstLine+data.replace("\n", ""))   #将换行符替换掉保存在列表中
    #     fb.close()


    def set_case_list(self):
        """
        set case list
        :return:
        """
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):  #如果data不是null同时data不要以#开头
                self.caseList.append(data.replace("\n", ""))   #将换行符替换掉保存在列表中
        fb.close()
        #print(self.caseList)

    # 取test_case文件夹下所有用例文件
    def set_case_suite(self):
        """
        set case suite
        :return:
        """
        self.set_case_list()
        test_suite = unittest.TestSuite()  #定义单元测试容器
        suite_module = []

        for case in self.caseList:
            case_name = case.split("/")[-1]
            #print(case_name+".py")
            print("caseName",case_name)

            # discover 方法定义
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py', top_level_dir=None) #定搜索用例文件的方法
            suite_module.append(discover)  #将筛选出来的用例添加到suite_module存在列表中


        if len(suite_module) > 0:  #如果列表中有值

            #将discover方法筛选出来的用例，循环添加到测试套件中,打印出的用例信息会递增
            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTests(test_name)
        else:
            return None
        print("test_suite",test_suite)

        return test_suite  #返回单元测试容器：测试套件

    def run(self):
        """
        run test
        :return:
        """
        try:
            suit = self.set_case_suite()
            if suit is not None:
                logger.info("********TEST START********")
                fp = open(resultPath, 'wb')
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')
                runner.run(suit)
            else:
                logger.info("Have no case to test.")
        except Exception as ex:
            logger.error(str(ex))
        finally:
            logger.info("*********TEST END*********")
            fp.close()
            # send test report by email
            if on_off == 'on':
                self.email.send_email()
            elif on_off == 'off':
                logger.info("Doesn't send report email to developer.")
            else:
                logger.info("Unknow state.")


if __name__ == '__main__':
    obj = AllTest()
    obj.run()
