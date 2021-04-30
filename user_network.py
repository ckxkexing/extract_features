# -*- coding: utf-8 -*-
# @Author: ckxkexing
# @Date:   2021-04-30 09:29:43
# @Last Modified by:   ckxkexing
# @Last Modified time: 2021-04-30 10:40:45

import networkx as nx
import json
import time

def main():
    start_time = time.time()
    G = nx.DiGraph()

    # 读入用户基本信息
    user_map = {}
    users = []

    with open('apache_spark/users_features.json', 'r') as f:
        users = json.load(f)
        for i in range(len(users)):
            if users[i]['login'] != None:
                user_map[users[i]['login']] = i
                G.add_node(i)

    # commit中author和committer的关系。
    with open('apache_spark/apache_spark_commits.json', 'r') as f:
        json_data = json.load(f)
        for data in json_data:
            if data['author'] == None or data['author'] == {}:
                continue
            if data['committer'] == None or data['committer'] == {}:
                continue
            
            if data['author']['login'] == data['committer']['login']:
                continue
            G.add_edge(user_map[data['committer']['login']], user_map[data['author']['login']])

    issue_id2user = {}
    with open('apache_spark/apaches_spark_issues.json', 'r') as f:
        json_data = json.load(f)
        for data in json_data:
            issue_id2user[data['number']] = user_map[data['user']['login']]


    # comment中reviewer和 issuer的关系
    with open('apache_spark/apache_spark_issues_comments.json', 'r') as f:
        json_data = json.load(f)
        for data in json_data:
            issue_id = int(data['issue_url'].split('/')[-1])
            if data['user']['login'] in user_map:
                u = user_map[data['user']['login']]
            else :
                continue
            if issue_id in issue_id2user:
                v = issue_id2user[issue_id]
            else :
                continue
            G.add_edge(u, v)
    for i,w in nx.degree(G):
        users[i]['in_degree'] = w

    for k, v in nx.closeness_centrality(G).items():
        users[k]['closeness_centrality'] = v

    for k, v in nx.clustering(G).items():
        users[k]['clustering_centrality'] = v

    for k, v in nx.betweenness_centrality(G).items():
        users[k]['betweenness_centrality'] = v

    for k, v in nx.eigenvector_centrality(G).items():
        users[k]['eigenvector_centrality'] = v

    with open('apache_spark/users_features_with_Graph.json', 'w+') as f:
        json.dump(users, f, indent=2)

    print("用时:", time.time() - start_time, 's')
if __name__ == '__main__':
    main()