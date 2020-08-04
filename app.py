
"""
 * Developed by-
 *
 * Name : Rahul Anand
 * Banner ID : B00841310
 * Email ID : rahul.anand@dal.ca
 * 
 """
from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS,cross_origin
import pymongo
from bson.objectid import ObjectId

app=Flask(__name__)
CORS(app) # Allowed cross origin

# Mongo connector
mongo_client = pymongo.MongoClient("mongodb+srv://affordly:affordly123@cluster0.lzi2l.mongodb.net/affordly?retryWrites=true&w=majority")
nosql_db = mongo_client["affordly"]
col = nosql_db["posts"]


@app.route('/clicked', methods=['GET'])
def clicked():
    """
    End point to increase number of clicks per view
    -- Require param: post_id
    -- Returns: Success or Exception
    """
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
            col.update_one({'_id':ObjectId(post_id)}, {'$set': {"clicks": clicks}})
        except Exception as e:
            print (str(e))
            return "Some error occurred"    
    return "Success"


@app.route('/trending', methods=['GET'])
def trending():
    """
    End point to fetch trending items
    -- Require param: None
    -- Returns: List of id and images of trending items
    """
    objects = col.find({"isActive":True}).sort([("clicks",-1)])
    return_dict = []
    for x in objects[:3]:
        idn = x.get('_id')
        image = x.get('img')
        return_dict.append({"id":str(idn), "image":image})
    return jsonify(return_dict)


@app.route('/search', methods=['GET'])
def search():
    keyword=request.args['keyword']
    result_set=[]
    if keyword:
        try:
            objects = col.find({"title": {"$regex": keyword, "$options":'i'}})
            for obj in objects:
                result_set.append({"_id": str(obj.get('_id')), "img":obj.get('img'), "title":obj.get('title'), "description":obj.get('description')})

            objects1 = col.find({"description": {"$regex": keyword, "$options":'i'}})
            for obj in objects1:
                result_set.append({"_0id": str(obj.get('_id')), "img":obj.get('img'), "title":obj.get('title'), "description":obj.get('description')})
        except Exception as e:
            print (str(e))
    if not result_set:
        return jsonify({"message":"No results found"})
    return jsonify(result_set)
