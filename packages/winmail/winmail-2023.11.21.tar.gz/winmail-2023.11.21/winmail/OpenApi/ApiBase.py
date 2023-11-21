# -*- coding:utf-8 -*-
from enum import Enum
from typing import Dict, Optional, Any, Union
from pydantic import Field
from winmail.OpenApi import OpenApi


class AuthType(str, Enum):
    """用户认证类型

    internal = 内部认证
    nt = NT认证
    third_party = 第三方认证
    """
    internal = '0'
    nt = '1'
    third_party = '2'


class UserStatus(str, Enum):
    """用户状态

    normal = 正常
    disabled = 禁止
    pending = 待审核
    paused = 暂停
    """

    normal = '0'
    disabled = '1'
    pending = '2'
    paused = '3'


class Base(OpenApi):

    def __init__(self, server: str, port: int, apikey: str, apisecret: str, use_ssl: bool = False) -> None:
        """
        初始化OpenApi接口

        :param server: 服务器地址
        :param port:  端口
        :param apikey: APIkey
        :param apisecret: API密钥
        :param use_ssl:  是否使用SSL端口
        :return: None
        """
        super().__init__(server, port, apikey, apisecret, use_ssl)
        self.login_status = False
        self.login_result = None

    # #####通用接口开始
    def login(self, user: str, pwd: str, manage_path: Optional[str] = '', tid: int = 0) -> Dict[str, Any]:
        """ 登陆认证

        登陆并修改登陆状态login_status,保存sessid。

        :param user: 认证邮箱用户名
        :param pwd:  密码
        :param manage_path: 调用管理端接口请写入管理地址，用户端调用请忽略，【winmail管理工具中系统设置-高级设置-系统参数-HTTP配置中查看】
        :param tid: 用户端调用参数，手机风格6，否则默认为0。参考web代码中用户登陆风格。
        :return: Dict
            管理端返回：
            {
                "result": "ok",
                "info":
                {
                    “ sessid ”:  "efd24f9f63d69d6f6f169b235822ca5875eb2bae",
                    “ user ”:  "admin"
                }
            }
            用户端返回：
            {
            "result": "ok",
            "info":
                {
                “ sessid ”:  "1a2db1b0edda735295508723d8c6a962",
                “uid”: "test",
                “email”: " test@cnu.com ",
                “fullname”: "测试用户",
                “mobile”: "13900000000",
                “company”: "华兆科技",
                “department”: "系统研发部",
                “jobtitle”: "工程帅",
                “office”: "",
                “officephone”: "",
                “homeaddress”: "",
                “homephone”: "",
                }
            }
        """

        self.login_result = super().login(user, pwd, manage_path=manage_path, tid=tid)

        if self.login_result['result'] == 'ok':
            self.login_status = True

        return self.login_result

    def updatesession(self):
        """更新会话

        更新Sessid，sessid默认为30分钟超时。
        :return: bool
        """
        return self.update_session()

    # #####管理端接口开始
    def domain(self, pageno: Optional[int] = 0) -> Dict[str, Any]:
        """ 获取域名

        取所有域名列表

        :param pageno: 分页序号，以 0 开始
        :return: Dict
            {
            "result": "ok",
            "info":
                {
                “ domains ”: 域名列表 ,
                “ totalcount ”: 域名总数
                “ pagecount ”:  分页总数
                }
            }
        """

        method_params = {"sessid": self.sessid, "method": "domain"}
        method_params.update({"pageno": str(pageno)})

        return self.get_api(**method_params)

    def domain_added(self, domain: str,
                     description: Optional[str] = None,
                     mailquota: Optional[int] = None,
                     mailcount: Optional[int] = None,
                     ftpquota: Optional[int] = None,
                     ftpcount: Optional[int] = None,
                     **kwargs: Optional[Dict]
                     ) -> Dict[str, Any]:
        """ 新增域名

        新增域名接口

        :param domain: 域名
        :param description: 描述
        :param mailquota: 新邮箱默认空间大小,单位 MB
        :param mailcount: 新邮箱默认最多邮件数
        :param ftpquota: 新邮箱默认网络磁盘空间大小
        :param ftpcount: 新邮箱默认网络磁盘最多文件数
        :param kwargs: 其他可能参数
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            -1  域名数已经达到允许注册数
            1  域名新增失败
            2  相同的域名已经存在
            3  相同的域别名已经存在
            4  相同的 NT 认证域名已经存在
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self.sessid, "method": "domain.added"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue
            if k == "kwargs":
                method_params.update(kwargs)
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self.get_api(**method_params)

    def domain_edited(self, domain: str,
                      description: Optional[str] = None,
                      mailquota: Optional[int] = None,
                      mailcount: Optional[int] = None,
                      ftpquota: Optional[int] = None,
                      ftpcount: Optional[int] = None,
                      **kwargs: Optional[Dict]
                      ) -> Dict[str, Any]:
        """ 修改域名

        修改指定域名

        :param domain: 域名
        :param description: 描述
        :param mailquota: 新邮箱默认空间大小,单位 MB
        :param mailcount: 新邮箱默认最多邮件数
        :param ftpquota: 新邮箱默认网络磁盘空间大小
        :param ftpcount: 新邮箱默认网络磁盘最多文件数
        :param kwargs: 其他可能参数
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  域名修改失败
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self.sessid, "method": "domain.edited"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue
            if k == "kwargs":
                method_params.update(kwargs)
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self.get_api(**method_params)

    def domain_delete(self, domain: str) -> Dict[str, Any]:
        """ 删除域名

        删除指定域名

        :param domain: 要删除的域名
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            errno  值  含义
            -1  域名数已经达到允许注册数。
            1  域名删除失败
            2  此域名下存在邮箱，请先删除域下用户，别名和组
            3  主域名不能被删除
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self.sessid, "method": "domain.delete"}
        method_params.update({"domain": domain})

        return self.get_api(**method_params)

    def user(self, domain: str, pageno: Optional[int] = 0) -> Dict[str, Any]:
        """ 获取用户列表

        获取指定域名下用户列表

        :param domain: 域名
        :param pageno: 分页序号，以 0 开始
        :return: 成功返回值
            {
            "result": "ok",
            "info":
                {
                “ users ”: 邮箱用户列表 ,
                “ totalcount ”: 用户总数
                “ pagecount ”:  分页总数
                “ domain ”:  所属域名
                }
            }
        """

        method_params = {"sessid": self.sessid, "method": "user"}
        method_params.update({"domain": domain, "pageno": str(pageno)})

        return self.get_api(**method_params)

    def user_added(self, name: str,
                   domain: str,
                   password: str,
                   authtype: Union[AuthType, int] = Field(AuthType.internal),
                   status: Optional[Union[UserStatus, int]] = Field(UserStatus.normal),
                   fullname: Optional[str] = None,
                   description: Optional[str] = None,
                   homeaddress: Optional[str] = None,
                   homephone: Optional[str] = None,
                   mobile: Optional[str] = None,
                   company: Optional[str] = None,
                   department: Optional[str] = None,
                   jobtitle: Optional[str] = None,
                   office: Optional[str] = None,
                   officephone: Optional[str] = None,
                   mailquota: Optional[int] = None,
                   mailcount: Optional[int] = None,
                   ftpquota: Optional[int] = None,
                   ftpcount: Optional[int] = None,
                   **kwargs: Optional[Dict]
                   ) -> Dict[str, Any]:
        """ 新增用户

        管理员新增邮箱用户接口。

        :param name: 邮箱用户名
        :param domain: 域名
        :param password: 邮箱密码
        :param authtype: 认证方式 0 - 本系统认证； 1 - NT 域认证； 2 - 第三方认证
        :param status: 状态 0 - 正常；1 - 禁止；2 - 等待审核
        :param fullname: 用户姓名
        :param description: 描述
        :param homeaddress: 家庭地址
        :param homephone: 电话电话
        :param mobile: 手机
        :param company: 工作单位
        :param department: 部门
        :param jobtitle: 职位
        :param office: 办公室
        :param officephone: 办公电话
        :param mailquota: 邮箱空间大小 单位MB
        :param mailcount: 邮箱最多邮件数
        :param ftpquota: 网络磁盘空间大小 单位MB
        :param ftpcount: 网络磁盘最多文件数
        :param kwargs: 其他参数
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            -1  用户数已经达到允许注册数
            1  用户新增失败
            2  相同的用户已经存在
            3  相同的用户别名已经存在
            4  相同的邮件组已经存在
            6  此域下用户邮箱数已经达到本域允许的注册数
            7  此域下用户邮箱容量已经达到本域允许的总容量
            8  此域下用户网络磁盘容量已经达到本域允许的总容量
            101  主服务器增加用户失败
            102  主服务器上相同的用户已经存在
            103  主服务器上相同的用户别名已经存在
            104  主服务器上相同的邮件组已经存在
            99  您没有权限进行此项操作
        """
        method_params = {"sessid": self.sessid, "method": "user.added"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue
            if k == "kwargs":
                method_params.update(kwargs)
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self.get_api(**method_params)

    def user_edited(self, name: str,
                    domain: str,
                    password: Optional[str] = None,
                    changedpwd: Optional[int] = 0,
                    authtype: Optional[Union[AuthType, int]] = Field(default=AuthType.internal),
                    status: Optional[Union[UserStatus, int]] = Field(default=UserStatus.normal),
                    fullname: Optional[str] = None,
                    description: Optional[str] = None,
                    homeaddress: Optional[str] = None,
                    homephone: Optional[str] = None,
                    mobile: Optional[str] = None,
                    company: Optional[str] = None,
                    department: Optional[str] = None,
                    jobtitle: Optional[str] = None,
                    office: Optional[str] = None,
                    officephone: Optional[str] = None,
                    mailquota: Optional[int] = None,
                    mailcount: Optional[int] = None,
                    ftpquota: Optional[int] = None,
                    ftpcount: Optional[int] = None,
                    **kwargs: Optional[Dict]
                    ) -> Dict[str, Any]:
        """ 修改用户

        管理员修改邮箱用户接口。*如果要修改密码，增加参数 changedpwd ，值设置为 1

        :param name: 邮箱用户名
        :param domain: 域名
        :param password: 邮箱密码
        :param changedpwd: 是否修改密码
        :param authtype: 认证方式 0 - 本系统认证； 1 - NT 域认证； 2 - 第三方认证
        :param status: 状态 0 - 正常；1 - 禁止；2 - 等待审核
        :param fullname: 用户姓名
        :param description: 描述
        :param homeaddress: 家庭地址
        :param homephone: 电话电话
        :param mobile: 手机
        :param company: 工作单位
        :param department: 部门
        :param jobtitle: 职位
        :param office: 办公室
        :param officephone: 办公电话
        :param mailquota: 邮箱空间大小 单位MB
        :param mailcount: 邮箱最多邮件数
        :param ftpquota: 网络磁盘空间大小 单位MB
        :param ftpcount: 网络磁盘最多文件数
        :param kwargs: 其他参数
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  用户修改失败
            99  您没有权限进行此项操作
        """
        method_params = {"sessid": self.sessid, "method": "user.edited"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue
            if k == "kwargs":
                method_params.update(kwargs)
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self.get_api(**method_params)

    def user_delete(self, name: str, domain: str) -> Dict[str, Any]:
        """删除用户

        删除邮箱用户
        :param name: 邮箱用户名
        :param domain: 域名
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  用户删除失败
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self.sessid, "method": "user.delete"}
        method_params.update({"name": name, "domain": domain})

        return self.get_api(**method_params)

    def group(self, domain: str, pageno: Optional[int] = 0) -> Dict[str, Any]:
        """取邮件组列表

        :param domain: 域名
        :param pageno: 页数
        :return: 成功返回值
            {
                "result": "ok",
                "info":
                {
                    “ groups ”: 邮箱用户列表 ,
                    “ totalcount ”: 用户总数
                    “ pagecount ”:  分页总数
                    “ domain ”:  所属域名
                }
            }
        """

        method_params = {"sessid": self.sessid, "method": "group"}
        method_params.update({"pageno": str(pageno), "domain": domain})

        return self.get_api(**method_params)

    def group_added(self,
                    name: str,
                    domain: str,
                    fullname: Optional[str] = None,
                    description: Optional[str] = None,
                    subgroup: Optional[str] = None,
                    members: Optional[str] = None,
                    sendmailright: Optional[int] = 0,
                    sendmailmembers: Optional[str] = None,
                    managers: Optional[str] = None,
                    visibleright: Optional[int] = 0,
                    sendervisible: Optional[bool] = True,
                    **kwargs: Optional[Dict]
                    ) -> Dict[str, Any]:
        """新增邮件组

        :param name: 组名
        :param domain: 域名
        :param fullname: 组名称
        :param description: 描述
        :param subgroup: 子分组，各子分组名以分号(;)分
        :param members: 组成员  各成员名以分号(;)分隔
        :param sendmailright: 发信权限
            0 - 任何人都可以给组员发
            信；
            1 - 只有组员可以发信；
            2 - 仅指定成员可以发信；
            3 - 本域下用户可以发信
        :param sendmailmembers: 发信成员  各发信成员名以分号(;)分隔
        :param managers: 组管理员  各组管理员名以分号(;)分隔
        :param visibleright: 可见权限
            0 - 任何人可以看到此通讯组及其成员；
            1 - 任何人可以看到此通讯组；
            2 - 本域用户可以看到此通讯组及其成员；
            3 - 域用户可以看到此通讯组；
            4 - 组成员可以看到此通讯组及其成员；
            5 - 组成员可以看到此通讯组；
            6 - 只有管理员可以看到此通讯组及成员
        :param sendervisible: 发信成员可见
            0 - 没有特别可见权限；
            1 - 发信成员有相同的可见度。
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  组新增失败
            2  相同的用户已经存在
            3  相同的用户别名已经存在
            4  相同的邮件组已经存在
            101  主服务器增加用户失败
            102  主服务器上相同的用户已经存在
            103  主服务器上相同的用户别名已经存在
            104  主服务器上相同的邮件组已经存在
            99  您没有权限进行此项操作


        """

        method_params = {"sessid": self.sessid, "method": "group.added"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue
            if k == "kwargs":
                method_params.update(kwargs)
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self.get_api(**method_params)

    def group_edited(self,
                     name: str,
                     domain: str,
                     fullname: Optional[str] = None,
                     description: Optional[str] = None,
                     subgroup: Optional[str] = None,
                     members: Optional[str] = None,
                     sendmailright: Optional[int] = 0,
                     sendmailmembers: Optional[str] = None,
                     managers: Optional[str] = None,
                     visibleright: Optional[int] = 0,
                     sendervisible: Optional[bool] = True,
                     **kwargs: Optional[Dict]
                     ) -> Dict[str, Any]:
        """新增邮件组

        :param name: 组名
        :param domain: 域名
        :param fullname: 组名称
        :param description: 描述
        :param subgroup: 子分组，各子分组名以分号(;)分
        :param members: 组成员  各成员名以分号(;)分隔
        :param sendmailright: 发信权限
            0 - 任何人都可以给组员发
            信；
            1 - 只有组员可以发信；
            2 - 仅指定成员可以发信；
            3 - 本域下用户可以发信
        :param sendmailmembers: 发信成员  各发信成员名以分号(;)分隔
        :param managers: 组管理员  各组管理员名以分号(;)分隔
        :param visibleright: 可见权限
            0 - 任何人可以看到此通讯组及其成员；
            1 - 任何人可以看到此通讯组；
            2 - 本域用户可以看到此通讯组及其成员；
            3 - 域用户可以看到此通讯组；
            4 - 组成员可以看到此通讯组及其成员；
            5 - 组成员可以看到此通讯组；
            6 - 只有管理员可以看到此通讯组及成员
        :param sendervisible: 发信成员可见
            0 - 没有特别可见权限；
            1 - 发信成员有相同的可见度。
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  组修改失败
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self.sessid, "method": "group.edited"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue
            if k == "kwargs":
                method_params.update(kwargs)
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self.get_api(**method_params)

    def group_addmember(self,
                        name: str,
                        domain: str,
                        groups: str) -> Dict[str, Any]:
        """增加组成员

        :param name: 组成员名
        :param domain: 组成员域名
        :param groups: 组名列表， 多个组以;分隔
        :return:  返回值
            成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  组成员增加失败
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self.sessid, "method": "group.addmember"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self.get_api(**method_params)

    def group_modifymember(self,
                           name: str,
                           domain: str,
                           groups: str) -> Dict[str, Any]:
        """修改组成员

        修改组成员，从系统里的其他组中删除此成员，仅是组名列表中的组成员。

        :param name: 组成员名
        :param domain: 组成员域名
        :param groups: 组名列表， 多个组以;分隔
        :return:  返回值
            成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  组成员增加失败
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self.sessid, "method": "group.modifymember"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self.get_api(**method_params)

    def group_delmember(self,
                        name: str,
                        domain: str,
                        groups: str) -> Dict[str, Any]:
        """删除组成员

        删除组成员，从指的组中删除此成员。

        :param name: 组成员名
        :param domain: 组成员域名
        :param groups: 组名列表， 多个组以;分隔
        :return:  返回值
            成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  组成员增加失败
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self.sessid, "method": "group.delmember"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self.get_api(**method_params)

    def group_delete(self, domain: str, pageno: Optional[int] = 0) -> Dict[str, Any]:
        """
        删除邮件组

        :param domain: 域名
        :param pageno: 页数
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  组删除失败
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self.sessid, "method": "group.delete"}
        method_params.update({"pageno": str(pageno), "domain": domain})

        return self.get_api(**method_params)

    def adminuser(self, pageno: Optional[int] = 0) -> Dict[str, Any]:
        """管理员列表

        获取管理员列表
        :param pageno:  页码  分页序号，以 0 开始
        :return: 成功返回值
            {
                "result": "ok",
                "info":
                {
                    “ users ”: 用户列表 ,
                    “ totalcount ”: 用户总数
                    “ pagecount ”:  分页总数
                }
            }
        """
        method_params = {"sessid": self.sessid, "method": "adminuser", "pageno": str(pageno)}

        return self.get_api(**method_params)

    def adminuser_added(self,
                        username: str,
                        password: str,
                        description: Optional[str],
                        adminrange: Optional[str],
                        usertype: Optional[int] = 0
                        ) -> Dict[str, Any]:

        """新增 管理员

        :param username: 管理员用户名
        :param password: 管理员密码
        :param description: 描述
        :param adminrange: 允许管理的域 多个域名之间用分号(;)分隔；域管理员需设置
        :param usertype: 管理员类型 0 - 超级管理员；1 - 域管理员
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  管理新增失败
            2  用户名格式不正确
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self.sessid, "method": "adminuser.added"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self.get_api(**method_params)

    def adminuser_edited(self,
                         username: str,
                         password: str,
                         description: Optional[str],
                         adminrange: Optional[str],
                         usertype: Optional[int] = 0
                         ) -> Dict[str, Any]:

        """修改管理员

        :param username: 管理员用户名
        :param password: 管理员密码
        :param description: 描述
        :param adminrange: 允许管理的域 多个域名之间用分号(;)分隔；域管理员需设置
        :param usertype: 管理员类型 0 - 超级管理员；1 - 域管理员
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  管理修改失败
            2  用户名格式不正确
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self.sessid, "method": "adminuser.edited"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self.get_api(**method_params)

    def adminuser_delete(self,
                         username: str
                         ) -> Dict[str, Any]:
        """删除管理员

        :param username: 管理员用户名
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  管理删除失败
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self.sessid, "method": "adminuser.delete", "username": username}

        return self.get_api(**method_params)

    # ######用户端接口开始
    def folders(self):
        """列邮件夹

        列邮件夹
        :return: 返回值
            {
            "result": "ok",
            "info":
                {
                “private”:  个人邮件夹,
                “public”:  公共邮件夹
                “archive”:  归档邮件夹
                “label”:  标签
                }
            }
        """

        method_params = {"sessid": self.sessid, "method": "folders"}

        return self.get_api(**method_params)

    def folders_newfolder(self, newfolder: str) -> Dict[str, Any]:
        """ 新建邮件夹

        新建邮件夹
        :param newfolder: 邮件夹名
        :return: 返回值
            { "result": "ok"}
        """
        method_params = {"sessid": self.sessid, "method": "folders.newfolder", "newfolder": newfolder}

        return self.get_api(**method_params)

    def folders_renamefolder(self, optfolder: str, newfolder: str) -> Dict[str, Any]:
        """ 重命名 邮件夹

         重命名 邮件夹
        :param optfolder:
        :param newfolder:
        :return: 返回值
            { "result": "ok"}
        """
        method_params = {"sessid": self.sessid, "method": "folders.renamefolder",
                         "newfolder": newfolder, "optfolder": optfolder}

        return self.get_api(**method_params)

    def folders_delfolder(self, optfolder: str) -> Dict[str, Any]:
        """ 删除邮件夹

        删除邮件夹
        :param optfolder: 要操作的邮件夹名
        :return: 返回值
            { "result": "ok"}
        """
        method_params = {"sessid": self.sessid, "method": "folders.delfolder", "optfolder": optfolder}

        return self.get_api(**method_params)

    def folders_emptyfolder(self, optfolder: str) -> Dict[str, Any]:
        """ 清空邮件夹

        清空邮件夹
        :param optfolder: 要操作的邮件夹名
        :return: 返回值
            { "result": "ok"}
        """
        method_params = {"sessid": self.sessid, "method": "folders.emptyfolder", "optfolder": optfolder}

        return self.get_api(**method_params)

    def msglist(self, folder: str, pag: Optional[int] = 1, **kwargs) -> Dict[str, Any]:
        """列邮件夹的邮件

        列邮件夹的邮件，此接口还有listtype/label参数，以便列出已读未读之类特定邮件。
        | listtype值 |                                       |
        | ---------- | ------------------------------------- |
        | flagged    | 星标邮件                              |
        | read       | 已读                                  |
        | unread     | 未读                                  |
        | answered   | 已回复                                |
        | forwarded  | 已转发                                |
        | label      | 有标签（需要和另一个参数label同时用） |

        :param folder: 文件夹
        :param pag: 页码 分页序号，以 1 开始
        :return: 返回值
        {
        "result": "ok",
        "info":
            {
            “messagelist”:  邮件列表信息,
            “totalpage”:  总分页数
            “newmsg”:  新邮件数
            “msgtotal”:  邮件总数
            }
        }
        """
        method_params = {"sessid": self.sessid, "method": "msglist"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue
            if k == "kwargs":
                method_params.update(kwargs)
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self.get_api(**method_params)

    def msglist_delete(self, folder: str, msgid: int) -> Dict[str, Any]:
        """删除邮件

        :param folder: 文件夹
        :param msgid: 邮件标识
        :return: 返回值{ "result": "ok"}
        """
        method_params = {"sessid": self.sessid, "method": "msglist.delete", "folder": folder, "msgid": str(msgid)}

        return self.get_api(**method_params)

    def msglist_move(self, folder: str, msgid: int, tofolder: str) -> Dict[str, Any]:
        """删除邮件

        :param folder: 文件夹
        :param msgid: 邮件标识
        :param tofolder:  目标邮件夹
        :return: 返回值{ "result": "ok"}
        """
        method_params = {"sessid": self.sessid, "method": "msglist.move",
                         "folder": folder, "msgid": str(msgid), "tofolder": tofolder}

        return self.get_api(**method_params)

    def msglist_top(self, folder: str, msgid: int) -> Dict[str, Any]:
        """置顶邮件

        :param folder: 文件夹
        :param msgid: 邮件标识
        :return: 返回值{ "result": "ok"}
        """
        method_params = {"sessid": self.sessid, "method": "msglist.top", "folder": folder, "msgid": str(msgid)}

        return self.get_api(**method_params)

    def msglist_untop(self, folder: str, msgid: int) -> Dict[str, Any]:
        """取消置顶邮件

        :param folder: 文件夹
        :param msgid: 邮件标识
        :return: 返回值{ "result": "ok"}
        """
        method_params = {"sessid": self.sessid, "method": "msglist.untop", "folder": folder, "msgid": str(msgid)}

        return self.get_api(**method_params)

    def msglist_read(self, folder: str, msgid: int) -> Dict[str, Any]:
        """邮件标记已读

        :param folder: 文件夹
        :param msgid: 邮件标识
        :return: 返回值{ "result": "ok"}
        """
        method_params = {"sessid": self.sessid, "method": "msglist.read", "folder": folder, "msgid": str(msgid)}

        return self.get_api(**method_params)

    def msglist_unread(self, folder: str, msgid: int) -> Dict[str, Any]:
        """邮件标记未读

        :param folder: 文件夹
        :param msgid: 邮件标识
        :return: 返回值{ "result": "ok"}
        """
        method_params = {"sessid": self.sessid, "method": "msglist.unread", "folder": folder, "msgid": str(msgid)}

        return self.get_api(**method_params)

    def msglist_flag(self, folder: str, msgid: int) -> Dict[str, Any]:
        """设置星标邮件

        :param folder: 文件夹
        :param msgid: 邮件标识
        :return: 返回值{ "result": "ok"}
        """
        method_params = {"sessid": self.sessid, "method": "msglist.flag", "folder": folder, "msgid": str(msgid)}

        return self.get_api(**method_params)

    def msglist_unflag(self, folder: str, msgid: int) -> Dict[str, Any]:
        """取消星标邮件

        :param folder: 文件夹
        :param msgid: 邮件标识
        :return: 返回值{ "result": "ok"}
        """
        method_params = {"sessid": self.sessid, "method": "msglist.unflag", "folder": folder, "msgid": str(msgid)}

        return self.get_api(**method_params)

    def msgnum(self) -> Dict[str, Any]:
        """各邮件夹未读邮件数

        :return: 返回值
            {
            "result": "ok",
            "info": 各文件夹的未读邮件数
            }
        """
        method_params = {"sessid": self.sessid, "method": "msgnum"}

        return self.get_api(**method_params)

    def readmsg(self, folder: str, msgid: int) -> Dict[str, Any]:
        """ 阅读邮件

        :param folder: 文件夹
        :param msgid: 邮件标识
        :return: 返回值
            {
            "result": "ok",
            "info":
                {
                “from”:  发件人信息,
                “reply-to”: 回复信息
                “to”:  收件人信息
                “cc”:  抄送信息
                “subject”: 主题
                “date”:  发件日期
                “body”:  信体内容
                “attachment”:  邮件附件
                “memo”:  邮件备注信息
                }
            }
        """
        method_params = {"sessid": self.sessid, "method": "readmsg", "folder": folder, "msgid": str(msgid)}

        return self.get_api(**method_params)

    def newmsg_send(self, to: str,
                    cc: Optional[str],
                    subject: str,
                    msgbody: str,
                    ishtml: Optional[bool],
                    priority: Optional[bool],
                    requestnotify: Optional[bool],
                    **kwargs
                    ) -> Dict[str, Any]:
        """ 发送邮件

        如果要发送带附件的邮件，要先重置写邮件缓存，然后上传附件，最后再发送邮件。重置写邮件缓存，如要发送含附件邮件建议先进行重置操作。
        :param to: 收件人 多个地址用分号(;)分隔
        :param cc: 抄送 多个地址用分号(;)分隔
        :param subject: 邮件主题
        :param msgbody: 邮件信体
        :param ishtml: Html 邮件  0 - 文本邮件；1 – HTML 邮件
        :param priority: 优先级  0 - 正常；1 - 优先
        :param requestnotify: 请求阅读回条 0 - 不需要；1 - 需要
        :return: 返回值 { "result": "ok"}
        """
        method_params = {"sessid": self.sessid, "method": "newmsg.send"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue
            if k == "kwargs":
                method_params.update(kwargs)
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self.get_api(**method_params)

    def newmsg_reset(self) -> Dict[str, Any]:
        """ 重置写邮件缓存

        :return: 返回值 { "result": "ok"}
        """
        method_params = {"sessid": self.sessid, "method": "newmsg.reset"}

        return self.get_api(**method_params)

    def upload_upload(self, attachfile: Union[str, list]) -> Dict[str, Any]:
        """上传附件

        可以一次上传多个文件，也可以分多次上传, 附件文件绝对路径。
        :param attachfile: 附件文件绝对路径或者多附件List。
        :return: 返回值
            {
            "result": "ok",
            “list”:[
                    {
                    "name":"readme.txt",
                    "dispname":"readme.txt",
                    "localname":"C:\\Winmail\\server\\webmail\\temp\\_attachments\\test_baa065a52e385
                    9e4e1a0ee2ca9188713_3a077176425dd745941ee40cd3dc5914",
                    "type":"text/plain",
                    "size":156894
                    },
                    {
                    "name":" 20180705141449.jpg",
                    "dispname":" 20180705141449.jpg",
                    "localname":"C:\\Winmail\\server\\webmail\\temp\\_attachments\\test_baa065a52e385
                    9e4e1a0ee2ca9188713_ 052c4b360ca824741aaa873077e8570d",
                    "type":"image/jpg",
                    "size": 54954
                    }
            ]
            }
        """

        method_params = {"sessid": self.sessid, "method": "upload.upload", "attachfile": attachfile}

        return self.get_api(**method_params)

    def upload_delete(self, attachid: int) -> Dict[str, Any]:
        """删除某个附件

        :param attachid: 附件 ID。上传后返回的附件数组， 所删除附件在数组中序号，序号以 0 开始
        :return: 返回值{ "result": "ok"}
        """

        method_params = {"sessid": self.sessid, "method": "upload.delete", "attachid": attachid}

        return self.get_api(**method_params)

    def addressbook(self, pag: Optional[int] = 1) -> Dict[str, Any]:
        """ 列个人地址簿

        :param pag: 页码分页序号，以 1 开始
        :return: 返回值
                {
                "result": "ok",
                "info":
                    {
                    “group”:  地址组列表 ,
                    “address”:  联系人列表
                    “totalpage”:  总页数
                    “addresscount”:  邮件总数
                    }
                }
        """

        method_params = {"sessid": self.sessid, "method": "addressbook", "pag": str(pag)}

        return self.get_api(**method_params)

    def addressbook_addcontact(self, name: str, email: str,
                               mobile: Optional[str],
                               phone: Optional[str],
                               fax: Optional[str],
                               address: Optional[str],
                               zipcode: Optional[str],
                               company: Optional[str],
                               depart: Optional[str],
                               jobtitle: Optional[str],
                               homephone: Optional[str],
                               homeaddress: Optional[str],
                               homezipcode: Optional[str],
                               im: Optional[str],
                               url: Optional[str],
                               email1: Optional[str],
                               birthday: Optional[str],
                               memo: Optional[str]) -> Dict[str, Any]:
        """ 增加联系人

         增加个人地址簿联系人
        :param name: 姓名
        :param email: 邮件地址
        :param mobile: 手机
        :param phone: 电话
        :param fax: 传真
        :param address: 联系地址
        :param zipcode: 区号
        :param company: 工作单位
        :param depart: 部门
        :param jobtitle: 职位
        :param homephone: 家庭电话
        :param homeaddress: 家庭地址
        :param homezipcode: 家庭区号
        :param im: 即时通信
        :param url: 个人网址
        :param email1: 备份邮箱地址
        :param birthday: 生日
        :param memo: 备注
        :return: 返回值{ "result": "ok"}
        """

        method_params = {"sessid": self.sessid, "method": "addressbook.addcontact"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self.get_api(**method_params)

    def addressbook_savecontact(self, id: int, name: str, email: str,
                                mobile: Optional[str],
                                phone: Optional[str],
                                fax: Optional[str],
                                address: Optional[str],
                                zipcode: Optional[str],
                                company: Optional[str],
                                depart: Optional[str],
                                jobtitle: Optional[str],
                                homephone: Optional[str],
                                homeaddress: Optional[str],
                                homezipcode: Optional[str],
                                im: Optional[str],
                                url: Optional[str],
                                email1: Optional[str],
                                birthday: Optional[str],
                                memo: Optional[str]) -> Dict[str, Any]:
        """ 修改 联系人

        :param id: 联系人标识
        :param name: 姓名
        :param email: 邮件地址
        :param mobile: 手机
        :param phone: 电话
        :param fax: 传真
        :param address: 联系地址
        :param zipcode: 区号
        :param company: 工作单位
        :param depart: 部门
        :param jobtitle: 职位
        :param homephone: 家庭电话
        :param homeaddress: 家庭地址
        :param homezipcode: 家庭区号
        :param im: 即时通信
        :param url: 个人网址
        :param email1: 备份邮箱地址
        :param birthday: 生日
        :param memo: 备注
        :return: 返回值{ "result": "ok"}
        """

        method_params = {"sessid": self.sessid, "method": "addressbook.savecontact"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self.get_api(**method_params)

    def addressbook_delecontact(self, id: int) -> Dict[str, Any]:
        """ 删除 联系人

        :param id: 联系人标识
        :return: { "result": "ok"}
        """
        method_params = {"sessid": self.sessid, "method": "addressbook.delecontact", "id": str(id)}

        return self.get_api(**method_params)

    def addressbook_addgroup(self, name: str, member: str) -> Dict[str, Any]:
        """增加地址组

        :param name: 分组名称
        :param member: 组成员多个联系人地址用分号(;)分隔
        :return: { "result": "ok"}
        """

        method_params = {"sessid": self.sessid, "method": "addressbook.addgroup",
                         "name": name, "member": member}

        return self.get_api(**method_params)

    def addressbook_savegroup(self, id: int, name: str, member: str) -> Dict[str, Any]:
        """修改地址组

        :param id: 组标识
        :param name: 分组名称
        :param member: 组成员多个联系人地址用分号(;)分隔
        :return: { "result": "ok"}
        """

        method_params = {"sessid": self.sessid, "method": "addressbook.savegroup", "id": str(id),
                         "name": name, "member": member}

        return self.get_api(**method_params)

    def addressbook_delegroup(self, id: int) -> Dict[str, Any]:
        """ 删除地址组

        :param id: 组标识
        :return: { "result": "ok"}
        """
        method_params = {"sessid": self.sessid, "method": "addressbook.delegroup", "id": str(id)}

        return self.get_api(**method_params)

    def netaddressbook(self, pag: Optional[int] = 1) -> Dict[str, Any]:
        """ 列公共地址簿

        :param pag: 页码分页序号，以 1 开始
        :return: 返回值
                {
                "result": "ok",
                "info": {
                    "address": [
                        {
                            "uid": "b",
                            "name": "\u59d3\u540d\u4e59",
                            "email": "b@test.com",
                            "mobile": "13700001111",
                            "company": "\u4e59\u7684\u516c\u53f8\u540d",
                            "department": "\u4e59\u7684\u90e8\u95e8",
                            "jobtitle": " ",
                            "office": " ",
                            "officephone": " ",
                            "homeaddress": " ",
                            "homephone": " ",
                            "chksum": "4c9617b6ca8715663bbed4923c644df0",
                            "usertype": "sys"
                        }
                    ],
                    "totalpage": 2,
                    "addresscount": 31
                }
            }
        """

        method_params = {"sessid": self.sessid, "method": "netaddressbook", "pag": str(pag)}

        return self.get_api(**method_params)

    def systemgroup(self, pag: Optional[int] = 1) -> Dict[str, Any]:
        """ 列系统通信组

        :param pag: 页码分页序号，以 1 开始
        :return: 返回值
        {
            "result": "ok",
            "info": {
                "group": [
                    {
                        "groupid": "everyone",
                        "name": "everyone",
                        "domain": "",
                        "fullname": "everyone@test.com",
                        "description": "",
                        "sendmailright": 3,
                        "visibleright": 0,
                        "sendervisible": 0,
                        "memberlist": "a;a-a;c112;api;1000",
                        "sendmailmember": "",
                        "managerlist": "",
                        "subgroup": [
                            "salse1"
                        ],
                        "extmembername": "",
                        "sortby": 0,
                        "orderno": 9999,
                        "localsend": 0,
                        "fromgroup": 0,
                        "rcptmember": 0,
                        "mailhost": "",
                        "syncaction": "",
                        "synctime": 1694592460,
                        "openid": "",
                        "id": 2982,
                        "groupmail": "everyone@test.com",
                        "manager": 0,
                        "sendmail": 1,
                        "listmember": true,
                        "arraymemberlist": null,
                        "subgrouplevel": 0,
                        "chksum": "0952e1dd7af352500f67524911b21a0c"
                    }
                ],
                "totalpage": 1,
                "groupcount": 7
            }
        }
        """

        method_params = {"sessid": self.sessid, "method": "systemgroup", "pag": str(pag)}

        return self.get_api(**method_params)
