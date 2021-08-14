
import os
import io

import torchvision.transforms as transforms
import torchvision as tv
import torch
from PIL import Image
import onnx

from resizeimage import resizeimage


def get_model() :
    # Preprocessing: load the ONNX model
    model_path = os.path.join('models', 'MedNet.onnx')
    model = onnx.load(model_path)
    # Check the model
    try:
        onnx.checker.check_model(model)
    except onnx.checker.ValidationError as e:
        print('The model is invalid: %s' % e)
    else:
        print('The model is valid!')
    return model

def transform_image(image_bytes) : 
    img = Image.open(io.BytesIO(image_bytes))
    # print('Size before : ',float(img.size[0]),float(img.size[1]))
    size = 64, 64
    # img.thumbnail(size, Image.ANTIALIAS)
    # img.resize(size, Image.ANTIALIAS)
    # img = resizeimage.resize_thumbnail(img, size)
    img = img.resize(size)
    # print('Size after : ',float(img.size[0]),float(img.size[1]))
    img_y = scaleImage(img)
    img_y.unsqueeze_(0)
    return img_y

def format_class_name(class_name):
    class_name = class_name.title()
    return class_name

# Pass a PIL image, return a tensor
def scaleImage(x):          
    toTensor = tv.transforms.ToTensor()
    y = toTensor(x)
    if(y.min() < y.max()):  
        y = (y - y.min())/(y.max() - y.min()) 
    z = y - y.mean()        
    return z

