from time import time
from django.utils import timezone
from django.core.files import File
tensorflow_import_start = time()

from .models import Plant
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image

tensorflow_import_end = time()
print(f"Tensorflow load time: {tensorflow_import_end-tensorflow_import_start}")
from .models import Detection, Disease

def load_prediction_models():
    print("Loading latest models started")
    models_load_start = time()
    prediction_models = {}

    for plant in Plant.objects.all():
        model_path = plant.prediction_model.path
        model = keras.models.load_model(model_path)
        #model = model_path
        prediction_models[plant.name] = model

    print("Loading latest models ended")
    models_load_end = time()
    print(f"Models load time: {models_load_end-models_load_start}")
    return prediction_models

def predict(models, detection : Detection):
    detection_start = time()

    #Load image,resize,convert to array
    img_data = Image.open(detection.img_path.path).resize((256,256))
    img = np.array(img_data)
    img_array = tf.expand_dims(img, 0)
    
    model = models.get(detection.plant_type.name)

    predictions = model.predict(img_array)
    
    #Update detection
    #detection.img_path = File(img_data)
    detection.completion_time = timezone.now()
    detection._complete = True

    predicted_class = np.argmax(predictions[0])
    disease = Disease.objects.filter(plant=detection.plant_type, keyword=predicted_class).first()
    detection.disease_detected = disease

    confidence = round(100 * (np.max(predictions[0])), 2)
    detection.confidence = confidence

    #Store resized image
    img_data.save(f"{detection.img_path.path}")

    detection.save()

    detection_end = time()
    print("Time taken for detection: ", detection_end - detection_start)
    return predicted_class, confidence