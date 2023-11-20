import pytest
from winmail import OpenApi12, OpenApi
from winmail import ComApi

api = OpenApi12('localhost', 80, 'bt66oa8d5b', 'btt87e78f6871aea2016a3916eb65299b7affb18')


class TestApi12:

    def test_login(self):
        login_result = api.login('admin', 'admin', 'admin', 0)
        print(login_result)

        assert login_result.get('result') and login_result['result'] in ['ok', 'error']
        assert api.sessid

    def test_user_edited(self):
        result = api.user_edited(name='api', password='test', domain='test.com', authtype=1,
                                 status=0)
        assert result['result'] == 'ok'


wc = ComApi()
winmail_db_path = wc.get_db_path()


class TestComApi:

    def test_add_domain(self):
        add_domain = wc.add_domain('testwesdf.com')
        assert add_domain == 0

    def test_del_domain(self):
        del_domain = wc.delete_domain('testwesdf.com')
        assert del_domain == 0
