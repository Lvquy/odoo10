# -*- coding: utf-8 -*-

import json

with open("test.json") as b:
    data = json.load(b)

    for i in data:
        print int(data[i]['_id'])
#
# with open("huyen.json") as b:
#     data = json.load(b)

# for i in data:
#     print '<record id="%s" model="huyen">' %data[i]['code']
#     print '<field name="name">%s</field>' %data[i]['name_with_type']
#     print '<field name="code_huyen">%s</field>' % data[i]['code']
#     print '<field name="parent_code">%s</field>' %data[i]['parent_code']
#     print '<field name="thuoc_tinh" ref="%s"/>' %data[i]['parent_code']
#     print '</record>'


#
# with open("tinh.json") as b:
#     data = json.load(b)
#
# for i in data:
#     print '<record id="%s" model="tinh">' %data[i]['code']
#     print '<field name="name">%s</field>' %data[i]['name_with_type']
#     print '<field name="code_tinh">%s</field>' % data[i]['code']
#     print '</record>'
#
# with open("xa3.json") as b:
#     data = json.load(b)
#
# for i in data:
#     print '<record id="%s" model="xa">' %data[i]['code']
#     print '<field name="name">%s</field>' %data[i]['name_with_type']
#     print '<field name="code_xa">%s</field>' % data[i]['code']
#     print '<field name="parent_code">%s</field>' %data[i]['parent_code']
#     print '<field name="thuoc_huyen" ref="%s"/>' %data[i]['parent_code']
#     print '</record>'


# import requests
# import json
#
# ACCESS_TOKEN = 'o.Et4pxH6uDRH0s0RHaUp9mpazs0vHX7rZ'
# resp = requests.post('https://api.pushbullet.com/v2/upload-request', data=json.dumps({'file_name': 'image.jpg'}), headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})
# if resp.status_code != 200:
#     raise Exception('failed to request upload')
# r = resp.json()
# resp = requests.post(r['upload_url'], data=r['data'], files={'file': open('image.jpg', 'rb')})
# if resp.status_code != 204:
#     raise Exception('failed to upload file')
# print r['file_name'], r['file_type'], r['file_url']

# import requests
# import json
#
#
# def send_notification_via_pushbullet(title, body):
#     """ Sending notification via pushbullet.
#         Args:
#             title (str) : title of text.
#             body (str) : Body of text.
#     """
#     data_send = {"type": "note", "title": title, "body": body}
#
#     ACCESS_TOKEN = 'o.Et4pxH6uDRH0s0RHaUp9mpazs0vHX7rZ'
#     resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
#                          headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})
#     if resp.status_code != 200:
#         raise Exception('Something wrong')
#     else:
#         print 'complete sending'

# for i in 'dkfjdkljljgldkfjgloiudlflkgjdkfg':
#     send_notification_via_pushbullet(title='Canh bao',body=i)
