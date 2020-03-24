# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 21:13:15 2020

@author: Gebruiker
"""

# coding: utf-8

import xml.etree.ElementTree as ET
import os
import random

names_dict = {"nurdle": 1, "w":2}
"""
cnt = 0
f = open('./voc_names.txt', 'r').readlines()
for line in f:
    line = line.strip()
    names_dict[line] = cnt
    cnt += 1
"""
voc_07 = 'data'


anno_path = 'data/Annotations'
img_path = 'data/JPEGImages'

N = 18
numbers = [str(k) for k in range(1,N)]
random.shuffle(numbers)

train = numbers[0:9]
test = numbers[9:]


def parse_xml(path):
    tree = ET.parse(path)
    img_name = path.split('/')[-1][:-4]
    
    height = tree.findtext("./size/height")
    width = tree.findtext("./size/width")

    objects = [img_name, width, height]

    for obj in tree.findall('object'):
        difficult = obj.find('difficult').text
        if difficult == '1':
            continue
        name = obj.find('name').text
        bbox = obj.find('bndbox')
        xmin = bbox.find('xmin').text
        ymin = bbox.find('ymin').text
        xmax = bbox.find('xmax').text
        ymax = bbox.find('ymax').text

        name = str(names_dict[name])
        objects.extend([name, xmin, ymin, xmax, ymax])
    if len(objects) > 1:
        return objects
    else:
        return None

test_cnt = 0
def gen_test_txt(txt_path):
    global test_cnt
    f = open(txt_path, 'w')


    img_names = test
    for img_name in img_names:
        img_name = img_name.strip()
        xml_path = anno_path + '/' + img_name + '.xml'
        objects = parse_xml(xml_path)
        if objects:
            objects[0] = img_path + '/' + img_name + '.jpg'
            if os.path.exists(objects[0]):
                objects.insert(0, str(test_cnt))
                test_cnt += 1
                objects = ' '.join(objects) + '\n'
                f.write(objects)
    f.close()


train_cnt = 0
def gen_train_txt(txt_path):
    global train_cnt
    f = open(txt_path, 'w')

    img_names = train
    for img_name in img_names:
        img_name = img_name.strip()
        xml_path = anno_path + '/' + img_name + '.xml'
        objects = parse_xml(xml_path)
        if objects:
            objects[0] = img_path + '/' + img_name + '.jpg'
            if os.path.exists(objects[0]):
                objects.insert(0, str(train_cnt))
                train_cnt += 1
                objects = ' '.join(objects) + '\n'
                f.write(objects)
    f.close()


gen_train_txt('train.txt')
gen_test_txt('val.txt')