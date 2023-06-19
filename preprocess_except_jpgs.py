import os
import subprocess
from concurrent.futures import ProcessPoolExecutor
from PIL import Image

VEHICLE_PATH = "/fast/MIT_SCL_V2/train/"

_, VEHICLE_MODELS, _ = next(os.walk(VEHICLE_PATH))

def convert_images(vehicle_image):
        try:
            print(vehicle_image)
            if vehicle_image.endswith(".svg"):
                vehicle_image_name = os.path.splitext(vehicle_image)[0]
                subprocess.run(["rsvg-convert", f"{vehicle_image}", ">", f"{vehicle_image_name}.jpg"])
                subprocess.run(["rm", f"{vehicle_image}"])
            else:
                #Image.open(f"{vehicle_image}")
                subprocess.run(["mogrify", "-format", "jpg", f"{vehicle_image}"])
        except Exception as e:
            print(e)
            subprocess.run(["rm", f"{vehicle_image}"])


vehicle_images_list = []
for i, vehicle in enumerate(sorted(VEHICLE_MODELS)):
    print(i, vehicle)
    _, _, VEHICLE_IMAGES = next(os.walk(VEHICLE_PATH+vehicle))
    
    for i, vehicle_image in enumerate(VEHICLE_IMAGES):
        if not vehicle_image.endswith(".jpg"):
            vehicle_images_list.append(f"{VEHICLE_PATH + vehicle + '/' + vehicle_image}")
            
with ProcessPoolExecutor(max_workers=50) as executor:
    executor.map(convert_images, vehicle_images_list)
        

