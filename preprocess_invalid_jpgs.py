import os
import subprocess
from concurrent.futures import ProcessPoolExecutor
from PIL import Image

VEHICLE_PATH = "/fast/MIT_SCL_V2/train/"

_, VEHICLE_MODELS, _ = next(os.walk(VEHICLE_PATH))

def convert_images(vehicle_image):
        try:
            image = Image.open(vehicle_image)
            image.close()
        except Exception as e:
            print(f"Coming to exception: {e}{vehicle_image}")
            try:
                subprocess.run(["mogrify", "-format", "jpg", f"{vehicle_image}"])
                try:
                    Image.open(vehicle_image)
                except Exception as e:
                    print("Convert also does not fix")
                    subprocess.run(["rm", f"{vehicle_image}"])
            except Exception as e:
                print(e)
                print("Cannot use convert command")
                subprocess.run(["rm", f"{vehicle_image}"])
            

vehicle_images_list = []
for i, vehicle in enumerate(sorted(VEHICLE_MODELS)):
    print(i, vehicle)
    _, _, VEHICLE_IMAGES = next(os.walk(VEHICLE_PATH+vehicle))
    
    for i, vehicle_image in enumerate(VEHICLE_IMAGES):
        vehicle_images_list.append(f"{VEHICLE_PATH + vehicle + '/' + vehicle_image}")

with ProcessPoolExecutor() as executor:
    executor.map(convert_images, vehicle_images_list)