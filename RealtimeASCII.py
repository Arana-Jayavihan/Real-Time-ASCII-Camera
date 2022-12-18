import cv2
import numpy as np
from PIL import Image
import keyboard as kb
from PIL import ImageFont
from cv2 import VideoWriter
from cv2 import VideoWriter_fourcc
from datetime import datetime


def genAsciiText(image):
    resizedImg = image.resize((new_width, new_height)).convert("L")
    asciiData = "".join([ascii_chars[pixel//22] for pixel in resizedImg.getdata()])
    AsciiFrameText = "\n".join([asciiData[index:(index+new_width)] for index in range(0, len(asciiData), new_width)])
    return AsciiFrameText

def StringToImg(string):
    font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
    color = fontFill
    thickness, orgY, snum = 0, 0, 0
    
    img = np.zeros([new_height*pixelSize, new_width*pixelSize,3], dtype=np.uint8)
    img.fill(backFill)
    
    for i in range(0, len(string), new_width+1):
        line = string[snum:i]
        orgX = 0
        for j in line:
            org = (orgX, orgY)
            image = cv2.putText(img, j, org, font, fontscale, color, thickness, cv2.FILLED)
            orgX += pixelSize
            
        orgY += pixelSize
        snum = i
    
    return image

print("""
***************************************************************************
[+] Optimal Frame width will be in range 170 and 240.
[+] Anything highrer will reduce FPS and anything lower will not work.
[+] Use p, o to increase and decrease frame size
[+] Use f, d to increase and decrease font size
[+] Press b to switch to between dark and light modes
[+] Press r to reset to default values
[+] Press c to take photo
[+] Press v to start and stop recording
[+] Press q to exit.
[+] ENJOY!!!
***************************************************************************\n""")


rec = False
pixelSize = 5
fontscale = 0.2
fontFill = (0,0,0)
backFill = 255
dark = False

new_width = int(input("[+] Enter Frame Width : "))
while new_width< 170:
    print("[+] INVALID FRAME WIDTH, please enter a valid width :(")
    new_width = int(input("[+] Enter Frame Width : "))
    
aspectR  = 9/16
new_height= int(aspectR *new_width)

video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, new_width)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, new_height)
 
ascii_chars = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."," "]
    
while True:
    now = datetime.now()
    ctime = now.strftime("%H_%M_%S_%f")
    ret, frame = video.read()
    if ret:
        image = StringToImg(genAsciiText(Image.fromarray(cv2.flip(frame, 1))))
        cv2.imshow("ASCII", image)
        cv2.imshow("REAL", cv2.resize(cv2.flip(frame, 1), (480, 360)))
    
        if kb.is_pressed("q"):
            print("[+] Exiting...:3")
            break
        
        elif kb.is_pressed("c"):
            print("[+] Photo Captured ;)")
            cv2.imwrite("ASCII_PHOTO_"+str(ctime)+".jpg", image)

        elif kb.is_pressed("v"):
            if rec == False:
                print("[+] Recording Started :)")
                rec = True
                videoSave = VideoWriter("ASCII_Video_"+str(ctime)+".avi", VideoWriter_fourcc(*'MP42'), 20.0, (new_width*pixelSize, new_height*pixelSize))
                
            elif rec == True:
                rec = False
                print("[+] Recording Saved :)")
                videoSave.release()
                
        elif kb.is_pressed("p"):
            maxPS = 10
            pixelSize += 1
            if pixelSize >= maxPS:
                pixelSize = maxPS

        elif kb.is_pressed("o"):
            minPS = 1
            pixelSize -= 1
            if pixelSize <= minPS:
                pixelSize = minPS
                
        elif kb.is_pressed("f"):
            maxFS = 1
            fontscale += 0.1
            if fontscale >= maxFS:
                fontscale = maxFS

        elif kb.is_pressed("d"):
            minFS = 0.1
            fontscale -= 0.1
            if fontscale <= minFS:
                fontscale = minFS

        elif kb.is_pressed("r"):
            pixelSize = 5
            fontscale = 0.2

        elif kb.is_pressed("b"):
            if dark == False:
                dark = True
                backFill = 0
                fontFill = (255, 255, 255)
                ascii_chars = ascii_chars[::-1]

            elif dark == True:
                dark = False
                backFill = 255
                fontFill = (0, 0, 0)
                ascii_chars = ascii_chars[::-1]
                
        if rec:
            videoSave.write(image)  
        
        if cv2.waitKey(1):
            continue
                
video.release()
cv2.destroyAllWindows()
