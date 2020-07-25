from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS,cross_origin
import pymongo
from bson.objectid import ObjectId


app=Flask(__name__)
mongo_client = pymongo.MongoClient("mongodb+srv://affordly:affordly123@cluster0.lzi2l.mongodb.net/affordly?retryWrites=true&w=majority")

nosql_db = mongo_client["affordly"]
col = nosql_db["posts"]


@app.route('/clicked', methods=['GET'])
def clicked():
    post_id=request.args['post_id']
    if not post_id:
        return "Please speccify a correct ID"
    obj = None
    try:
        obj = list(col.find({'_id':ObjectId(post_id)}))[0]
    except:
        return "Object not found"

    if obj:
        clicks = obj.get('clicks')
        clicks = clicks + 1
        try:
            col.update_one({'_id':ObjectId(post_id)}, {'$set': {"clicks": clicks}}, multi=True)
    # col.update({}, {'$set': {"clicks": 0}}, multi=True)
    
    return "Success"