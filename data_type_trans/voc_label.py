import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets=[('2007', 'train')]

classes = ["Vehicle",  "Pedestrian",  "TrafficLight",  "TrafficSign"]


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh

    temp = 0

    if x < 0 or w < 0 or y < 0 or h < 0:
        temp = 1

    return (x,y,w,h),temp

#def convert(size, box):
#        image_width = 1.0 * size[0]
#        image_height = 1.0 * size[1]

        #box = obj.box
#        absolute_x = box[0] + 0.5 * (box[1] - box[0])
#        absolute_y = box[2] + 0.5 * (box[3] - box[2])

#       absolute_width = box[1] - box[0]
#        absolute_height = box[3] - box[2]

#        x = absolute_x / image_width
#        y = absolute_y / image_height
#        width = absolute_width / image_width
#        height = absolute_height / image_height

#       return (x, y, width, height)

def convert_annotation(year, image_id):
    in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id))
    out_file = open('VOCdevkit/VOC%s/labels/%s.txt'%(year, image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)

        if cls_id == 0 or cls_id == 1 or cls_id == 2 or cls_id == 3:
            cls_id = 0
        elif cls_id == 4 or cls_id == 5:
            cls_id = 1
        elif cls_id == 6 or cls_id == 7 or cls_id == 8 or cls_id == 9 or cls_id == 10 or cls_id == 11 or cls_id == 12:
            cls_id = 2
        elif cls_id == 13 or cls_id == 14:
            cls_id = 3

        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb,temp = convert((w,h), b)

        if temp == 0:
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

for year, image_set in sets:
    if not os.path.exists('VOCdevkit/VOC%s/labels/'%(year)):
        os.makedirs('VOCdevkit/VOC%s/labels/'%(year))
    image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
    list_file = open('%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg\n'%(wd, year, image_id))
        convert_annotation(year, image_id)
    list_file.close()

os.system("cat 2007_train.txt  > train.txt")
os.system("cat 2007_train.txt  > train.all.txt")

