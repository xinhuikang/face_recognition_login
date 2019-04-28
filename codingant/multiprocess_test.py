from multiprocessing import Process
from multiprocessing import Manager
from multiprocessing import Pool
import cv2
import ffmpy3
import os, glob, sys, time
import face_recognition
import math


def eye_aspect_ratio(eye):
    point0 = eye[0]
    point1 = eye[1]
    point2 = eye[2]
    point3 = eye[3]
    point4 = eye[4]
    point5 = eye[5]
    temp = math.pow(point1[0] - point5[0], 2), math.pow(point1[1] - point5[1], 2)
    distance1 = math.sqrt(math.fsum(temp))
    temp = math.pow(point2[0] - point4[0], 2), math.pow(point2[1] - point4[1], 2)
    distance2 = math.sqrt(math.fsum(temp))
    temp = math.pow(point0[0] - point3[0], 2), math.pow(point0[1] - point3[1], 2)
    distance3 = math.sqrt(math.fsum(temp))
    return (distance1 + distance2) / (2 * distance3)


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
        outputs={outfile: '-r 25 -y'}
    )
    ff.run()


def piece_state(f, i, dict):
    unknown_face = face_recognition.load_image_file(f)
    locate_unknown_face = face_recognition.face_locations(unknown_face)
    landmards = face_recognition.face_landmarks(unknown_face, locate_unknown_face)
    left_eye = landmards[0]['left_eye']
    right_eye = landmards[0]['right_eye']
    left_ear = eye_aspect_ratio(left_eye)
    right_ear = eye_aspect_ratio(right_eye)
    dict[i] = (left_ear, right_ear)


def detection_blink():
    num = 0
    left_blink, right_blink = (False, False)
    infile = 'temp.webm'
    outfile = 'temp.mp4'
    translate(infile, outfile)
    video2frame(outfile)
    pool = Pool(processes=4)
    results = []
    dict = Manager().dict()

    files = glob.glob(os.path.join('.', "*.jpg"))
    print('files', files)
    for f, i in zip(files, range(len(files))):
        pool.apply_async(piece_state, (f, i, dict))

    pool.close()
    pool.join()

    print('dict:', dict)
    for i in sorted(dict):
        left_ear, right_ear = dict[i]
        if left_ear < 0.20:
            left_blink = True
        if right_ear < 0.20:
            right_blink = True

        if left_ear >= 0.20 and right_ear >= 0.20 and left_blink and right_blink:
            num += 1
            right_blink = False
            left_blink = False

    return num

import numpy as np
if __name__ == '__main__':
    start = time.clock()
    number = detection_blink()
    end = time.clock()
    np.save('temp', number)