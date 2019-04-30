from django.http import JsonResponse
import base64
from django.contrib.auth import login as ori_login
import face_recognition
from .models import Faces
from django.contrib.auth.models import User
import math
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import cv2
import ffmpy3
import os, glob, sys, time
from multiprocessing import Manager
from multiprocessing import Pool
import numpy as np


# Create your views here.
def login(request):
    return render(request, 'login_registration.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get("uname")
        # firstname = request.POST.get("Fname")
        # lastname = request.POST.get("Lname")
        password = request.POST.get("password")
        print(username, ':', password)
        user = User.objects.create_user(username=username, password=password)

        faceImage = request.POST.get('faceImg')
        # 提取出base64格式，并进行转换为图片
        index = faceImage.find('base64,')
        base64Str = faceImage[index + 6:]
        img = base64.b64decode(base64Str)
        fileName = 'upload/faces/' + username + '.JPG'
        with open(fileName, 'wb') as f:
            f.write(img)
        Faces.objects.create(user=user, face_img=fileName)
        JsonBackInfo = {
            "canLogin": True,
            "AuthName": username
        }

        return JsonResponse(JsonBackInfo)

    elif request.method == 'GET':
        return render(request, 'register.html')


def update(request):
    if request.method == 'POST':
        user = request.user
        username = request.user.username

        faceImage = request.POST.get('faceImg')
        # 提取出base64格式，并进行转换为图片
        index = faceImage.find('base64,')
        base64Str = faceImage[index + 6:]
        img = base64.b64decode(base64Str)
        fileName = 'upload/faces/' + username + '.JPG'
        with open(fileName, 'wb') as f:
            f.write(img)
        Faces.objects.filter(user=user).update(face_img=fileName)
        JsonBackInfo = {
            "canLogin": True,
            "AuthName": username
        }

        return JsonResponse(JsonBackInfo)


def auth_user(img):
    # 人脸登陆验证
    known_people = Faces.objects.all()
    known_face = []
    auth_name = []
    for people in known_people:
        auth_name.append(people.user.username)
        face = face_recognition.load_image_file(people.face_img)
        print(people.face_img)
        face_location = face_recognition.face_locations(face)
        known_face += face_recognition.face_encodings(face, face_location)

    canLogin = False
    AuthName = "未授权用户"


    # 1> 加载相机刚拍摄的人脸
    unknown_face = face_recognition.load_image_file(img)
    locate_unknown_face = face_recognition.face_locations(unknown_face)
    unknown_face_tmp_encoding = []
    try:
        unknown_face_tmp_encoding = face_recognition.face_encodings(unknown_face, locate_unknown_face)[0]
    except IndexError:
        canLogin = False  # 图片中未发现人脸

    # 第二中方法
    results1 = face_recognition.compare_faces(known_face, unknown_face_tmp_encoding, 0.4)
    for i, face_distance in enumerate(results1):
        if face_distance == True:
            canLogin = True
            AuthName = auth_name[i]
            break

    JsonBackInfo = {
        "canLogin": canLogin,
        "AuthName": AuthName
    }

    os.system('rm *.jpg')
    return JsonBackInfo


def loginFaceCheck(request):
    if request.method == "POST" and request.is_ajax():
        # 获取base64格式的图片
        start = time.clock()
        faceImage = request.POST.get('faceImg')
        # 提取出base64格式，并进行转换为图片
        index = faceImage.find('base64,')
        base64Str = faceImage[index+6:]
        img = base64.b64decode(base64Str)

        # 不能直接将传来的图片转为numpy数组，会报错“'utf-8' codec can't decode byte 0x89...”，用python先保存再读取
        imgName = 'temp.jpg'
        with open(imgName, 'wb') as f:
            f.write(img)
        end = time.clock()
        print("img_get_write:", end - start)

        start = time.clock()
        JsonBackInfo = auth_user(imgName)
        end = time.clock()
        print("auth_user_time:", end - start)

        if JsonBackInfo['AuthName'] != "未授权用户":
            user = User.objects.get_by_natural_key(username=JsonBackInfo['AuthName'])  # authenticate(username='admin', password='123456')
            if user is not None:
                if user.is_active:
                    ori_login(request, user)

        return JsonResponse(JsonBackInfo)


@csrf_exempt
def test(request):
    if request.method == "POST":
        startt = time.time()
        start = time.clock()
        videos = request.FILES['faceVideo']
        fileName = 'temp.webm'
        # file = uploadedfile.File(videos)
        with open(fileName, 'wb') as f:
            for chunk in videos.chunks():
                f.write(chunk)
        end = time.clock()
        print("video_get_write:", end - start)

        start = time.time()
        os.system('python3 multiprocess_test.py')
        while len(glob.glob(os.path.join('.', "*.npy"))) == 0:
            pass
        num = int(np.load('temp.npy'))
        end = time.time()
        print("Blink_video_stream:", end - start)

        files = glob.glob(os.path.join('.', "*.jpg"))
        imgName = files[int(len(files) / 2)]
        jsonInfo = auth_user(imgName)
        os.system('rm *.mp4 *.npy')
        JsonBackInfo = {
            "canLogin": jsonInfo['canLogin'],
            "AuthName": jsonInfo['AuthName'],
            'blink_num': num
        }

        if jsonInfo['AuthName'] != "未授权用户" and num == 2:
            user = User.objects.get_by_natural_key(username=jsonInfo['AuthName'])  # authenticate(username='admin', password='123456')
            if user is not None:
                if user.is_active:
                    ori_login(request, user)
        
        print("total_time:", time.time() - startt)
        return JsonResponse(JsonBackInfo)
    else:
        return render(request, 'random-instruction.html')


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

    cap.release()


def translate(infile, outfile):
    ff = ffmpy3.FFmpeg(
        inputs={infile: None},
        outputs={outfile: '-r 25 -y'}
    )
    ff.run()


def piece_state(f, i, d):
    unknown_face = face_recognition.load_image_file(f)
    locate_unknown_face = face_recognition.face_locations(unknown_face)
    landmards = face_recognition.face_landmarks(unknown_face, locate_unknown_face)
    left_eye = landmards[0]['left_eye']
    right_eye = landmards[0]['right_eye']
    left_ear = eye_aspect_ratio(left_eye)
    right_ear = eye_aspect_ratio(right_eye)
    d[i] = (left_ear, right_ear)


def detection_blink():
    num = 0
    left_blink, right_blink = (False, False)
    infile = 'temp.webm'
    outfile = 'temp.mp4'
    translate(infile, outfile)
    video2frame(outfile)
    pool = Pool(processes=4)
    d = Manager().dict()

    files = glob.glob(os.path.join('.', "*.jpg"))
    print('files', files)
    for f, i in zip(files, range(len(files))):
        pool.apply(piece_state, (f, i, d))# _async

    pool.close()
    pool.join()

    print('dict:', d)
    for i in sorted(d):
        left_ear, right_ear = d[i]
        if left_ear < 0.20:
            left_blink = True
        if right_ear < 0.20:
            right_blink = True

        if left_ear >= 0.20 and right_ear >= 0.20 and left_blink and right_blink:
            num += 1
            right_blink = False
            left_blink = False

    return num
