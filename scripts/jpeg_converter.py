import os
from PIL import Image

input_folder = input("Insert input folder path: ")
output_folder = input("Insert output folder path: ")

def tif_to_jpeg(input_folder, output_folder):

    os.makedirs(output_folder, exist_ok=True)
    
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.lower().endswith(".tif") or filename.lower().endswith(".tiff"):
                path = os.path.join(root, filename)
                img = Image.open(path).convert("RGB")
                out = os.path.join(output_folder, filename.rsplit(".", 1)[0] + ".jpg")
                img.save(out, "JPEG", quality=100)

    print("Done! Saved in " + output_folder)

tif_to_jpeg(input_folder, output_folder)

