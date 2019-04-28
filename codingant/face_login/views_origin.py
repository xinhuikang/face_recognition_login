from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import base64
from django.contrib.auth import authenticate
from django.contrib.auth import login as ori_login
import face_recognition
from .models import Faces
from django.contrib.auth.models import User
import math
from django.shortcuts import render, redirect


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


def loginFaceCheck(request):
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


    if request.method == "POST" and request.is_ajax():
        # 获取base64格式的图片
        faceImage = request.POST.get('faceImg')
        # 提取出base64格式，并进行转换为图片
        index = faceImage.find('base64,')
        base64Str = faceImage[index+6:]
        img = base64.b64decode(base64Str)
        # # 将文件保存
        # backupDate = time.strftime("%Y%m%d_%H%M%S")
        # if int(request.POST.get('id')) == 0 :
        #     fileName = BASE_LOGIN_LEFT_PATH +"LeftImg_%s.jpg" % (backupDate)
        # else:
        #     fileName = BASE_LOGIN_RIGHT_PATH + "RightImg_%s.jpg" % (backupDate)
        # fileName = BASE_LOGIN_LEFT_PATH + "LeftImg_%s.jpg" % (backupDate)

    #     # 删除多余的图片
    #     filesLeft = os.listdir(BASE_LOGIN_LEFT_PATH)
    #     filesLeft.sort()
    #     leftImgCount = filesLeft.__len__()
    #     # filesRight = os.listdir(BASE_LOGIN_RIGHT_PATH)
    #     # filesRight.sort()
    #     # RightImgCount = filesRight.__len__()
    #
    #     if leftImgCount > 100:
    #         # 图片超过100个，删除一个
    #         os.unlink(BASE_LOGIN_LEFT_PATH +filesLeft[0])
    #     # if RightImgCount > 100:
    #     #     # 图片超过100个，删除一个
    #     #     os.unlink(BASE_LOGIN_RIGHT_PATH + filesRight[0])

        # 对图片进行人脸识别比对
        canLogin = False
        AuthName = "未授权用户"

        # 不能直接将传来的图片转为numpy数组，会报错“'utf-8' codec can't decode byte 0x89...”，用python先保存再读取
        fileName = 'temp.jpg'
        with open(fileName, 'wb') as f:
            f.write(img)

        # 1> 加载相机刚拍摄的人脸
        unknown_face = face_recognition.load_image_file("temp.jpg")
        locate_unknown_face = face_recognition.face_locations(unknown_face)
        landmards = face_recognition.face_landmarks(unknown_face, locate_unknown_face)
        print('left:', landmards[0]['left_eye'])
        print('right:', landmards[0]['right_eye'])
        left_eye = landmards[0]['left_eye']
        right_eye = landmards[0]['right_eye']
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        if left_ear > 0.18:
            print("left eye opened:", left_ear)
        else:
            print('left eye closed:', left_ear)
        if right_ear > 0.18:
            print("right eye opened:", right_ear)
        else:
            print("right eye closed:", right_ear)
        unknown_face_tmp_encoding = []
        try:
            unknown_face_tmp_encoding = face_recognition.face_encodings(unknown_face, locate_unknown_face)[0]
        except IndexError:
            canLogin = False  # 图片中未发现人脸

        # 2> 进行比对

        ### 第一种方法
        # results = face_recognition.face_distance(known_face,unknown_face_tmp_encoding)
        # 小于0.6即对比成功。但是效果不好，因此我们设置阈值为0.4,
        # for i, face_distance in enumerate(results):
        #     if face_distance <= 0.4:
        #         canLogin = True
        #         AuthName = os.listdir(BASE_LOGIN_AUTH_PATH)[i][:-4]

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

        if AuthName != "未授权用户":
            user = User.objects.get_by_natural_key(username=AuthName)  # authenticate(username='admin', password='123456')
            if user is not None:
                if user.is_active:
                    ori_login(request, user)

        return JsonResponse(JsonBackInfo)


def test(request):
    canLogin = False
    AuthName = "未授权用户"

    if request.method == "POST" and request.is_ajax():
        video = request.POST.get('faceVideo')
        fileName = 'temp.webm'
        with open(fileName, 'wb') as f:
            f.write(video)
        JsonBackInfo = {
            "canLogin": canLogin,
            "AuthName": AuthName
        }

        if AuthName != "未授权用户":
            user = User.objects.get_by_natural_key(username=AuthName)  # authenticate(username='admin', password='123456')
            if user is not None:
                if user.is_active:
                    ori_login(request, user)

        return JsonResponse(JsonBackInfo)
    else:
        return render(request, 'test.html')
