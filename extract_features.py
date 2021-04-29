# -*- coding: utf-8 -*-
# @Author: chenkexing
# @Date:   2021-04-28 16:52:07
# @Last Modified by:   chenkexing
# @Last Modified time: 2021-04-29 10:08:26


import json

def main():
    # 从commit中提取出所有用户，并对其进行id编号

    # 之前pick过一遍,先只获取author
    users = []  # {email, users}
    commit_count = {}
    with open("apache_spark_commits.json", 'r') as f:
        json_data = json.load(f)
        cnt = 0
        for data in json_data:
            flag = 1
            cnt += 1

            if data["author"] == None or data["author"] == {}:
                continue
            cur_login = data["author"]["login"]
            if cur_login not in commit_count:
                commit_count[cur_login] = 0
            commit_count[cur_login] += 1
            for exist_user in users:
                if data["author"]["login"] == exist_user["login"]:
                    flag = 0
                    break
            data["author"]["email"] = data["commit"]["author"]["email"]
            if flag == 1:
                users.append(data["author"])
    for user in users:
        user['user_commits_count'] = commit_count[user['login']]
        user['is_author'] = 1
        del user['node_id']
        del user['avatar_url']
        del user['gravatar_id']
        del user['followers_url']
        del user['following_url']
        del user['gists_url']
        del user['starred_url']
        del user['subscriptions_url']
        del user['organizations_url']
        del user['html_url']
        del user['repos_url']
        del user['events_url']
        del user['received_events_url']
        del user['type']
        del user['site_admin']

    print(json.dumps(users[:3], indent=2))


if __name__ == '__main__':
    main()