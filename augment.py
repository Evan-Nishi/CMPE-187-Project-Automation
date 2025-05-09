import os
import random

from PIL import Image, ImageEnhance
from fileutils import get_image_paths

def rotate_img(img, orientation):
    '''
    img - <PIL.Image>: the image object to be rotated
    orientation - <int>: 0 for straight, 1 for tilted, 2 for extreme
    '''
    if orientation == 'S':
        deg = random.randint(-30,30)
       
    elif orientation == 'M': #31 60
        deg = random.choice([random.randint(31,60), random.randint(-60,-31)])
    elif orientation == 'L':
        deg = random.choice([random.randint(61,150), random.randint(-150,-61)])
    
    return [orientation, img.rotate(deg, expand=True)]



# Simulate reduced brightness and contrast with the same brightness factor
def reduce_bright(img):
    enhancer = ImageEnhance.Brightness(img)
    brightness_factor = random.randint(3, 8) * 0.1
    
    img = enhancer.enhance(brightness_factor)

    contraster = ImageEnhance.Contrast(img)
    
    img = contraster.enhance(brightness_factor) 
    
    
    return [brightness_factor, img]




#image input name format: <unit>-<subchapter>-<writing type>.<file extension>
#writing type is either t for typed, m for messy, n for neat
#example: 7-8-t.png

#image output name format:
#./out/<unit>/<subchapter>-<writing type>-r<deg rotated>-b<percent brightness>.<file extension>

def save_augments(fname, target_path = './static/in1-3'):
        try:
            f_tokens = fname.split('.')
            extension = f_tokens[-1]

            if extension == 'json':
                print('got json')
                return 
            
            img = Image.open(f"{target_path}/{fname}")

            os.makedirs(target_path, exist_ok=True)

            rot_images = [
                rotate_img(img, 'S'),
                rotate_img(img, 'M'),
                rotate_img(img, 'L')
            ]

            #SN, SP
            #MN, MP
            #LN, LP
            
            for r_i in rot_images:
                r_i[1].save(f'{target_path}/{f_tokens[0]}-AUG-{r_i[0]}N.{extension}')

                b_i = reduce_bright(img)

                b_i[1].save(f'{target_path}/{f_tokens[0]}-AUG-{r_i[0]}P.{extension}')
        except Exception as e:
            print(e)

def augment_all():
    fpaths = get_image_paths('./in2-4')
    for p in fpaths:
        #if on unix like systems change this!
        case_fname = p.split('\\')[-1].split('.')[0]
        if len(case_fname.split('-AUG-')) == 1:
            #print("saving")
            save_augments(p.split('\\')[-1])

augment_all()