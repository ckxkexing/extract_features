# -*- coding: utf-8 -*-
# @Author: ckxkexing
# @Date:   2021-04-29 17:38:48
# @Last Modified by:   ckxkexing
# @Last Modified time: 2021-04-29 18:17:17


import requests
from fake_useragent import UserAgent
import random
import json


class tool_api(object):
    def __init__(self, org, proj):
        self.org = org
        self.proj = proj
        self.ua = UserAgent()
        self.my_token = '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'


    def get_merge_actor(self, pr_id):
        # https://api.github.com/repos/apache/spark/issues/30327/events
        url = 'https://api.github.com/repos/' + self.org + '/' + self.proj + '/issues/' + str(pr_id) + '/events'

 
        headers = { "User-Agent" :  self.ua.random,
                'Accept': 'application/vnd.github.v3+json',
                'Accept-Language': 'en',
                'Authorization': 'token ' + self.my_token}
        response = requests.get(url, headers = headers)
        json_data = json.loads(response.text)
        # print(json_data)
        for data in json_data:
            if data['event'] == 'merged':
                return data['actor']

    def get_reviewer(self, url):
        # pass
        headers = { "User-Agent" :  self.ua.random,
                'Accept': 'application/vnd.github.v3+json',
                'Accept-Language': 'en',
                'Authorization': 'token ' + self.my_token}
        response = requests.get(url, headers = headers)
        json_data = json.loads(response.text)
        reviewer = []
        for data in json_data:
            reviewer.append(data['user'])
        return reviewer


