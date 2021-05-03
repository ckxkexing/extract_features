# -*- coding: utf-8 -*-
# @Author: ckxkexing
# @Date:   2021-05-03 16:00:22
# @Last Modified by:   ckxkexing
# @Last Modified time: 2021-05-03 18:46:45


'''
这里是Georgios Gousios等人在
An Exploratory Study of the Pull-Based Software Development Mdel
中提到的merge 启发式检索
实现方法。

直接给apache_spark_pulls.json添加
merged_by属性
'''

'''
先没有考虑pr 的commit
先处理pr的comment
'''
import json
import time
def pr_merged_check():
    is_cm = []
    merge_number = {}   
    start_time = time.time()
    with open('apache_spark/apache_spark_issues_comments.json', 'r') as f:
        is_cm = json.load(f)
        for cm in is_cm:
            text = cm['body'].lower()
            if 'merged' in text or 'merging' in text:
                number = int(cm['issue_url'].split('/')[-1])
                merge_number[number] = cm['user']['login']


    merge_count = 0
    with open('apache_spark/apache_spark_pulls.json', 'r') as f:
        pulls = json.load(f)
        for pull in pulls:
            pull['merged_by'] = None
            number = int(pull['number'])
            if number in merge_number:
                merge_count += 1
                pull['merged_by'] = merge_number[number]
    with open('apache_spark/apache_spark_pulls.json', 'w') as f:
        json.dump(pulls, f, indent = 2)
    print("merge_count:", merge_count)
    print("用时:", time.time() - start_time, 's')

# merge_count: 21135
# 用时: 29.969332933425903 s
if __name__ == '__main__':
    pr_merged_check()