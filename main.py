import re
from fastapi import FastAPI, File, UploadFile, Response
from ocr import *
from pipeline import ocr_pipeline, ocr_pipeline_debug, ocr_pipeline_test
app = FastAPI(title="Mahindra and Mahindra OCR POC", 
                version="0.0.1",
                contact={
                    "name": "Assert SecureTech",
                    "url": "https://assertai.com/",
                    "email": "harshit@assertsecuretech.com",
                },)


@app.get("/")
def test_endpoint():
    return {"Hello": "World"}


@app.post("/invoice")
def get_accuracy_of_results(response: Response, file: UploadFile = File(...),  template: str = "0"):
    response_full = ocr_pipeline(file, template)
    response = response_full['result']
    print(response_full['result'])
    return response

@app.post("/debug")
def debug_input_image(response: Response, file: UploadFile = File(...),  template: str = "0"):
    response_full = ocr_pipeline_debug(file, template)
    response = response_full['image']
    print(response_full['result'])
    return response

@app.post("/ocr_text")
def get_text_from_image(file: UploadFile = File(...)):
    response_full = ocr_pipeline_test(file)
    response = response_full['result']
    #print(response_full['result'])
    return response

if __name__ == "__main__":
    pass