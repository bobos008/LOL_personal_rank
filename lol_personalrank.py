# coding=utf-8


import requests
import time
import random
import json


class PersonalRank(object):

    def __init__(self):
        self.ss = requests.session()
        self.man_url = 'https://apps.game.qq.com/lol/act/a20160519Match/Match.php'
        self.init_url = 'https://lpl.qq.com/es/data/rank.shtml?iGameId=115&sGameType=7'

    def load_rank_page(self):
        """加载初始页面"""
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,\
                application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu \
                Chromium/75.0.3770.90 Chrome/75.0.3770.90 Safari/537.36'
        }
        response = self.ss.get(self.init_url, headers=headers)
        if response.status_code == 200:
            return True
        return False

    def get_personal_rank(self, ipage='1'):
        """获取选手返回数据(没有清洗)"""
        headers = {
            'Referer': 'https://lpl.qq.com/es/data/rank.shtml?iGameId=115&sGameType=7',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu \
                Chromium/75.0.3770.90 Chrome/75.0.3770.90 Safari/537.36',
        }
        time_tmp = str(int((time.time() * 1000)))
        r_str = str(round(random.random(), 16))
        params = {
            '_a': 'personalrank',
            'iGameId': '115',
            'sGameType': '7',
            'iPage': ipage,
            'sRet': 'PERSONARANKLIST',
            'r': r_str,
            '_': time_tmp
        }
        response = self.ss.get(self.man_url, headers=headers, params=params)
        if response.status_code == 200:
            res_str = response.text
            remove_str = " = "
            if remove_str in res_str:
                remove_str_count = len(remove_str)
                c_index = res_str.index(remove_str)
                result_str = res_str[c_index + remove_str_count:]
                try:
                    res_dict = json.loads(result_str)
                    return res_dict
                except Exception as error:
                    print("get_personal_rank_error:", error)
                    return None
        return None

    def main(self):
        """入口"""
        if not self.load_rank_page():
            print("加载初始页面失败！")
            return None
        time.sleep(1)
        personal_rank = self.get_personal_rank()
        if not personal_rank:
            print("选手数据为空！")
            return None
        msg_data = personal_rank.get("msg", None)
        if not msg_data:
            print("返回数据中没有msg字段!")
            return None
        page_count = msg_data.get("count", None)
        if not page_count:
            print("返回数据中没有count字段!")
            return None
        result_data = msg_data.get("data", list())
        if int(page_count) > 1:
            time.sleep(1)
            for i in range(2, int(page_count) + 1):
                other_personal_rank = self.get_personal_rank(str(i))
                msg_data = other_personal_rank.get("msg", dict())
                cresult_data = msg_data.get("data", list())
                result_data.extend(cresult_data)
        return result_data


if __name__ == '__main__':
    pr = PersonalRank()
    print(json.dumps(pr.main()))
