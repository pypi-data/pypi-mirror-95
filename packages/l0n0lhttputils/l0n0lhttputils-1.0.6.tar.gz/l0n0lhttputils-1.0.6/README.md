# http服务开发经常用到的库集合(持续更新，第一版写的简单)

## 1.包含内容
### dbmysql mysql数据库权限控制，可用于前端直接执行mysql
### http_server 基于aiohttp的http服务器
### tencent_cos 腾讯对象存储
### token_mgr 用于管理token
### wx_gzh 用于处理微信公众号开发获取授权信息

## 2.使用文档

### 安装
```
pip install l0n0lhttputils
```

### 使用方法，以微信登录验证为例
```python
import logging
import asyncio
import requests

from l0n0lhttputils.config_file import yaml_file
from l0n0lhttputils.http_server import http_server, web
from l0n0lhttputils.dbmysql import dbmysql
from l0n0lhttputils.token_mgr import token_mgr, check_token

g_config = yaml_file("config.yaml")
g_config.load_config()

db = dbmysql(
    g_config.get("mysql_host"),
    g_config.get("mysql_port"),
    g_config.get("mysql_user"),
    g_config.get("mysql_password"),
    g_config.get("mysql_db")
)

# 用户csrf token
g_token_mgr: token_mgr = token_mgr()
g_token_mgr.token_timestamp = g_config.get("token_expire_time")

g_server = http_server(g_config.get("listen_host"),
                       g_config.get("listen_port"))
session_keys = {}

@g_server.route("post", "/{prefix}/login")
async def login(request: web.Request):
    """用户登录
    @code:微信提供的code
    """
    # 获取用户的微信code
    request_data = await request.json()

    # 向微信验证用户的code是否正确，并获取用户的openid
    check_result = requests.get("https://api.weixin.qq.com/sns/jscode2session", params={
        'appid': config.get("appid"),
        "secret": config.get("secret_key"),
        "js_code": request_data['code'],
        "grant_type": 'authorization_code'
    })

    # 判断验证时网络是否正常
    if check_result.status_code != 200:
        return web.json_response({"errMsg": "向微信检查登录状态错误"})

    # 获取微信的验证结果，openid
    json_value = check_result.json()
    openid = json_value['openid']

    # 生成本次会话的token，防止csrf攻击
    token = g_token_mgr.gen_token(openid)

    # 保存会话key
    session_keys[openid] = json_value['session_key']

    # 检测是否有该用户,没有则创建该用户
    db.post("insert into `users` (`openid`) values (%s) on duplicate key update `openid` = values(`openid`)",
            [openid])

    # 验证成功，把会话token返回给用户
    return web.json_response({
        "errMsg": "OK",
        "token": token,
    })


@g_server.route("post", "/{prefix}/user_data")
@check_token(g_token_mgr) # check_token 会检测用户http请求中的  header中是否有 "token" header 
async def user_data(request: web.Request):
    """
    获取用户基本数据
    """
    data = db.get("select * from `users` where `openid` = %s",
                  [request.openid])
    if not data:
        return web.json_response({
            "errMsg": "服务器错误"
        })

    # 验证成功，把会话token返回给用户
    return web.json_response({
        "errMsg": "OK",
        "data": data,
    })

def update_test(cost):
    print(cost)

async def update_test_async(cost):
    print(cost)


async def main():
    #####################设置log#################################
    logging.basicConfig(filename="testserver.log", level=logging.INFO)
    ####################向主循环添加自己的更新函数#################
    g_server.update_elapse = 0.1 # 设置主循环更新时间(默认0.1)
    g_server.add_update_func(update_test)
    g_server.add_async_update_func(update_test_async)
    #############################################################
    await g_server.common_run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
```