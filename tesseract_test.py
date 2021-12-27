import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
print(pytesseract.pytesseract.tesseract_cmd)

def Correct(text):
  
    corrected = text
    for k in Replace:
    #print(k)
        corrected = corrected.replace(k,Replace[k]) 
        print("["+k+"]"+":"+corrected)
        return corrected

path_to_image = "images/Invoice.1.jpg" 
image = cv2.imread(path_to_image)
h, w, _ = image.shape    

def Contrast(image, imageOut, contrast, bright):
    #Change contrast and brightness - might be not necessary, just find appropriate values for the mask
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            for c in range(image.shape[2]):
                imageOut[y,x,c] = np.clip(contrast*image[y,x,c] + bright, 0, 255)
    # cv2.imshow('Contrast-ImageOut', imageOut)
    # cv2.waitKey(0)    

def Partition(image):
    h, w, _ = image.shape  
    cv2.rectangle(image,(0,0),(w,h),255,2)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
    cnts, hier = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cropped = []
    for i, cnt in enumerate(cnts):
        x,y,w,h = cv2.boundingRect(cnt)
        cropped.append(image[y:y+h,x:x+w])
        
Partition(image.copy())     
imageContrast = image.copy()
custom_config = r'--oem 3 --psm 12'  
text = pytesseract.image_to_string(imageContrast, config=custom_config)#, lang="ita")
print(text)
cv2.waitKey(0)
cv2.destroyAllWindows()