from flask import Flask, request, jsonify, render_template, send_file
from src.exception import CustomException
from src.logger import logging as lg
import os, sys

from src.pipeline.predict_pipeline import PredictionPipeline
from src.pipeline.training_pipeline import TrainingPipeline

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify("Website main page/home")

@app.route('/train')
def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return "Training Completed"
    
    except CustomException as e:
        raise CustomException(e, sys) from e
    
@app.route('/predict', methods=['POST', 'GET'])
def predict():
    try:
        if request.method == 'POST':
            prediction_pipeline = PredictionPipeline(request)
            prediction_file_detail = prediction_pipeline.run_pipeline()

            lg.info("prediciton completed. Downloading predition file.")
            return send_file(prediction_file_detail.prediction_file_path, 
                             download_name = prediction_file_detail.prediction_file_name,
                             as_attachment = True) 

        else:
            return render_template('prediction.html')   
           
    
    except CustomException as e:
        raise CustomException(e, sys) from e

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug = True)