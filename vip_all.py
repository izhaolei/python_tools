#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 10:50:07 2017

@author: zhaolei
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 15:43:34 2017

@author: zhaolei
"""

import os
import cv2
import time

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
    
def write_labels(paths,path,new_dir,files,label_dir):
    print('now processing : '+path)
    video=cv2.VideoCapture(path)
    fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    success, frame = video.read()
    labels=get_labels(label_dir)
    i=1
    sums=0
    start=time.time()
    while success:
        if(i in labels.keys()):
            sums+=1
            if(sums==3):
                sums=0
                label=labels[i]
                cv2.imwrite(os.path.join(paths,'images',new_dir+u'{:03d}.jpg'.format(i)),frame)
                for j in range(len(label)/5):
                    line=[new_dir+u'{:03d}.jpg'.format(i),str(label[j*5+1]),str(label[j*5+2]),str(label[j*5+3]),str(label[j*5+4]),str(label[j*5])]
                    files.writelines(','.join(line))
                    files.write(u'\n')
                cv2.waitKey(10/int(fps)) #延迟
        success, frame = video.read()
        i+=1
    video.release()
    end=time.time()
    print('cost time: {} s'.format(end-start)) 

        
        
path='/media/disks/DATA/Data/VIP'

files=os.listdir(path)
f=open(os.path.join(path,'label.txt'),'w')
os.mkdir(os.path.join(path,u'images'))
for i in files:
    if '.mp4' in i:
        li=i.rstrip()
        da=li.split('_')
        da=da[:-1]
        newdir=''.join(da)
        vedio_dir=os.path.join(path,i)
        label_dir=os.path.join(path,'labels',i[:5]+'.txt')
        print label_dir
        #os.mkdir(newdir)
        write_labels(path,vedio_dir,newdir,f,label_dir)
f.close()