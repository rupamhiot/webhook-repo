from flask import Blueprint, jsonify,json, render_template, request
from datetime import datetime
from ..extensions import collection
from flask import render_template
import logging
import uuid
logging.basicConfig(level=logging.DEBUG)
from .dates import convert_timestamp

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')
# Receiver end point

@webhook.route('/')
def api_route_main():
    return 'welcome'

@webhook.route('/receiver', methods=["POST"])
def receiver():
    logging.info("Received a webhook request")
    if request.headers['Content-Type'] == 'application/json':
        payload = request.json
        # print(payload)
        action = payload.get('action')
        author = payload.get('pull_request', {}).get('user', {}).get('login')
        if "pusher" in payload:
            ref = payload.get('ref')
            to_branch = ref.split('/')[-1]  # Extracting branch name from ref
            pushed_by = payload.get('pusher', {}).get('name')
            timestamp_str = payload.get('head_commit',{}).get('timestamp')
            timestamp = convert_timestamp(timestamp_str)
            collection.insert_one({
                'id':uuid.uuid4().hex,
                'request_id':None,
                'author':pushed_by,
                'action':'push',
                'from_branch':None,
                'to_branch':to_branch,
                'timestamp':timestamp
            })
            
        elif action == 'opened':
            pull_request_id = payload.get('pull_request', {}).get('id')
            base_branch = payload.get('pull_request', {}).get('base', {}).get('ref')
            head_branch = payload.get('pull_request', {}).get('head', {}).get('ref')
            timestamp_str = payload.get('pull_request', {}).get('created_at')
            timestamp = convert_timestamp(timestamp_str)
            collection.insert_one({
                'id':uuid.uuid4().hex,
                'request_id':pull_request_id,
                'author':author,
                'action':action,
                'from_branch':head_branch,
                'to_branch' : base_branch,
                'timestamp':timestamp
            })
        elif action == 'closed' and payload.get('pull_request', {}).get('merged'):
            merged_pr_id = payload.get('pull_request', {}).get('id')
            base_branch = payload.get('pull_request', {}).get('base', {}).get('ref')
            head_branch = payload.get('pull_request', {}).get('head', {}).get('ref')
            timestamp_str = payload.get('pull_request', {}).get('updated_at')
            timestamp = convert_timestamp(timestamp_str)
            collection.insert_one({
                'id':uuid.uuid4().hex,
                'request_id':merged_pr_id,
                'author':author,
                'action':action,
                'from_branch':head_branch,  
                'to_branch':base_branch,
                'timestamp':timestamp
            })
    return {}, 200

#The UI will keep pulling data from MongoDB every 15 seconds and display the latest changes
@webhook.route('/ui', methods=["GET"])
def api_route():
    pull_requests_data = collection.find().sort("timestamp",-1)
    return render_template('index.html',pull_requests_data=pull_requests_data)

# for fetchind the data in mongodb
# @webhook.route('/api/data')
# def get_data():
#     <--------- Dont have to use this here ---------->
#     <--------- In html data already passed --------->
#     pull_requests = collection.find().sort("timestamp",-1)
#     # Convert ObjectId to strings
#     pull_requests = [{**pr, '_id': str(pr['_id'])} for pr in pull_requests]
#     return jsonify(pull_requests)