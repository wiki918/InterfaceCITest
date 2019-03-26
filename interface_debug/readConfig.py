import os
import codecs
import configparser

proDir = os.path.split(os.path.realpath(__file__))[0]
#print("proDir",proDir)   #获取当前路径 D:\githome\python-oop
configPath = os.path.join(proDir, "config.ini")
#print(configPath)        #获取config.ini的路径 D:\githome\python-oop\config.ini

#读取和写入配置文件
class ReadConfig:
    def __init__(self):
        fd = open(configPath)
        data = fd.read()

        #  remove BOM # 判断是否为带BOM文件
        if data[:3] == codecs.BOM_UTF8: # 判断是否为带BOM文件
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()  #实例化configParser对象
        self.cf.read(configPath)  #用来读写配置文件.ini文件

    def get_email(self, name): #获取EMAIL分组下指定name的值
        value = self.cf.get("EMAIL", name)  #.get方法得到section中option的值，返回为string类型
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_headers(self, name):
        value = self.cf.get("HEADERS", name)
        return value

    def set_headers(self, name, value):
        self.cf.set("HEADERS", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)

    def get_url(self, name):
        value = self.cf.get("URL", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value


