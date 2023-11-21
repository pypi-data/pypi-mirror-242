# -*- coding:utf-8 -*-

from winmail.OpenApi import Base, UserStatus, AuthType


class OpenApi12(Base):
    def __init__(self, server: str, port: int, apikey: str, apisecret: str, use_ssl: bool = False) -> None:
        super().__init__(server, port, apikey, apisecret, use_ssl)


if __name__ == "__main__":
    api = OpenApi12('localhost', 80, 'bt66oa8d5b', 'btt87e78f6871aea2016a3916eb65299b7affb18')
    api.login('admin', 'admin', 'admin', 0)
    # print(api.domain())
    print(api.user_edited(name='api', password='test', domain='test.com', authtype=1,
                          status=UserStatus.normal))
    print(api.adminuser())
