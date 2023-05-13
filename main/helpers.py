import os, random
from django.utils.deconstruct import deconstructible
from datetime import datetime

@deconstructible 
class UploadTo:
    def __init__(self, folder):
        self.folder = folder
    
    def __call__(self, instance, filename): 
        ext = os.path.splitext(filename)[1]
        return "{}/{}/{:%Y-%m}/{:%Y-%m-%d-%H-%M-%S}-{}{}".format(
            self.folder,
            instance.patient_history,
            datetime.now(),
            datetime.now(),
            random.randint(1000, 9999),
            ext
        )