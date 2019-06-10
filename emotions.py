# -*- coding: utf-8 -*-
# @Author  : diaoxinqiang
# @File    : emotions.py
# @Time    : 2019/6/6 下午8:00
# @Software: PyCharm
import csv
import json
import urllib.request

import os

import re
import requests


def get_emotions(text, access_token):
    try:
        values = {
            'text': text,
        }

        host = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?' + \
               'access_token=' + access_token \
               + '&charset=UTF-8' \
               + '&text=' + text

        response = requests.post(host, json=values).json()
        print(response)
        item_values = []
        items = response['items'][0]
        item_values.append(str(items['sentiment']))
        item_values.append(str(items['confidence']))
        item_values.append(str(items['positive_prob']))
        item_values.append(str(items['negative_prob']))

        return item_values
    except Exception as e:
        print(e)
        return []


def get_access_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    client_id = 'xxxx'
    client_secret = '00000'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id \
           + '&client_secret=' + client_secret
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = json.loads(response.read())
    if (content):
        print(content)
    access_token = content['access_token']
    return access_token


emoji_pattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE)


def remove_emoji(text):
    return emoji_pattern.sub(r'', text)


def read_csv():
    access_token = get_access_token()
    path = './CSV'
    files = os.listdir(path)
    for file in files:
        csv_path = os.path.join(path, file)
        count = 0
        lines = []
        rows = []
        with open(csv_path, encoding='utf-8') as f:

            for line in f:
                count += 1
                row = line.split(',')
                if count > 2:
                    print(row)
                    comment = row[1]
                    comment = remove_emoji(comment)
                    if comment is not None and '' != comment:
                        item_values = get_emotions(comment, access_token)
                        row.extend(item_values)
                        new_line = ','.join(row)

                        lines.append(new_line)
                        rows.append(row)
                    else:
                        lines.append(line)
                        rows.append(row)
                elif count == 2:
                    row.extend(['sentiment', 'confidence', 'positive_prob', 'negative_prob'])
                    rows.append(row)

                    new_line = ','.join(row)
                    lines.append(new_line)
                # elif count >= 10:
                #     break
                else:
                    rows.append(row)
                    lines.append(line)

        with open(os.path.join('./emotions_csv', 'emotions' + file), "w",
                  encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # 写入多行用writerows
            writer.writerows(rows)


if __name__ == '__main__':
    read_csv()
