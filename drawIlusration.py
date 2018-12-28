#-*-coding: utf-8 -*-

import sys
import mcpi.minecraft as minecraft
import mcpi.block as block
import cv2
import numpy as np
import pdb

def decleaseColor(img, NC = 4):
    '''
    #IMG = decleaseColor(img,<Number_of_Colors(色数)=64>)
    #注：色数分だけループが走るので、色数が大きくなればなるほど処理重く なるはず。
    '''
    if NC >256 : NC = 256 #一応、処理が無理な数値が来た時用に。

    ###分割処理用のステップデータの作成
    CS = 256/NC # CS=ColorStepsの意。
    steps = [] #ここに分割させる処理単位と設定する色が格納される[(色範 囲の下限1,色範囲の上限1,設定する色1),(色範囲の下限2,色範囲の上限2,設定す る 色2),...]
    stepF = range(1,257,CS)
    stepE = range(CS,256+CS,CS)
    for i in range(0,len(stepF)):
        steps.append((stepF[i],stepE[i],(stepF[i]+stepE[i])/2))

    ###画像の分割処理
    rgb = cv2.split(img)
    for col in rgb:
        for step in steps:
            idx = np.where((step[0] <= col) & (col <= step[1]))
            col[idx] = step[2]

    r_img = cv2.merge(rgb)
    return r_img

if __name__ == '__main__':

    #標準入力からのカメラの設定
    argvs = sys.argv  # コマンドライン引数を格納したリストの取得
    argc = len(argvs) # 引数の個数
    if (argc < 2):
        # 引数が足りない場合は、その旨を表示
        print 'Usage: # '
        print 'Usage: # 例）　Python TakeImages.py 1'
        print 'Usage: # '
    else:
        if len(argvs[1]) > 2:
            imgPath = argvs[1]
            imgSize = int(argvs[2])
        else:
            CamNo = int(argvs[1])
    #pdb.set_trace()
    # create img data
    img = cv2.imread(imgPath)
    y,x,_ = img.shape
    if x>=y:
        res_width = imgSize
        res_height = int(y*imgSize/x)
    else:
        res_width = int(x*imgSize/y)
        res_height = imgSize

    #pdb.set_trace()
    resize_img = cv2.resize(img,(res_width,res_height))
    dec_img = decleaseColor(resize_img,4)
    cv2.imshow("test",dec_img)
    cv2.moveWindow("test",0,0)
    cv2.waitKey(0)
    
    # create in minecraft
    mc = minecraft.Minecraft.create()
    mc.postToChat("Hello World!")
    #mc.player.setTilePos(0,0,100)
    
    pos = mc.player.getTilePos()
    

    ###分割処理用のステップデータの作成
    CS = 180/8 # CS=ColorStepsの意。
    steps = [] #ここに分割させる処理単位と設定する色が格納される[(色範 囲の下限1,色範囲の上限1,設定する色1),(色範囲の下限2,色範囲の上限2,設定す る 色2),...]
    #stepF = range(1,180)
    #stepE = range(CS,180+CS,CS)
    #for i in range(0,len(stepF)):
    #    steps.append((stepF[i],stepE[i],(stepF[i]+stepE[i])/2))
    steps.append((0,29,1,9))
    steps.append((30,59,2,10))
    steps.append((60,89,3,11))
    steps.append((90,119,4,12))
    steps.append((120,149,5,13))
    steps.append((150,180,6,14))
    
    ###画像の分割処理
    #hsv = cv2.split(cv2.cvtColor(resize_img,cv2.COLOR_BGR2HSV))
    flip_res_img = cv2.flip(resize_img,-1)
    hsv = cv2.cvtColor(flip_res_img,cv2.COLOR_BGR2HSV)
    #h,s,v = cv2.split(hsv)
    #pdb.set_trace()
    for y,ret in enumerate(hsv):
        for x,(h,s,v) in enumerate(ret):
            # white-black
            if s <= 127 and v <= 64:
                mc.setBlock(pos.x+x,pos.y+y,0,block.Block(35,15))
            elif s <= 127 and v <= 128:
                mc.setBlock(pos.x+x,pos.y+y,0,block.Block(35,7))
            elif s <= 127 and v <= 192:
                mc.setBlock(pos.x+x,pos.y+y,0,block.Block(35,8))
            elif s <= 127 and v <= 255:
                mc.setBlock(pos.x+x,pos.y+y,0,block.Block(35,0))
            else: #for colors
                for step in steps:
                    if step[0] <= h and h<= step[1]:
                        if v >= 127:
                            mc.setBlock(pos.x+x,pos.y+y,0,block.Block(35,step[2]))
                        else:
                            mc.setBlock(pos.x+x,pos.y+y,0,block.Block(35,step[3]))
