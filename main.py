#! /usr/bin/env python3
# coding=utf-8

import os
import re
import sys
from sklearn import svm
from sklearn import metrics
import joblib #python 3

def get_len(_url):
    '''
        url 长度特征
    '''
    return len(_url)


def get_http_count(_url):
    '''
        这里是存在http头
    '''
    if re.search('(http://)|(https://)', _url, re.IGNORECASE):
        return 1
    else:
        return 0


def get_evil_char(_url):
    '''
        特殊字符: <>,\'\"/
        @reutrn: 个数
    '''
    return len(re.findall("[<>,\'\"/]", _url, re.IGNORECASE))


def get_evil_word(_url):
    '''
       关键字
       @return: 个数
    '''
    return len(re.findall("(alert)|(script)|", _url, re.IGNORECASE))


def etl(file_name, _data, isXSS):
    '''
        get data
        @param file_name: 数据文件
        @param _data: 传入的数组
        @param isXSS: 测试集标注
    '''
    with open(file_name, 'r') as fh:
        # get all the urls as a list
        target_contents = fh.read().split('\n')[:-2]
        for i in target_contents:
            # 提取feature 1: 长度
            feature_1 = get_len(i)

            # 提取feature 2: http数
            feature_2 = get_http_count(i)

            # 提取feature 3: 特殊字符
            feature_3 = get_evil_char(i)

            # 提取敏感关键字
            feature_4 = get_evil_word(i)

            # 训练特征集
            x.append([feature_1, feature_2, feature_3, feature_4])
            if isXSS:
                y.append(1)
            else:
                y.append(0)
        return _data


x = []
y = []
def main(target_file):
    # trainning
    print("[!] traing...")
    etl("xss-10000.txt", x, 1)
    etl("good-xss-10000.txt", x, 0)
    clf = svm.SVC(kernel='linear', C=1).fit(x, y)

    # 模型存储
    joblib.dump(clf, "xss-svm-10000-module.m")

    # predict
    print("[!] predict....")
    with open(target_file, 'r') as fh:
        target_contents = fh.read().split('\n')
        # 特征化
        x_test = []
        for i in target_contents:
            feature_1 = get_len(i) 
            feature_2 = get_http_count(i)
            feature_3 = get_evil_char(i)
            feature_4 = get_evil_word(i)
            x_test.append([feature_1, feature_2, feature_3, feature_4])

    y_test = clf.predict(x_test)
    print(y_test)


if __name__ == '__main__':
    target_file = sys.argv[1]
    if os.path.exists(target_file):
        main(target_file)
