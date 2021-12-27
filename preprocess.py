import tempfile
from PIL import Image
import cv2, os
import numpy as np

IMAGE_SIZE = 1800
BINARY_THREHOLD = 180

def save_image_to_debug(myimage):
    """
    Save image to local debug folder
    :param myimage: File object uploaded to endpoint
    :return: Location on file saved in debug folder
    """
    file_location = f"debug/{myimage.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(myimage.file.read())
        file_object.close()
    return file_location

def process_image_for_ocr(file_location):
    """
    pipeline for all the image processing
    input: image object
    return: cv2 image
    """
    #file_location = save_image_to_debug(myimage)
    file = set_image_dpi(file_location)
    image = remove_noise_and_smooth(file['cv2_image'])
    os.remove(file['temp_file'])
    return image

def set_image_dpi(file_location):
    """
    Upsale image DPI to 300
    :param file_location: Location of file to be upscaled
    :return: 
    """
    im = Image.open(file_location)
    length_x, width_y = im.size
    factor = max(1, int(IMAGE_SIZE / length_x))
    size = factor * length_x, factor * width_y
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    im_resized.close()
    
    image = cv2.imread(temp_filename,0)
    cv2.imwrite("debug/image_300dpi.jpeg", image)
    os.remove(file_location)
    #os.remove(temp_filename)
    return {'temp_file': temp_filename, 'cv2_image': image}

def image_smoothening(img):
    """
    makes the image smooth
    :param img: Input cv2 image
    :result: smoothened cv2 image
    """
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite("debug/smooth.jpeg", th3)
    return th3

def remove_noise_and_smooth(img):
    """
    removes the noise in input image
    :param img: Input cv2 image
    :result: noise removed cv2 image
    """
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 10)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    cv2.imwrite("debug/noise.jpeg", or_image)
    return or_image