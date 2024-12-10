import os
import cv2
import torch
from PIL import Image
from torchvision import transforms

def extractFrames(videoPath, n=10):
    """
    Extracts frames from a video.

    Args:
        videoPath(str): path to uploaded video
        n(int, optional): number of frames to skip between each extraction

    Returns:
        [list(str)]: list containing paths to all extracted frames in a sequential order 
    """
    video = cv2.VideoCapture(videoPath)
    success, frame = video.read()
    frames = []
    count = 0

    while success:
        video.set(cv2.CAP_PROP_POS_FRAMES, count)

        framePath = os.path.join('uploads', 'frames', f"frame_{count}.jpg")
        cv2.imwrite(framePath, frame)
        frames.append(framePath)
        success, frame = video.read()
        
        count += n

    return frames

def detectFaces(imgPath):
    """
    Detects faces in an image and saves them in respective folder

    Args:
        imgPath : path to the image to detect faces from

    Returns:
        [list(str)] : list of paths to extracted faces  
    """
    img = cv2.imread(imgPath)
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

    facesDetected = face_cascade.detectMultiScale(grayImg, scaleFactor=1.1, minNeighbors=3, minSize=(30,30))
    
    faces = []
    count = 0

    for (x, y, w, h) in facesDetected:
        faceToSave = img[y: y+h, x: x+w]
        path = os.path.join('uploads', 'faces', f"face_{count}.jpg") 
        cv2.imwrite(path, faceToSave)
        faces.append(path)

    return faces

def convertToTensor(face):
    """
    Converts images into VGG11 acceptable format

    Args:
        face(str): path to extracted image that needs to be transformed
    
    Returns:
        [torch.tensor]: input batch for model 
    """
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=0.5, std=0.5)
    ])

    img = Image.open(face).convert('RGB')
    img = transform(img)
    img = img.unsqueeze(0)

    return img

def videoPreprocessingPipeline(videoPath):
    frames = extractFrames(videoPath)
    print(frames)
    faces = [detectFaces(frame) for frame in frames]
    print(faces)
    imgTensors = [convertToTensor(face) for face in faces]
    print(imgTensors)
    input_batch = torch.cat(imgTensors)    

    return input_batch