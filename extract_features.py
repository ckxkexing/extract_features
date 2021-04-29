# -*- coding: utf-8 -*-
# @Author: chenkexing
# @Date:   2021-04-28 16:52:07
# @Last Modified by:   ckxkexing
# @Last Modified time: 2021-04-29 11:52:35


import json
import datetime

class Developer(object):

    def __init__(self, login, id):
        # user identity
        self.login = login
        self.id    = id

        self.email = 'null'
        self.is_author = 0
        self.is_committer = 0
        self.is_reviewer = 0
        self.is_merger = 0
        self.is_assignee = 0

        # commit
        self.user_commits_count = 0
        self.first_commit = 0
        self.last_commit  = 0


def time_change(utc):
    # utc = "2017-07-28T08:28:47.776Z"
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    utc_time = datetime.datetime.strptime(utc, UTC_FORMAT)
    local_time = utc_time + datetime.timedelta(hours=8)
    # print(local_time)    # 2017-07-28 16:28:47.776000
    return local_time

def main():
    # 从commit中提取出所有用户，并对其进行id编号

    # 之前pick过一遍,先只获取author
    users = []  # {email, users}
    commit_count = {}

# 处理出所有author信息
    with open("apache_spark/apache_spark_commits.json", 'r') as f:
        json_data = json.load(f)
        for data in json_data:
            flag = 1

            if data["author"] == None or data["author"] == {}:
                continue
            cur_login = data["author"]["login"]
            if cur_login not in commit_count:
                commit_count[cur_login] = 0
            commit_count[cur_login] += 1
            for exist_user in users:
                if data["author"]["login"] == exist_user.login:
                    if time_change(exist_user.first_commit) > time_change(data["commit"]["author"]["date"]):
                        exist_user.first_commit = data["commit"]["author"]["date"]
                    if time_change(exist_user.last_commit) < time_change(data["commit"]["author"]["date"]):
                        exist_user.first_commit = data["commit"]["author"]["date"]
                    exist_user.user_commits_count += 1
                    flag = 0
                    break
            if flag == 1:
                tmp = Developer(data["author"]["login"], data["author"]["id"])
                tmp.first_commit = data["commit"]["author"]["date"]
                tmp.last_commit  = data["commit"]["author"]["date"]
                tmp.email = data["commit"]["author"]["email"]
                tmp.is_author = 1
                tmp.user_commits_count = 1
                users.append(tmp)
# author end

# 处理所有committer信息
    with open("apache_spark/apache_spark_commits.json", 'r') as f:
        json_data = json.load(f)
        for data in json_data:
            flag = 1

            if data["committer"] == None or data["committer"] == {}:
                continue
            cur_login = data["committer"]["login"]
            if cur_login not in commit_count:
                commit_count[cur_login] = 0
            commit_count[cur_login] += 1
            for exist_user in users:
                if data["committer"]["login"] == exist_user.login:
                    if time_change(exist_user.first_commit) > time_change(data["commit"]["committer"]["date"]):
                        exist_user.first_commit = data["commit"]["committer"]["date"]
                    if time_change(exist_user.last_commit) < time_change(data["commit"]["committer"]["date"]):
                        exist_user.first_commit = data["commit"]["committer"]["date"]
                    exist_user.is_committer = 1
                    flag = 0
                    break
            if flag == 1:
                tmp = Developer(data["committer"]["login"], data["committer"]["id"])
                tmp.first_commit = data["commit"]["committer"]["date"]
                tmp.last_commit  = data["commit"]["committer"]["date"]
                tmp.email = data["commit"]["committer"]["email"]
                tmp.is_committer = 1
                users.append(tmp)
# committer end



    for i in range(5):
        print(json.dumps(users[i].__dict__ ,indent=2))
if __name__ == '__main__':
    main()