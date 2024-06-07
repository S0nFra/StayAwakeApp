import os
import json
import base64

def resource_path(relative_path):
    return os.path.join(os.getcwd(), relative_path)

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

if __name__ == "__main__":
    imgs = dict()
    dir = resource_path("icon")
    exts_allowed = {".png", ".jpg"}
    for file in os.listdir(dir):
        file_name, file_extension = os.path.splitext(file)
        if file_extension not in exts_allowed:
            continue
        print(file)        
        imgs[file_name.replace("-", "_")] = encode_image(os.path.join(dir,file))

    data = json.dumps(imgs, indent=4)
    with open("./encoded_icon.txt", "w") as file:
        file.write(data)