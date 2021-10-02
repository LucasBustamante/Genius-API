from flask_restful import Resource, reqparse
import requests
from dotenv import load_dotenv
from os.path import join, dirname
import uuid
import os
import boto3
from flask import request, jsonify

class GeniusConsume(Resource):

    def search_artist(self, artist):
        base_url = 'http://api.genius.com'
        headers = {'Authorization': 'Bearer {}'.format(os.environ.get('genius_token'))}
        search_url = "{}/search?q={}".format(base_url, artist)
        return requests.get(search_url, headers=headers).json()

    def top_hits(self, info_artist):
        list_songs = []
        for song in info_artist['response']['hits']:
            list_songs.append(song['result']['title'])
        return list_songs

    def get(self, artist):

        res = self.search_artist(artist)

        id_transaction = ''
        if len(res['response']['hits']) != 0:
            id_transaction = str(uuid.uuid4())

        hits = self.top_hits(res)

        about = {
            'id_transaction': id_transaction,
            'artist': artist,
            'songs': hits
        }

        if about['id_transaction'] == '':
            return jsonify(about)

        dynamodb = boto3.resource(
            'dynamodb',
            region_name='us-east-2',
            aws_access_key=os.environ.get('aws_access_key'),
            aws_secret_key=os.environ.get('aws_secret_key')
            )

        table = dynamodb.Table('tb_searches')

        table.put_item(
            Item={
                'id_transaction': id_transaction,
                'artist': artist,
                'songs': hits
            }
        )

        return jsonify(about)