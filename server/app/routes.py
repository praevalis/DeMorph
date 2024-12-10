import os
from app import app
from flask import request, jsonify
from flask_cors import CORS
from utils.video_processing import videoPreprocessingPipeline
from services.detection import *

CORS(app)
@app.route('/api/upload', methods=['POST'])
def upload_video():
    """Fetches video from client"""
    if 'video' not in request.files:
        return jsonify({'error': 'No video file uploaded'}), 400

    video_file = request.files['video']
    video_path = os.path.join('uploads', 'videos', video_file.filename)
    video_file.save(video_path)

CORS(app)
@app.route('/api/inference', methods=['POST'])
def return_inference():
    """Returns inference to client"""
    

