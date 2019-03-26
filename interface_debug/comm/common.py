import requests
import readConfig as readConfig
import os
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree
from comm import configHttp as configHttp
from comm.Log import MyLog as Log
import json

localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
print(proDir)
localConfigHttp = configHttp.ConfigHttp()
log = Log.get_log()
logger = log.get_logger()

caseNo = 0



#登录操作获取token
def get_visitor_token():
    urlStr=get_url_from_xml('sign-in')
    #print("urlStr",urlStr)
    localConfigHttp.set_url(str(urlStr))
    #print(aa)

    # set header

    X_KJT_Agent = localReadConfig.get_headers("X-KJT-Agent")
    X_DEV_Label=localReadConfig.get_headers("X-DEV-Label")

    header = {"X-KJT-Agent": X_KJT_Agent,"X-DEV-Label":X_DEV_Label}
    localConfigHttp.set_headers(header)

    # set param
    data = {"account": get_xls("userCase.xlsx","login")[0][3],  #取到account  18300005502
            "password": get_xls("userCase.xlsx","login")[0][4]}  #取到password  ww123456
    #print(data)
    localConfigHttp.set_data(data)

    response = localConfigHttp.post().json()

    token=get_value_from_return_json(response,"body","auth")
    return token
    #print("login",token)

def get_value_from_return_json(json, name1, name2):
    """
    get value by key
    :param json:
    :param name1:
    :param name2:
    :return:
    """
    #info = json['info']
    group = json[name1]
    value = group[name2]
    return value

#拿到token放在配置文件里
def set_visitor_token_to_config():
    """
    set token that created for visitor to config
    :return:
    """
    token_v=get_visitor_token()
    #print("token_v121212",token_v)
    localReadConfig.set_headers("TOKEN_V", token_v)

#解析一些response
def show_return_msg(response):
    """
    show msg detail
    :param response:
    :return:
    """
    url = response.url
    msg = response.text
    print("\n请求地址："+url)
    # 可以显示中文
    print("\n请求返回值："+'\n'+json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))
# ****************************** read testCase excel ********************************

# 从excel文件中读取测试用例
def get_xls_list(xls_name, sheet_name):
    """
    get interface data from xls file
    :return:列表
    共调登录接口获取用户名和密码
    """
    #返回列表
    cls = []
    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)  #获取xls文件路径:
    # open xls file
    file = open_workbook(xlsPath)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows  #获取总行数 7
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':  #第一行第一列
            cls.append(sheet.row_values(i))

    return cls


def get_xls(xls_name, sheet_name):
    """
    get interface data from xls file
    :return:元组
    """
    #返回元组
    allList = []
    allTuple = ()
    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)  # 获取xls文件路径:
    # open xls file
    file = open_workbook(xlsPath)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows  # 获取总行数 7
    row1 = sheet.row_values(0)  # 第一行  #['case_name', 'method', 'token', 'email', 'password', 'result', 'code', 'msg']
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':  # 第一行第一列
            subList = []
            ccount = len(sheet.row_values(i))  #8
            for ii in range(ccount):
                lastList = []
                lastList.append(row1[ii])
                lastList.append(sheet.row_values(i)[ii])
                subList.append(lastList)
            #print(subList)

            # print(dict(subList))
            allList.append(dict(subList))

    allTuple = tuple(allList)
    return allTuple
    # print("allTuple",allTuple)

# ****************************** read SQL xml ********************************
database = {}


def set_xml():
    """
    set sql xml
    :return:
    """
    if len(database) == 0:
        sql_path = os.path.join(proDir, "testFile", "SQL.xml")
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            # print(db_name)
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                # print(table_name)
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    # print(sql_id)
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table


def get_xml_dict(database_name, table_name):
    """
    get db dict by given name
    :param database_name:
    :param table_name:
    :return:
    """
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict


def get_sql(database_name, table_name, sql_id):
    """
    get sql by given name and sql_id
    :param database_name:
    :param table_name:
    :param sql_id:
    :return:
    """
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql
# ****************************** read interfaceURL xml ********************************

def get_url_from_xml(name):
    """
    By name get url from interfaceURL.xml
    :param name: interface's url name
    :return: url
    """
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')  #D:\githome\python-oop\testFile\interfaceURL.xml
    tree = ElementTree.parse(url_path)  #拿到xml.etree.ElementTree.ElementTree object
    for u in tree.findall('url'):
        url_name = u.get('name')
        #print(url_name)
        if url_name == name:
            for c in u.getchildren():
                url_list.append(c.text)
                print(url_list)
    url ='/'+'/'.join(url_list)

    return url   #/v2/User/Member/loginCommon
    #print("url",url)


if __name__ == "__main__":
    print(get_xls("login"))
    set_visitor_token_to_config()


    # get_xls("userCase.xlsx","login")
    # #get_visitor_token()
    # get_url_from_xml("sign-in")
    # set_visitor_token_to_config()
    # #get_value_from_return_json()
    # get_visitor_token()
