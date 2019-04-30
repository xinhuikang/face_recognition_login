from multiprocessing import Process
from multiprocessing import Manager
from multiprocessing import Pool
import cv2
import ffmpy3
import os, glob, sys, time
import face_recognition
import math


def mouth_aspect_ratio(top_lip, bottom_lip):
    point0 = top_lip[7]
    point1 = top_lip[8]
    point2 = top_lip[9]
    point3 = top_lip[10]
    point4 = top_lip[11]
    point5 = bottom_lip[8]
    point6 = bottom_lip[9]
    point7 = bottom_lip[10]
    temp = math.pow(point1[0] - point7[0], 2), math.pow(point1[1] - point7[1], 2)
    distance0 = math.sqrt(math.fsum(temp))
    temp = math.pow(point2[0] - point6[0], 2), math.pow(point2[1] - point6[1], 2)
    distance1 = math.sqrt(math.fsum(temp))
    temp = math.pow(point3[0] - point5[0], 2), math.pow(point3[1] - point5[1], 2)
    distance2 = math.sqrt(math.fsum(temp))
    temp = math.pow(point0[0] - point4[0], 2), math.pow(point0[1] - point4[1], 2)
    distance3 = math.sqrt(math.fsum(temp))
    return (distance0 + distance1 + distance2) / (3 * distance3)
    


def video2frame(videofile):
    # 读取视频
    cap = cv2.VideoCapture(videofile)
    # 获取FPS(每秒传输帧数(Frames Per Second))
    fps = cap.get(cv2.CAP_PROP_FPS)
    # 获取总帧数
    totalFrameNumber = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(fps)
    print(totalFrameNumber)
    # 当前读取到第几帧
    COUNT = 0

    # 若小于总帧数则读一帧图像
    while COUNT < totalFrameNumber:
        # 一帧一帧图像读取
        ret, frame = cap.read()
        # 把每一帧图像保存成jpg格式（这一行可以根据需要选择保留）
        cv2.imwrite(str(COUNT).zfill(3) + '.jpg', frame)
        # 显示这一帧地图像
        # cv2.imshow('video', frame)
        COUNT = COUNT + 1
        # 延时一段33ms（1s➗30帧）再读取下一帧，如果没有这一句便无法正常显示视频
        cv2.waitKey(33)

    cap.release();


def translate(infile, outfile):
    ff = ffmpy3.FFmpeg(
        inputs={infile: None},
        outputs={outfile: '-r 25 -y -an'}
    )
    ff.run()


def mouth_state(f, i, dict):
    start = time.clock()
    for ff, ii in zip(f, range(len(f))):
        unknown_face = face_recognition.load_image_file(ff)
        locate_unknown_face = face_recognition.face_locations(unknown_face)
        landmards = face_recognition.face_landmarks(unknown_face, locate_unknown_face)
        top_lip = landmards[0]['top_lip']
        bottom_lip = landmards[0]['bottom_lip']
        mouth_mar = mouth_aspect_ratio(top_lip, bottom_lip)
        dict[ii + i] = (mouth_mar)

    end = time.clock()
    print('piece_time:', end - start)

import multiprocessing
def detection_open():
    num = 0
    mouth_open = (False)
    infile = 'test.webm'#'Android-webm/temp.webm'
    outfile = 'temp.mp4'
    
    start = time.clock()
    translate(infile, outfile)
    video2frame(outfile)
    end = time.clock()
    print('trans_time:', end - start)
    
    start = time.clock()
    dict = Manager().dict()

    files = glob.glob(os.path.join('.', "*.jpg"))
    step = int(len(files) / 3) + 1
    jpgs = [files[i:i + step] for i in range(0, len(files), step)]
    jobs = []
#    print('jpgs', jpgs)
    for f, i in zip(jpgs, range(3)):
        p = multiprocessing.Process(target=mouth_state, args=(f, i * step, dict))
        jobs.append(p)
        p.start()

    for i in jobs:
        i.join()

#    print('dict:', dict)
    for i in sorted(dict):
        print(i, dict[i])
        mouth_mar = dict[i]
        if mouth_mar < 0.7:
            mouth_open = True

        if mouth_mar >= 0.7 and mouth_open:
            num += 1
            mouth_open = False
    #os.system('del *.mp4 *.jpg')
    
    end = time.clock()
    print('time:', end - start)
    return num


if __name__ == '__main__':
#    start = time.clock()
    number = detection_open()
#    end = time.clock()
    print(number)