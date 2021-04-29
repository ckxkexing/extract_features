# -*- coding: utf-8 -*-
# @Author: chenkexing
# @Date:   2021-04-28 16:52:07
# @Last Modified by:   ckxkexing
# @Last Modified time: 2021-04-29 14:26:40


import json
import datetime
import time
class Developer(object):

    def __init__(self, name, login, id):
        # user identity
        self.name = name
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
        self.first_commit = None
        self.last_commit  = None

        # issue
        self.user_issue_count = 0
        self.first_issue = None
        self.last_issue = None

        # pulls
        self.user_pulls_count = 0
        self.first_pull = None
        self.last_pull = None

def time_change(utc):
    # utc = "2017-07-28T08:28:47.776Z"

    UTC_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    utc_time = datetime.datetime.strptime(utc, UTC_FORMAT)
    local_time = utc_time + datetime.timedelta(hours=8)
    # print(local_time)    # 2017-07-28 16:28:47.776000
    return local_time

def main():
    start_time = time.time()
    # 从commit中提取出所有用户，并对其进行id编号

    # 之前pick过一遍,先只获取author
    users = []  # {email, users}
    commit_count = {}
    user_map = {}
# 处理出所有author信息
    with open("apache_spark/apache_spark_commits.json", 'r') as f:
        json_data = json.load(f)
        for data in json_data:
            if data["author"] == None or data["author"] == {}:
                continue
            cur_user = data["author"]
            if cur_user["login"] in user_map:
                exist_user = users[user_map[cur_user["login"]]]
                if time_change(exist_user.first_commit) > time_change(data["commit"]["author"]["date"]):
                    exist_user.first_commit = data["commit"]["author"]["date"]
                if time_change(exist_user.last_commit) < time_change(data["commit"]["author"]["date"]):
                    exist_user.first_commit = data["commit"]["author"]["date"]
                exist_user.user_commits_count += 1
            else:
                tmp = Developer( data["commit"]["author"]["name"],data["author"]["login"], data["author"]["id"])
                tmp.first_commit = data["commit"]["author"]["date"]
                tmp.last_commit  = data["commit"]["author"]["date"]
                tmp.email = data["commit"]["author"]["email"]
                tmp.is_author = 1
                tmp.user_commits_count = 1
                users.append(tmp)
                user_map[tmp.login] = len(users) - 1
# author end

# 处理所有committer信息
    with open("apache_spark/apache_spark_commits.json", 'r') as f:
        json_data = json.load(f)
        for data in json_data:
            if data["committer"] == None or data["committer"] == {}:
                continue
            cur_user = data["committer"]
            if cur_user["login"] in user_map:
                exist_user = users[user_map[cur_user["login"]]]
                if time_change(exist_user.first_commit) > time_change(data["commit"]["committer"]["date"]):
                    exist_user.first_commit = data["commit"]["committer"]["date"]
                if time_change(exist_user.last_commit) < time_change(data["commit"]["committer"]["date"]):
                    exist_user.first_commit = data["commit"]["committer"]["date"]
                exist_user.is_committer = 1
            else:
                tmp = Developer(data["commit"]["committer"]["name"],data["committer"]["login"], data["committer"]["id"])
                tmp.first_commit = data["commit"]["committer"]["date"]
                tmp.last_commit  = data["commit"]["committer"]["date"]
                tmp.email = data["commit"]["committer"]["email"]
                tmp.is_committer = 1
                users.append(tmp)
# committer end

# 将commit中的co_patner 也添加到users中
    with open("apache_spark/pick_prople_from_apache_spark_commits.json", 'r') as f:
        json_data = json.load(f)
        for data in json_data:
            for cp in data["co_patner"]:
                flag = 1
                for exist_user in users:
                    if cp['email'] == exist_user.email:
                        flag = 0
                        break
                if flag == 1:
                    tmp = Developer(cp["name"], None, None)
                    tmp.email = cp['email']
                    users.append(tmp)
# co_patner 处理结束

# issue start
    with open("apache_spark/apaches_spark_issues.json", 'r') as f:
        json_data = json.load(f)
        for data in json_data:
            cur_user = data['user']
            if cur_user['login'] in user_map:
                exist_user = users[user_map[cur_user['login']]]
                exist_user.user_issue_count += 1
                if exist_user.first_issue==None or time_change(exist_user.first_issue) > time_change(data['created_at']):
                    exist_user.first_issue = data['created_at']
                if exist_user.last_issue==None or time_change(exist_user.last_issue) < time_change(data['updated_at']):
                    exist_user.last_issue = data['updated_at']
            else :
                tmp = Developer(None, cur_user["login"], cur_user["id"])
                tmp.first_issue = data['created_at']
                tmp.last_issue  = data['updated_at']
                tmp.user_issue_count = 1
                users.append(tmp)
                user_map[tmp.login] = len(users) - 1
# issue end
  

# pull start
# reviewer 需要['review_comments']的获取

    with open("apache_spark/apache_spark_pulls.json", 'r') as f:
        json_data = json.load(f)
        for data in json_data:
            cur_user = data['user']
            if cur_user['login'] in user_map:
                exist_user = users[user_map[cur_user['login']]]
                exist_user.user_pulls_count += 1
                if exist_user.first_pull==None or time_change(exist_user.first_pull) > time_change(data['created_at']):
                    exist_user.first_pull = data['created_at']
                if exist_user.last_pull==None or time_change(exist_user.last_pull) < time_change(data['updated_at']):
                    exist_user.last_pull = data['updated_at']
            else :
                tmp = Developer(None, cur_user["login"], cur_user["id"])
                tmp.first_pull = data['created_at']
                tmp.last_pull  = data['updated_at']
                tmp.user_pulls_count = 1
                users.append(tmp)
                user_map[tmp.login] = len(users) - 1
# pull end

    for i in range(0,2):
        print(json.dumps(users[i].__dict__ ,indent=2))

    print("用时:", time.time() - start_time, 's')
if __name__ == '__main__':
    main()