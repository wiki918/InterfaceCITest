import unittest
import paramunittest
import readConfig as readConfig
from comm import Log as Log
from comm import common
from comm import configHttp as ConfigHttp

login_xls = common.get_xls("userCase.xlsx", "login")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


# @paramunittest.parametrized(
#     {'case_name': 'login', 'method': 'post', 'token': '0', 'account': '18300005502', 'password': 'ww123456',
#      'result': '0', 'code': '0', 'msg': '正常处理'},
#     {'case_name': 'login_PasswordError', 'method': 'post', 'token': '0', 'account': '18300005502', 'password': 'ww12345',
#      'result': '0', 'code': '9999', 'msg': '请输入正确的登录密码'},
# )
@paramunittest.parametrized(*login_xls)  # 从数组中获取用例，我的方法是先将用例写到excel中，再读取excel获取用例组
class TestLogin(unittest.TestCase):
    def setParameters(self, case_name, method, token, account, password, result, code, msg):
        print("firstfirstfirstfirstfirstfirstfirstfirstfirstfirstfirstfirstfirst")
        """
        set params
        :param case_name:
        :param method:
        :param token:
        :param account:
        :param password:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)  # 转化成字符串
        self.method = str(method)
        self.token = str(token)
        self.account = str(account)
        self.password = str(password)
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
        self.return_json = None
        self.info = None

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """
        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name+"测试开始前准备")

    # def testHello(self):
    #     print("aaaaaaaaaaaaaaaaaaaa")

    def testLogin(self):
        global auth
        """
        test body
        :return:
        """
        print("---进入testlogin方法测试---")
        # set url
        self.url = common.get_url_from_xml('sign-in')
        configHttp.set_url(self.url)
        print("第一步：设置url  " + self.url)

        # get visitor token
        # if self.token == '0':  #如果token=0 就取token；1的话就不取token
        #     token = localReadConfig.get_headers("token_v")
        # elif self.token == '1':
        #     token = ""

        # 请求头里是否需要传auth(后台传0代表不需要传；为1代表需要传auth)
        X_KJT_Auth=None
        if self.token == '0':  # 不需要传auth
            X_KJT_Auth = None
        elif self.token == '1':  # 需要传auth
            X_KJT_Auth = localReadConfig.get_headers("token_u")

        # set headers
        X_KJT_Agent = localReadConfig.get_headers("X-KJT-Agent")
        X_DEV_Label = localReadConfig.get_headers("X-DEV-Label")
        auth = str(X_KJT_Auth)
        header = {"X-KJT-Agent": X_KJT_Agent, "X-DEV-Label": X_DEV_Label, "X-KJT-Auth": auth}
        configHttp.set_headers(header)
        print("第二步：设置header(token等)")

        # set params
        data = {"account": self.account, "password": self.password}
        configHttp.set_data(data)
        print("第三步：设置发送请求的参数")

        # test interface
        self.return_json = configHttp.post()
        method = str(self.return_json.request)[
                 int(str(self.return_json.request).find('[')) + 1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法：" + method)

        # check result
        self.checkResult()
        print("第五步：检查结果")

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()  # self.info是{...}
        # show return message
        common.show_return_msg(self.return_json)

        if self.result == '0':
            # account = common.get_value_from_return_json(self.info, 'body', 'account')   #查看response里返回的account信息
            self.assertEqual(str(self.info['status']), self.code)
            self.assertIn(self.msg,self.info['message'])  # 判断是字符串是否包含（实际包含期望）
            # self.assertEqual(account, self.account)

        if self.result == '1':
            self.assertEqual(str(self.info['status']), self.code)
            self.assertIn(self.msg, self.info['message'])

    def tearDown(self):
        """
        :return:
        """
        info = self.info
        if str(info['status']) == "0":
            # get uer token
            token_u = common.get_value_from_return_json(info, 'body', 'auth')
            # set user token to config file
            localReadConfig.set_headers("TOKEN_U", token_u)
        else:
            pass
        self.log.build_case_line(self.case_name, str(self.info['status']), self.info['message'])
        print("测试结束，输出log完结\n\n")


if __name__ == '__main__':
    unittest.main(verbosity=2)
