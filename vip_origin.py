#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 15:43:34 2017

@author: zhaolei
"""

import os
import cv2

def get_axes(*lis):
    liss= list(lis[1:4])
    
    liss.append(lis[8])
    liss.append(lis[9])
    return liss
    
def get_labels(dirs):
    labels=dict()
    file=open(dirs)
    first_line=file.readline()
    first_line=first_line.rstrip()
    lines=file.readlines()
    for line in lines:
        li=line.rstrip()
        da=li.split('_')
        dat=list(int(i) for i in da)
        if dat[0] in labels.keys():
            labels[dat[0]]+=get_axes(*dat)
        else:
            labels[dat[0]]=get_axes(*dat)
    return labels
    
def write_labels(path,new_dir,files,label_dir):
    print('now processing : '+path)
    video=cv2.VideoCapture(path)
    fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    success, frame = video.read()
    labels=get_labels(label_dir)
    i=1
    while success:
        print i
        if(i in labels.keys()):
            label=labels[i]
            cv2.imwrite(os.path.join(new_dir,'{:05d}.jpg'.format(i)),frame)
            for j in range(len(label)/5):
                line=[new_dir[-5:]+u'/{:05d}.jpg'.format(i),str(label[j*5+1]),str(label[j*5+2]),str(label[j*5+3]),str(label[j*5+4]),str(label[j*5])]
                files.writelines(','.join(line))
                files.write(u'\n')
        cv2.waitKey(10/int(fps)) #延迟
        success, frame = video.read()
        i+=1
    video.release()

        
        
path='/media/disks/DATA/Data/test'

files=os.listdir(path)
f=open(os.path.join(path,'label.txt'),'w')
for i in files:
    if '_00_00_00.mp4' in i:
        newdir=os.path.join(path,i[:-4])
        vedio_dir=os.path.join(path,i)
        label_dir=os.path.join(path,'labels',i[:5]+'.txt')
        print label_dir
        os.mkdir(newdir)
        write_labels(vedio_dir,newdir,f,label_dir)
f.close()
