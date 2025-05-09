import os
import csv
import json
import base64
from sympy import Eq
from collections import defaultdict

def get_image_paths(directory):
    image_extensions = ('.jpg', '.jpeg', '.png')
    image_paths = []
    absolute_directory = os.path.abspath(directory)

    for root, _, files in os.walk(absolute_directory):
        for file in files:
            if file.lower().endswith(image_extensions):
                image_paths.append(os.path.join(root, file))
    return image_paths

#returns a dictionary of filename to json path for each image
def get_json_dict(directory):
    jsonpaths = {}
    absolute_directory = os.path.abspath(directory)

    for root, _, files in os.walk(absolute_directory):
        for file in files:
            if file.lower().endswith('.json'):
                json_path = os.path.join(root, file)
                # Derive the corresponding image filename (same basename, different extension)
                base_name = os.path.splitext(file)[0]
                jsonpaths[base_name] = json_path
    return jsonpaths


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


class Logger:
    def __init__(self, log_path = './logs'):
        self.chat_log = open(f'{log_path}/gpt_log.csv', 'w',encoding='utf-8')
        self.seek_log = open(f'{log_path}/seek_log.csv', 'w',encoding='utf-8')

        self.type_errors = 0

        #this is horrible, truly
        self.chat_ptype_buckets = defaultdict(lambda:0)
        self.seek_ptype_buckets = defaultdict(lambda:0)

        self.chat_actor_buckets = defaultdict(lambda:0)
        self.seek_actor_buckets = defaultdict(lambda:0)

        self.chat_augment_buckets = defaultdict(lambda: 0)
        self.seek_augment_buckets = defaultdict(lambda: 0)
        
    def log_gpt(self, fname, iscorrect : bool, aug_code, actor, ptype):
        try:
            self.chat_log.write(f'{fname},{"✅" if iscorrect else "❌"}\n')

            if iscorrect:
                self.chat_ptype_buckets[f'{ptype}-right'] += 1
                self.chat_actor_buckets[f'{actor}-right'] += 1
                self.chat_augment_buckets[f'{aug_code}-right'] += 1
            else:
                self.chat_ptype_buckets[f'{ptype}-wrong'] += 1
                self.chat_actor_buckets[f'{actor}-wrong'] += 1
                self.chat_augment_buckets[f'{aug_code}-wrong'] += 1
            
            print(f'GPT:{fname}:{"✅" if iscorrect else "❌"}')
        except TypeError:
            self.type_errors += 1
            print("type errors: ", self.type_errors)
    
    def log_seek(self, fname, iscorrect : bool, aug_code, actor, ptype):
        try:
            self.seek_log.write(f'{fname},{"✅" if iscorrect else "❌"}\n')

            if iscorrect:
                self.seek_ptype_buckets[f'{ptype}-right'] += 1
                self.seek_actor_buckets[f'{actor}-right'] += 1
                self.seek_augment_buckets[f'{aug_code}-right'] += 1
            else:
                self.seek_ptype_buckets[f'{ptype}-wrong'] += 1
                self.seek_actor_buckets[f'{actor}-wrong'] += 1
                self.seek_augment_buckets[f'{aug_code}-wrong'] += 1
            
            print(f'Seek:{fname}:{"✅" if iscorrect else "❌"}')
        except TypeError:
            self.type_errors += 1
            print("type errors: ", self.type_errors)

    def __del__(self):
        self.chat_log.close()
        self.seek_log.close()
        
        #I just don't know what to say except I'm so done with this project
        with open("./logs/seek_aug.json", "w") as f:
           json.dump(self.seek_augment_buckets, f, indent=4)
        with open("./logs/chat_aug.json", "w") as f:
           json.dump(self.chat_augment_buckets, f, indent=4)

        with open("./logs/seek_actor.json", "w") as f:
           json.dump(self.seek_actor_buckets, f, indent=4)
        with open("./logs/chat_actor.json", "w") as f:
           json.dump(self.chat_actor_buckets, f, indent=4)

        with open("./logs/seek_ptype.json", "w") as f:
           json.dump(self.seek_ptype_buckets, f, indent=4)
        with open("./logs/chat_ptype.json", "w") as f:
           json.dump(self.chat_ptype_buckets, f, indent=4)
