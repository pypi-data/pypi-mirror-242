
import torch
from fastai.vision.all import *
from PIL import Image

class ImageColorizer:
    def __init__(self, model_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.learner = load_learner(model_path).to(self.device)
    
    def colorize(self, input_path, output_path):
        img = PILImage.create(input_path)
        colorized_img = self.learner.predict(img)[0]
        colorized_img.save(output_path)
