
import numpy as np
import os
from PIL import Image
from PIL import ImageFilter
import cv2

def video_length(video_path):
    cap = cv2.VideoCapture(video_path)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return length

#extract frames from imput video
def extract_frames(video_path, save_path):
    print('***EXTRACTING FRAMES***')
    _, file_name = os.path.split(video_path)
    
    cap = cv2.VideoCapture(video_path)
    
    ct = 1
    ret, frame = cap.read()
    while ret:
        cv2.imwrite(os.path.join(save_path, '{}.jpg'.format(ct)), frame)
        ret, frame = cap.read()
        ct += 1
    cap.release()
    print('***FINISHED EXTRACTION***')

#process individual images
def image_process(save_path, output_path):
    for image_path in os.listdir(save_path):
        if image_path.endswith('.jpg'):
            #rotate and crop each frame
            input_path = os.path.join(save_path, image_path)
            im = Image.open(input_path)
            full_out_path = os.path.join(output_path, image_path)
            im.crop((960, 0, 962, 1080)).save(full_out_path)
        else:
            continue
    
def concat_images(image_list):
    _im = image_list.pop(0)
    _im = Image.open(os.path.join(output_path, _im))
    for im in image_list:
        if im.endswith('.jpg'):
            im = Image.open(os.path.join(output_path, im))
            dst = Image.new('RGB', (_im.width + im.width, im.height), (0, 0, 0))
            dst.paste(_im, (0, 0))
            dst.paste(im, (_im.width, 0))
            _im = dst
    print(type(_im))
    _im.save('out.jpeg')

def make_list(video):
    image_list = []
    ct = 1
    for i in range(int(video_length(video))):
        path = '{}.jpg'.format(ct)
        image_list.append(path)
        ct += 1
    return image_list

def delete_frames(save_path, output_path):
    for i in os.listdir(save_path):
        if i.endswith('.jpg'):
            os.remove(os.path.join(save_path, i))
    
    for i in os.listdir(output_path):
        if i.endswith('.jpg'):
            os.remove(os.path.join(output_path, i))



if __name__ == '__main__':
    video = 'input.mp4'
    save_path = 'frames'
    output_path = 'processed frames'
    extract_frames(video, save_path)
    image_process(save_path, output_path)
    image_list = make_list(video)
    concat_images(image_list)
    delete_frames(save_path, output_path)
    
