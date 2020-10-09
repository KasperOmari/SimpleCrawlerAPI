#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from scanner import Crawler

app = Flask(__name__)
api = Api(app)

PORT = 1234
HOST = '0.0.0.0'

sampleData = "{'url': 'http://<host>:<port>/', 'depth': '<depth 0-n>'}"
getMessage = "Send a post request to http://localhost:{port}/ with something like: {data}"

class CrawlerApi(Resource):

    def get(self):
        return {'Name': 'Simple Crawler API',
                'Description': getMessage.format(port=PORT,
                data=sampleData)}

    def post(self):
        json_data = request.get_json(force=True)
        url = json_data['url']
        depth = json_data['depth']
        crawlOutput = Crawler.crawl(Crawler(), url, depth)
        return jsonify(crawlOutput)


api.add_resource(CrawlerApi, '/')

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
