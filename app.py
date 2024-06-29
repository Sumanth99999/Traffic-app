from flask import *
import os
from werkzeug.utils import secure_filename
from keras.models import load_model
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Classes of traffic signs
classes = { 0:'Speed limit (20km/h)',
            1:'Speed limit (30km/h)',      
            2:'Speed limit (50km/h)',       
            3:'Speed limit (60km/h)',      
            4:'Speed limit (70km/h)',    
            5:'Speed limit (80km/h)',      
            6:'End of speed limit (80km/h)',     
            7:'Speed limit (100km/h)',    
            8:'Speed limit (120km/h)',     
            9:'No passing',   
           10:'No passing veh over 3.5 tons',     
           11:'Right-of-way at intersection',     
           12:'Priority road',    
           13:'Yield',     
           14:'Stop',       
           15:'No vehicles',       
           16:'Veh > 3.5 tons prohibited',       
           17:'No entry',       
           18:'General caution',     
           19:'Dangerous curve left',      
           20:'Dangerous curve right',   
           21:'Double curve',      
           22:'Bumpy road',     
           23:'Slippery road',       
           24:'Road narrows on the right',  
           25:'Road work',    
           26:'Traffic signals',      
           27:'Pedestrians',     
           28:'Children crossing',     
           29:'Bicycles crossing',       
           30:'Beware of ice/snow',
           31:'Wild animals crossing',      
           32:'End speed + passing limits',      
           33:'Turn right ahead',     
           34:'Turn left ahead',       
           35:'Ahead only',      
           36:'Go straight or right',      
           37:'Go straight or left',      
           38:'Keep right',     
           39:'Keep left',      
           40:'Roundabout mandatory',     
           41:'End of no passing',      
           42:'End no passing veh > 3.5 tons' }

def is_valid_image(file_data):
    try:
        Image.open(io.BytesIO(file_data)).verify()
        return True
    except Exception as e:
        print("Invalid Image:", e)
        return False

def image_processing(file_data):
    if not is_valid_image(file_data):
        return "Not a valid image"
    
    try:
        model = load_model('traffic_classifier.h5')
        image = Image.open(io.BytesIO(file_data))
        image = image.resize((30,30))
        data = np.array(image)
        X_test = np.array([data])
        Y_pred = model.predict(X_test)
        predicted_class = np.argmax(Y_pred)
        return classes[predicted_class]
    except Exception as e:
        print("Prediction Error:", e)
        return "Not a Valid Image"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        file_data = f.read()
        # Make prediction
        result = image_processing(file_data)
        result = "Predicted Traffic🚦Sign is: " + result
        f.close()  # Close the file object
        return result
    return "Invalid request"

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5050,debug=True)
