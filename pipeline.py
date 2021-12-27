from preprocess import process_image_for_ocr, save_image_to_debug
from align import align_image
import cv2
import os
import io
from fastapi.responses import StreamingResponse
from ocr import *
'''
template = {"0": "templates/original3.jpeg", "1": "templates/original4.jpeg", "2": "templates/Invoice 6.jpeg", "4": "templates/Invoice.1.jpg", "5": "templates/Invoice.4.jpg", "6": "templates/Invoice 7.jpeg", "7": "templates/Invoice 11.jpeg", "8": "templates/Invoice 12.jpeg", "9": "templates/Invoice.3.jpg"}'''
template = {"0": "templates/original.jpeg", "1": "templates/Invoice.1.jpg", "2":"templates/original2.jpeg", "3":"templates/Invoice.3.jpg", "4":"templates/Invoice.4.jpg", "6":"templates/Invoice 6.jpeg", "7": "templates/Invoice 7.jpeg", "8": "templates/Invoice 8.jpeg", "9":"templates/Invoice 9.jpeg","10":"templates/Invoice 10.jpeg", "11": "templates/Invoice 11.jpeg", "12": "templates/Invoice 12.jpeg"}
def ocr_pipeline(myimage, template_no):
    
    file_location = save_image_to_debug(myimage)
    image = cv2.imread(file_location)
    template_image = cv2.imread(template[template_no])
    aligned = align_image(image, template_image, debug=False)
    cv2.imwrite("debug/aligned.jpeg", aligned)
    processed = process_image_for_ocr("debug/aligned.jpeg")
    cv2.imwrite("debug/processed.jpeg", processed)
    os.remove(file_location)

    response =  inference2(processed, template_no) 
    #response =  inference(processed, boxes=True, show=False)  
    _, im_png = cv2.imencode(".png", response['image'])
    return {"image": StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png"), "result":response['result']}

    #return processed
def ocr_pipeline_debug(myimage, template_no):
    
    file_location = save_image_to_debug(myimage)
    image = cv2.imread(file_location)
    template_image = cv2.imread(template[template_no])
    aligned = align_image(image, template_image, debug=False)
    cv2.imwrite("debug/aligned.jpeg", aligned)
    processed = process_image_for_ocr("debug/aligned.jpeg")
    cv2.imwrite("debug/processed.jpeg", processed)
    os.remove(file_location)

    response =  debug_invoice(processed, template_no) 
    #response =  inference(processed, boxes=True, show=False)  
    _, im_png = cv2.imencode(".png", response['image'])
    return {"image": StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png"), "result":response['result']}

def ocr_pipeline_test(myimage):
    
    file_location = save_image_to_debug(myimage)
    image = cv2.imread(file_location)
    #template_image = cv2.imread(template[template_no])
    #aligned = align_image(image, template_image, debug=False)
    #cv2.imwrite("debug/aligned.jpeg", aligned)
    #processed = process_image_for_ocr("debug/aligned.jpeg")
    #cv2.imwrite("debug/processed.jpeg", processed)
    os.remove(file_location)

    response =  test_invoice(image) 
    #response =  test_invoice(processed, template_no) 
    #response =  inference(processed, boxes=True, show=False)  
    _, im_png = cv2.imencode(".png", response['image'])
    return {"image": StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png"), "result":response['result']}
