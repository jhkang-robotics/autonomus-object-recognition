from lxml import etree
from PIL import Image
import csv
import os
import io
#이미지 파일 경로
IMG_PATH = "/home/kjh/workspace/Car_object_Award/yolov5/runs/detect/exp2"
fw = os.listdir(IMG_PATH)

#xml파일 저장경로
save_path = "/home/kjh/workspace/final"

# txt_folder is txt file root that using darknet rectbox
txt_folder = "/home/kjh/workspace/labels"

#edit your label set
labels = ['Vehicle','Pedestrian','TrafficLight','TrafficSign']
def csvread(fn):
    with open(fn, 'r') as csvfile:
      list_arr = []
      reader = csv.reader(csvfile, delimiter=' ')

      for row in reader:
        list_arr.append(row)
    return list_arr

def convert_label(txt_file):
    global label
    for i in range(len(labels)):
        if int(txt_file) == i:
            label = labels[i]
            return label
#core code = convert the yolo txt file to the x_min, x_max..

def extract_coor(txt_file, img_width, img_height):
    x_rect_mid = float(txt_file[1])
    y_rect_mid = float(txt_file[2])
    width_rect = float(txt_file[3])
    height_rect = float(txt_file[4])

    x_min_rect = ((2 * x_rect_mid * img_width) - (width_rect * img_width)) / 2
    x_max_rect = ((2 * x_rect_mid * img_width) + (width_rect * img_width)) / 2
    y_min_rect = ((2 * y_rect_mid * img_height) - (height_rect * img_height)) / 2
    y_max_rect = ((2 * y_rect_mid * img_height) + (height_rect * img_height)) / 2

    return x_min_rect, x_max_rect, y_min_rect, y_max_rect

for line in fw:
    root = etree.Element("annotation")

    #try debug to check your path
    img_style = IMG_PATH.split('/')[-1]
    img_name = line
    image_info = IMG_PATH + "/" + line
    img_txt_root = txt_folder + "/" + line[:-4]
    txt = ".txt"

    txt_path = img_txt_root + txt
    txt_file = csvread(txt_path)
    #####################################

    #read the image information
    img_size = Image.open(image_info).size

    img_width = img_size[0]
    img_height = img_size[1]
    img_depth = Image.open(image_info).layers
    #######################################


    for ii in range(len(txt_file)):
        label = convert_label(txt_file[ii][0])
        score = txt_file[ii][-1]
        x_min_rect, x_max_rect, y_min_rect, y_max_rect = extract_coor(
            txt_file[ii], img_width, img_height)

        object = etree.Element("object")
        ####################object - element##################
        name = etree.SubElement(object, "name")
        name.text = "%s" % (label)

        bndbox = etree.SubElement(object, "bndbox")
        #####sub_sub########
        xmin = etree.SubElement(bndbox, "xmin")
        xmin.text = "%d" % (x_min_rect)
        ymin = etree.SubElement(bndbox, "ymin")
        ymin.text = "%d" % (y_min_rect)
        xmax = etree.SubElement(bndbox, "xmax")
        xmax.text = "%d" % (x_max_rect)
        ymax = etree.SubElement(bndbox, "ymax")
        ymax.text = "%d" % (y_max_rect)
        #####sub_sub########

        root.append(object)
        ####################################################
        confidence = etree.Element("confidence")
        confidence.text = "%s" % (score)

        root.append(confidence)

    file_output = etree.tostring(root, pretty_print=True, encoding='UTF-8')
    # print(file_output.decode('utf-8'))
    ff = io.open(save_path + '/' + '%s_v001_1.xml' % (img_name[:-4]), 'w', encoding="utf-8")
    ff.write(file_output.decode('utf-8'))
