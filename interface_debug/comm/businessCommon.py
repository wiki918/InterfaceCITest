from comm import common
from comm import configHttp
import readConfig as readConfig


localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localLogin_xls = common.get_xls_list("userCase.xlsx", "login")



# login(登录后拿到response)
def login():
    """
    login
    :return: token
    """
    # set url
    urlStr = common.get_url_from_xml('sign-in')  #/v2/User/Member/loginCommon
    #print(urlStr)
    #print(type(urlStr))
    localConfigHttp.set_url(str(urlStr))   #http://10.255.12.58080/zhuanle/v2/User/Member/loginCommon
    #print(aa)


    # set header

    X_KJT_Agent = localReadConfig.get_headers("X-KJT-Agent")
    X_DEV_Label=localReadConfig.get_headers("X-DEV-Label")

    header = {"X-KJT-Agent": X_KJT_Agent,"X-DEV-Label":X_DEV_Label}
    localConfigHttp.set_headers(header)


    # set param
    data = {"account": localLogin_xls[0][3],  #取到account  18300005502
            "password": localLogin_xls[0][4]}  #取到password  ww123456
    #print(data)
    localConfigHttp.set_data(data)

    #check此次请求是post还是get请求
    # response1 = localConfigHttp.post()
    # print("url",response1.url,response1.text)
    # method = str(response1.request)[int(str(response1.request).find('['))+1:int(str(response1.request).find(']'))]
    # print("method",method)


    # login
    response = localConfigHttp.post().json()

    # cc=int(method.find('['))+1
    # dd=int(method.find(']'))
    # print("cc",cc)
    # print("dd",dd)
    # print('str2',method[cc:dd])
    #info = response.json()
    # print(response)
    #print(response["body"]["token"])
    #return response["body"]["token"]
    #token = common.get_value_from_return_json(response, "body", "token")
    #print("busines",token)
    token=common.get_value_from_return_json(response,"body","auth")
    #print(token)
    return token
    #print("login",token)



#logout
def logout(token):
    """
    logout
    :param token: login token
    :return:
    """
    # set url
    url = common.get_url_from_xml('logout')
    localConfigHttp.set_url(url)

    # set header

    X_KJT_Agent = localReadConfig.get_headers("X-KJT-Agent")
    X_DEV_Label=localReadConfig.get_headers("X-DEV-Label")
    X_KJT_Auth=token

    header = {"X-KJT-Agent": X_KJT_Agent,"X-DEV-Label":X_DEV_Label,'X-KJT-Auth':X_KJT_Auth}
    localConfigHttp.set_headers(header)


    # logout
    localConfigHttp.post()

    #调登出操作后把配置文件里的token_v置为null
    X_KJT_Auth=""
    localReadConfig.set_headers("token_u",X_KJT_Auth)






