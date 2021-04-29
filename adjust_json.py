# -*- coding: utf-8 -*-
# @Author: ckxkexing
# @Date:   2021-04-28 14:01:25
# @Last Modified by:   chenkexing
# @Last Modified time: 2021-04-28 17:05:29
import json
def main():
    
    with open('apache_spark_commits.json', 'r') as f:
        d = json.load(f)
    with open('adjusted_apache_spark_commits.json', 'w') as f:
        json.dump(d, f, indent = 2)

if __name__ == '__main__':
    main()