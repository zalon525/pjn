#!/usr/bin/env python3

import json
from urllib.request import urlopen, Request
import time
import sys
import logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


user = 'fgalas525@gmail.com'
task = 'any2txt|wcrft2|liner2({"model":"n82"})'
url = 'http://ws.clarin-pl.eu/nlprest2/base'
in_file = 'data.zip'
out_file = 'out.zip'


def upload(file):
    logging.debug('Uploading file: {}'.format(file))
    resp = urlopen(Request('{}/upload/'.format(url), data=open(file, 'rb'),
                           headers={'Content-Type': 'binary/octet-stream'})).read().decode('ascii')
    logging.debug('Response: {}'.format(resp))
    return resp


def process(data):
    doc = json.dumps(data)
    req = Request('{}/startTask/'.format(url), data=doc.encode('ascii'), headers={'Content-Type': 'application/json'})
    logging.debug('Requesting: url="{}", data="{}"'.format(req.full_url, req.data))
    taskid = urlopen(req).read().decode('ascii')
    logging.debug('Response: {}'.format(taskid))
    time.sleep(0.2)
    req = Request('{}/getStatus/{}'.format(url, taskid))
    logging.debug('Requesting: url="{}", data="{}"'.format(req.full_url, req.data))
    resp = urlopen(req).read().decode('ascii')
    logging.debug('Response: {}'.format(resp))
    data = json.loads(resp)
    while data["status"] == "QUEUE" or data["status"] == "PROCESSING":
        time.sleep(0.5)
        req = Request('{}/getStatus/{}'.format(url, taskid))
        logging.debug('Requesting: url="{}", data="{}"'.format(req.full_url, req.data))
        resp = urlopen(req).read().decode('ascii')
        logging.debug('Response: {}'.format(resp))
        data = json.loads(resp)
    if data["status"] == "ERROR":
        logging.error("Error {}".format(data['value']))
        return None
    return data["value"]


def main():
    fileid = upload(in_file)
    data = process({'lpmn': 'filezip({fileid})|{task}|dir|makezip'.format(fileid=fileid, task=task), 'user': user})
    if data is not None:
        data = data[0]["fileID"]
        req = Request('{}/download{}'.format(url, data))
        logging.debug('Requesting: url="{}", data="{}"'.format(req.full_url, req.data))
        content = urlopen(req).read()
        logging.debug('Response: {}'.format(content))
        with open(out_file, "wb") as outfile:
            outfile.write(content)


if __name__ == '__main__':
    exit(main())
