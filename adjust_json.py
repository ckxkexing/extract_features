# -*- coding: utf-8 -*-
# @Author: ckxkexing
# @Date:   2021-04-28 14:01:25
# @Last Modified by:   ckxkexing
# @Last Modified time: 2021-04-29 13:27:30
import json
def main():
    
    with open('apache_spark/apaches_spark_issues.json', 'r') as f:
        d = json.load(f)
    with open('apache_spark/adjusted_apache_spark_issues.json', 'w') as f:
        json.dump(d, f, indent = 2)

if __name__ == '__main__':
    main()