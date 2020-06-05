import config

from flask import Blueprint, jsonify, request
import requests
import pandas as pd
import json

api = Blueprint('api', __name__)

@api.route('/posts', methods=['GET'])
def getPosts():
    comments = requests.get(config.COMMENTS_API).content
    posts = json.loads(requests.get(config.POSTS_API).content)

    df = pd.DataFrame(pd.read_json(comments,orient='columns'))
    grouped = df.groupby('postId')['postId'].count().reset_index(name="count")
    sorted = grouped.sort_values('count')
    comments_count = sorted.to_dict('records')
    
    result = []
    for cc in comments_count:
        post = next((x for x in posts if x['id'] == cc['postId']), None)
        if post != None:
            post['total_number_of_comments'] = cc['count']
            del post['userId']
            result.append(post);
            
    return jsonify(result)

@api.route('/search', methods=['POST'])
def search():
    comments = json.loads(requests.get(config.COMMENTS_API).content)
    data = json.loads(request.data)
    
    value = data['value']
    field = data['field']
    print(value, field)
    result = []

    for comment in comments:
        if value in comment[field]:
            result.append(comment)

    return jsonify(result)
