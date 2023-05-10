import os
from os.path import join, dirname
from dotenv import load_dotenv


from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient('mongodb://ghozialko:ghozai182@ac-hdy0ugk-shard-00-00.u50i71m.mongodb.net:27017,ac-hdy0ugk-shard-00-01.u50i71m.mongodb.net:27017,ac-hdy0ugk-shard-00-02.u50i71m.mongodb.net:27017/?ssl=true&replicaSet=atlas-edifbm-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    # sample_receive = request.form.get('sample_give')
    # print(sample_receive)
    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    profile_name = f'profile-{mytime}.{extension}'
    save_to = f'static/{profile_name}'
    profile.save(save_to)

    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    doc = {
        'file': filename,
        'profile': profile_name,
        'title': title_receive,
        'content': content_receive,
        'date': mytime
    }
    db.diary.insert_one(doc)
    return jsonify({'message': 'data was saved!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)