from typing import Text
import cv2
import pytesseract
from pytesseract import Output
from collections import namedtuple
from LCS import levenshtein_ratio_and_distance
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"

IMAGE_SIZE = 1800
BINARY_THREHOLD = 180
OCRLocation = namedtuple("OCRLocation", ["id", "bbox", "filter_keywords"])
'''
OCR_LOCATIONS_template4 = [
    OCRLocation("gst", (20, 740, 170, 150),
        ["gstn", "no,", "no"]),
    OCRLocation("address", (20, 460, 170, 120),
        ["net", "amt", "supply"]),
    OCRLocation("address", (20, 580, 170, 120),
        ["net", "amt", "supply"]),
    OCRLocation("phone", (10, 660, 170, 11),
        ["telephone", "phone", "ph", "ph.", "ph,"]),
    OCRLocation("net amt", (10, 226, 170, 16),
        ["net", "amt", "supply"]),
    OCRLocation("full", (0, 0, 1180, 1580), ["net", "amt", "supply"]),
]

# OCR_LOCATIONS_template5 = [
#     OCRLocation("gst", (20, 740, 170, 150),
#         ["gstn", "no,", "no"]),
#     OCRLocation("address", (20, 460, 170, 120),
#         ["net", "amt", "supply"]),
#     OCRLocation("address", (20, 580, 170, 120),
#         ["net", "amt", "supply"]),
#     OCRLocation("phone", (10, 660, 170, 11),
#         ["telephone", "phone", "ph", "ph.", "ph,"]),
#     OCRLocation("net amt", (10, 226, 170, 16),
#         ["net", "amt", "supply"]),
#     OCRLocation("full", (0, 0, 1180, 1580), ["net", "amt", "supply"]),
# ]
'''
#----------------Invoice 10.jpeg---------------------
OCR_LOCATIONS_template10 = [
     OCRLocation("Title", (353, 88, 472, 48),
        ["PRITIKA AUTO INDUSTRIES LTD"]),
    OCRLocation("GSTIN No", (222, 228, 220, 35),
        ["02AAACH4698CIZV"]),
    OCRLocation("GSTIN", (195, 502, 173, 25),
        ["05AAACM3025E1Z5"]),
    #OCRLocation("IRN No", (294, 279, 663, 45),
        #["irn", "no,", "no"]),
    OCRLocation("PAN No", (196, 525, 134, 29),
        ["AAACM3025E"]),
    OCRLocation("Ivoice No", (230, 264, 209, 35),
        ["PAU/21-22/3722"]),
    OCRLocation("Invoice Date", (930, 243, 140, 36),
        ["04-Oct-2021"]),
    OCRLocation("Party Name", (108, 369, 453, 140),
        ["MAHINDRA & MAHINDRA LTD [RUDARPUR]\nFD-RUDRAPUR PLANT, AGRI DEVELOPMENT\nCENTER, VILLAGE & POST OFFICE LALPUR, KICHA\nROAD, UDHAM SING NAGAR-263148\nRUDRAPUR\nUttarakhand-263148"]),
    OCRLocation("Consignee Name", (585, 359, 476, 140),
        ["MAHINDRA & MAHINDRA LTD [RUDARPUR]\nFD-RUDRAPUR PLANT, AGRI DEVELOPMENT\nCENTER, VILLAGE & POST OFFICE LALPUR, KICHA\nROAD, UDHAM SING NAGAR-263148\nRUDRAPUR\nUttarakhand-263148"]),
    OCRLocation("Order No", (203, 562, 210, 27),
        ["6710349368 Dt.19/04/19"]),
    OCRLocation("Rupees", (142, 1307, 408, 36),
        ["Two Lakh Thirty Six Thousand Fifteen Only"]),  
    OCRLocation("Net Amount", (999, 1265, 110, 31),
        ["236015.00"]), 
    #OCRLocation("full", (0, 0, 1180, 1580), ["pan", "gstin_no", "gstin", "irn", "invoice", "invoic_dt", "partyname", "consignename"]),
]

#--------------Invoice 6.jpeg-----------------------
OCR_LOCATIONS_template6 = [
     OCRLocation("title", (357, 90, 299, 30),
        ["Sharda Motor Industries Ltd."]),
    OCRLocation("Phone No", (604, 121, 77, 10),
        ["0253-6687680/681"]),
    OCRLocation("GSTIN", (121, 294, 103, 16),
        ["05AAACM3025E1Z5"]),
    OCRLocation("IRN No", (131, 186, 471, 23),
        ["734e4f8e1d57c3bee31b4eab70b18193006132b2d75baf894a9b771e74e7e4c9"]),
    OCRLocation("Email", (480, 132, 204, 20),
        ["despatchnsk@shardamotor.com"]),
    OCRLocation("Order No", (97, 395, 65, 14),
        ["6710012217"]),
    OCRLocation("Ivoice No", (702, 200, 92, 21),
        ["NT22Y17529"]),
    OCRLocation("Invoice Date", (741, 215, 121, 17),
        ["07-09-21 2:15:36 PM"]),
    OCRLocation("Part No", (169, 393, 83, 14),
        ["0105LAN00080N"]),
    OCRLocation("Bill To", (80, 225, 233, 65),
        ["MAHINDRA & MAHINDRA-HARIDWAR\nPLOT NO,01,03,17,22 AUTO SECTOR-5,IIE SIDCUL\nHARIDWAR\n249401"]),
    OCRLocation("Ship to", (363, 224, 248, 59),
        ["MAHINDRA & MAHINDRA-HARIDWAR\nPLOT NO,01,03,17,22 AUT0 SECTOR-5,IIE SIDCUL\nHARIDWAR\n249401"]),
    OCRLocation("Rupees", (574, 933, 320, 32),
        ["Amount in Words: **** SIX THOUSAND ONE HUNDRED\nEIGHTY FIVE RUPEED AND FORTY SEVEN PAISA ONLY"]),  
    OCRLocation("Net Amount", (857, 897, 45, 18),
        ["6185.47"]), 
    #OCRLocation("full", (0, 0, 1180, 1580), ["pan", "gstin_no", "gstin", "irn", "invoice", "invoic_dt", "partyname", "consignename"]),
]
#--------------Invoice.1.jpg-----------------------
OCR_LOCATIONS_template1 = [
    #  OCRLocation("Title", (353, 88, 472, 43),
    #     ["title", "no,", "no"]),
    # OCRLocation("GSTIN No", (222, 228, 220, 30),
    #     ["gstin_no", "no,", "no"]),
    OCRLocation("GSTIN", (83, 51, 82, 14),
        ["27AAACM3025E1ZZ"]),
    OCRLocation("Place of Supply", (51, 165, 108, 19),
        ["Telangana"]),
    OCRLocation("PAN", (74, 36, 59, 15),
        ["AAACM3025E"]),
    OCRLocation("Code", (230, 167, 33, 26),
        ["PLF023"]),
    OCRLocation("Destination", (452, 170, 47, 12),
        ["Zaheerabad"]),
    # OCRLocation("Invoice Date", (930, 243, 147, 36),
    #     ["invoic_dt", "no,", "no"]),
    OCRLocation("Bill To Party", (49, 77, 162, 68),
        ["billparty"]),
    OCRLocation("Ship To Pary", (277, 80, 164, 64),
        ["shippary"]),
    OCRLocation("Grand Total", (297, 280, 160, 13),
        ["125880.80"]),
    OCRLocation("Total Tax", (95, 304, 231, 12),
        ["NINE TEEN THOUSAND TWO HUNDRED TWO RUPEES EIGHT PAISE ONLY"]),  
    OCRLocation("Geand Total", (102, 316, 317, 14),
        ["ONE LAKH FIVE THOUSEND EIGHT HUNDRED EIGHTY RUPEES NINETY EIGHT PAISE ONLY"]), 
    OCRLocation("Vehicle No", (265, 371, 57, 18),
        ["MH12LT2087s"]),
    OCRLocation("FULL", (0,0,576,715),
    ["FULL"])
    #OCRLocation("full", (0, 0, 1180, 1580), ["pan", "gstin_no", "gstin", "irn", "invoice", "invoic_dt", "partyname", "consignename"]),
]
#-----------------------------------------------

#--------------Invoice.4.jpg-----------------------
OCR_LOCATIONS_template4 = [
     OCRLocation("Title", (201, 5, 130, 15),
        ["MAHINDRA & MAHINDRA LTD."]),
    # OCRLocation("GSTIN No", (222, 228, 220, 30),
    #     ["gstin_no", "no,", "no"]),
    OCRLocation("GSTIN", (79, 71, 81, 14),
        ["27AAACM3025E1ZZ"]),
    OCRLocation("Place of Supply", (111, 185, 38, 17),
        ["Telangana"]),
    OCRLocation("PAN", (61, 57, 61, 14),
        ["AAACM3025E"]),
    OCRLocation("Code", (223, 189, 35, 12),
        ["PLF012"]),
    OCRLocation("Destination", (444, 186, 49, 16),
        ["Zaheerabad"]),
    # OCRLocation("Invoice Date", (930, 243, 147, 36),
    #     ["invoic_dt", "no,", "no"]),
    OCRLocation("Bill To Party", (45, 109, 164, 52),
        ["billparty", "no,", "no"]),
    OCRLocation("Ship To Pary", (269, 109, 158, 50),
        ["shippary", "no,", "no"]),
    OCRLocation("Grand Total", (286, 331, 47, 12),
        ["1729168.13"]),
    OCRLocation("Total Tax", (87, 354, 326, 13),
        ["THREE LAKH SEVEN THOUSEND FIFTY THREE PASE ONLY"]),  
    OCRLocation("Geand Total", (97, 365, 334, 16),
        ["SEVENEEN LAKH TWOENTY HOUSAND ONE HUNDRED SIXTY EIGHT RUPEES THREEN PAISE ONLY"]), 
    OCRLocation("Vehicle No", (258, 422, 57, 14),
        ["MA12LT2087S"]),
    #OCRLocation("full", (0, 0, 1180, 1580), ["pan", "gstin_no", "gstin", "irn", "invoice", "invoic_dt", "partyname", "consignename"]),
]
#--------------Invoice 7.jpeg-----------------------
OCR_LOCATIONS_template7 = [
     OCRLocation("CIN No", (349, 101, 156, 24),
        ["L27100MH1999PLC121285"]),
    # OCRLocation("Phone No", (604, 121, 77, 10),
    #     ["phone_no", "no,", "no"]),
    OCRLocation("GSTIN/UIN", (295, 173, 129, 29),
        ["36AABCM6632JIZD"]),
    OCRLocation("PAN No", (500, 168, 100, 21),
        ["AABCM66321"]),
    OCRLocation("Billed To", (87, 202, 61, 23),
        ["PLF023"]),
    OCRLocation("Name", (88, 230, 173, 61),
        ["MAHINDRA & MAHINDRA LIMITDZaheerabed - Farm Division"]),
    OCRLocation("Address", (85, 287, 175, 51),
        ["NEAR BIDAR T JUNCTION, "]),
    OCRLocation("City", (91, 352, 110, 28),
        ["ZAHEERABAD"]),
    OCRLocation("Shipped To", (370, 207, 55, 24),
        ["PLF023"]),
    OCRLocation("GST Inv. No", (677, 199, 95, 23),
        ["IN2041030238"]),
    OCRLocation("GST Inv. Date", (674, 224, 99, 19),
        ["07.10.2021"]),
    OCRLocation("Customer PO No", (679, 245, 78, 20),
        ["6710562417"]),  
    OCRLocation("Vendor Code", (676, 281, 64, 24),
        ["DM223D"]), 
    OCRLocation("Total Invoice", (752, 648, 68, 26),
        ["48,012.36"]),
    OCRLocation("CGST in Words", (125, 690, 444, 19),
        ["Five Thousand two Hundred Fifty One and Thirty Five Paise Only"]),
    OCRLocation("Invoice Total in Words", (171, 729, 468, 24),
        ["Forty Thousand tweve Rupees and Thirty Six Paisa Only"]),
    OCRLocation("Gross Weight", (542, 751, 60, 25),
        ["240.120"]),
    OCRLocation("Net Weight", (732, 742, 41, 24),
        ["240.120"]),
    #OCRLocation("full", (0, 0, 1180, 1580), ["pan", "gstin_no", "gstin", "irn", "invoice", "invoic_dt", "partyname", "consignename"]),
]
#---------------Invoice 11.jpeg----------------------
OCR_LOCATIONS_template11 = [
     OCRLocation("Title", (307, 65, 460, 37),
        ["GAINMAX FERROCAST PVT.LTD."]),
    OCRLocation("GSTIN", (485, 214, 230, 30),
        ["gstin", "no,", "no"]),
    #OCRLocation("IRN No", (294, 279, 663, 45),
        #["irn", "no,", "no"]),
    # OCRLocation("PAN No", (196, 525, 134, 27),
    #     ["pan", "no,", "no"]),
    OCRLocation("Ivoice No", (876, 209, 55, 20),
        ["4826"]),
    OCRLocation("Invoice Date", (828, 232, 99, 23),
        ["05/10/2021"]),
    OCRLocation("Address", (396, 269, 268, 109),
        ["address", "no,", "no"]),
    OCRLocation("HSN Code", (845, 451, 80, 22),
        ["84835090"]), 
    OCRLocation("Grand Total", (957, 1208, 85, 27),
        ["13,073.00"]), 
    #OCRLocation("full", (0, 0, 1180, 1580), ["pan", "gstin_no", "gstin", "irn", "invoice", "invoic_dt", "partyname", "consignename"]),
]
#--------------Invoice 12.jpeg------------------------
OCR_LOCATIONS_template12 = [
     OCRLocation("Address", (77, 236, 406, 157),
        ["address", "no,", "no"]),
    OCRLocation("Consignee", (76, 402, 368, 121),
        ["consignee", "no,", "no"]),
    #OCRLocation("IRN No", (294, 279, 663, 45),
        #["irn", "no,", "no"]),
    # OCRLocation("PAN No", (196, 525, 134, 27),
    #     ["pan", "no,", "no"]),
    OCRLocation("Buyer(Bill)", (72, 535, 392, 123),
        ["buyer", "no,", "no"]),
    OCRLocation("Invoice No", (661, 220, 198, 26),
        ["invoic_no", "no,", "no"]),
    #OCRLocation("full", (0, 0, 1180, 1580), ["pan", "gstin_no", "gstin", "irn", "invoice", "invoic_dt", "partyname", "consignename"]),
]
#----------------Invoice.3.jpg----------------------
OCR_LOCATIONS_template3 = [
     OCRLocation("Title", (216, 11, 20, 13),
        ["MAHINDRA & MAHINDRA LTD."]),
    # OCRLocation("GSTIN No", (222, 228, 220, 30),
    #     ["gstin_no", "no,", "no"]),
    OCRLocation("GSTIN", (93, 71, 76, 13),
        ["27AAACM3025E1ZZ"]),
    OCRLocation("Place of Supply", (121, 183, 43, 16    ),
        ["telangana"]),
    OCRLocation("PAN", (319, 188, 72, 14),
        ["AAACM3025E"]),
    OCRLocation("Code", (235, 185, 30, 18),
        ["PLFO23"]),
    OCRLocation("Destination", (451, 185, 51, 18),
        ["Zaheerabed"]),
    # OCRLocation("Invoice Date", (930, 243, 147, 36),
    #     ["invoic_dt", "no,", "no"]),
    OCRLocation("Bill To Party", (61, 109, 166, 58),
        ["billparty", "no,", "no"]),
    OCRLocation("Ship To Pary", (276, 109, 165, 56),
        ["shippary", "no,", "no"]),
    OCRLocation("Grand Total", (300, 297, 37, 12),
        ["97411.84"]),
    OCRLocation("Total Tax", (99, 319, 271, 14),
        ["TWENTY ONE THOUSEND THREE HUNDRED EIGHT RUPEES EIGHTY PAISA ONLY"]),  
    OCRLocation("Geand Total", (107, 329, 277, 17),
        ["NINETY SEVEN THOUSAND FOUR HUNDRED ELEVEN RUPEES FOUR PAISA ONLY"]), 
    OCRLocation("Vehicle No", (752, 648, 68, 26),
        ["MA12LT2087S"]),
    #OCRLocation("full", (0, 0, 1180, 1580), ["pan", "gstin_no", "gstin", "irn", "invoice", "invoic_dt", "partyname", "consignename"]),
]

#-----------------Invoice 10--------------------------
OCR_LOCATIONS_template0 = [
    OCRLocation("name", (490, 330, 672, 165), 
        ["SHREE RAM PALACE"]),
    OCRLocation("gst", (700, 762, 700, 90), 
        ["07AAJPG1725F2Z1"]),
    OCRLocation("address line 1", (20, 500, 1700, 88),
        ["SHOP NO. 7, LSC MKT., SHEIKH SARAI-II,"]),
    OCRLocation("address line 2", (475, 580, 800, 90),
        ["NEW DELHI-110017"]),
    OCRLocation("phone", (450, 660, 800, 110),
        ["29250303, 29250304, 29251709"]),
    OCRLocation("net amt", (500, 2260, 1700, 300),
        ["95.00"]),
    #OCRLocation("whole", (0, 0, 1850, 2860), ["net", "amt", "supply"]),
]

template_locations = {"0":OCR_LOCATIONS_template0, "1":OCR_LOCATIONS_template1, "3":OCR_LOCATIONS_template3, "4":OCR_LOCATIONS_template4, "6":OCR_LOCATIONS_template6, "7":OCR_LOCATIONS_template7, "10": OCR_LOCATIONS_template10, "11":OCR_LOCATIONS_template11, "12":OCR_LOCATIONS_template12}

def cleanup_text(text) -> str:
    """
    strip out non-ASCII text so we can draw the text on the image
    :param text: original text
    :return: stripped text
    """
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()

def inference(img, boxes=False, show=False):
    custom_config = r'--oem 3 --psm 3' 
    #custom_config = r'--psm 3 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvw0123456789'       
    if boxes:
        result = pytesseract.image_to_data(img, output_type=Output.DICT, config=custom_config)
        n_boxes = len(result['level'])
        for i in range(n_boxes):
            (x, y, w, h) = (result['left'][i], result['top'][i], result['width'][i], result['height'][i])
            #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, result['text'][i], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        if show:
            print(n_boxes)
            #cv2.imshow('img', OCRLocation("GSTIN No", (222, 228, 220, 30),
        #["gstin", "no,", "no"]),"lt":result}

def inference2(image, template_no):
    OCR_LOCATIONS = template_locations[template_no]
    parsingResults = []
    results = {}
    results_with_confidence = {}
    for loc in OCR_LOCATIONS:
        (x, y, w, h) = loc.bbox
        roi = image[y:y + h, x:x + w]
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # OCR the ROI using Tesseract
        #cv2.imshow("roi", roi)
        #cv2.waitKey(1000)
        rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        image_ee = cv2.copyMakeBorder(rgb, 200, 200, 200, 200, cv2.BORDER_CONSTANT, value=[255,255,255])
        #cv2.imshow("test{}".format(x), image_ee)
        custom_config = r'--oem 3 --psm 3'
        text = pytesseract.image_to_string(image_ee, config=custom_config)
        #print("pytessact", text) 
        for line in text.split("\n"):
            # if the line is empty, ignore it
                if len(line) == 0:
                    continue
                lower = line.lower()
                count = sum([lower.count(x) for x in loc.filter_keywords])
                #print(count, lower)
                if count >= 0:
                    parsingResults.append((loc, line))
        # OCR the ROI using Tesseract
        rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        custom_config = r'--oem 3 --psm 3'
        text = pytesseract.image_to_string(rgb, config=custom_config)
        text = cleanup_text(text.strip())
        for i in loc.filter_keywords:
            #print(LCSubStr(i, text, len(i), len(text)))
            #print(i, text)
            if len(text)>0:
                print(levenshtein_ratio_and_distance(i.upper(),text.strip().upper(), ratio_calc=True))
                results_with_confidence[loc.id]={"original":i.upper(), "generated":text.strip().upper(), "accuracy":str(round(levenshtein_ratio_and_distance(i.upper(),text.strip().upper(), ratio_calc=True),2)*100)+"%"}
            #else:
                #results_with_confidence[loc.id]={"original":i.upper(), "generated":"", "accuracy":"0%"}
    #print(results) 
    for (loc, line) in parsingResults:
        # grab any existing OCR result for the current ID of the document
        r = results.get(loc.id, None)
        # if the result is None, initialize it using the text and location
        # namedtuple (converting it to a dictionary as namedtuples are not
        # hashable)
        if r is None:
            results[loc.id] = (line, loc._asdict())
        # otherwise, there exists an OCR result for the current area of the
        # document, so we should append our existing line
        else:
            # unpack the existing OCR result and append the line to the
            # existing text
            (existingText, loc) = r
            text = "{}\n{}".format(existingText, line)
            # update our results dictionary
            results[loc["id"]] = (text, loc)
    for (locID, result) in results.items():
        # unpack the result tuple
        (text, loc) = result
        # display the OCR result to our terminal
        print(loc["id"])
        print("=" * len(loc["id"]))
        print("{}\n\n".format(text))
        # extract the bounding box coordinates of the OCR location and
        # then strip out non-ASCII text so we can draw the text on the
        # output image using OpenCV
        (x, y, w, h) = loc["bbox"]
        clean = cleanup_text(text)
        # draw a bounding box around the text
        #image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # loop over all lines in the text
        for (i, line) in enumerate(text.split("\n")):
            # draw the line on the output image
            startY = y + (i * 70) + 40
            #cv2.putText(image, line, (x-10, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    return {"image": image, "result":results_with_confidence}


def debug_invoice(image, template_no):
    OCR_LOCATIONS = template_locations[template_no]
    parsingResults = []
    results = {}
    results_with_confidence = {}
    for loc in OCR_LOCATIONS:
        (x, y, w, h) = loc.bbox
        roi = image[y:y + h, x:x + w]
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, loc.id, (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # OCR the ROI using Tesseract
        #cv2.imshow("roi", roi)
        #cv2.waitKey(1000)
        rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        image_ee = cv2.copyMakeBorder(rgb, 200, 200, 200, 200, cv2.BORDER_CONSTANT, value=[255,255,255])
        #cv2.imshow("test{}".format(x), image_ee)
        custom_config = r'--oem 3 --psm 3'
        text = pytesseract.image_to_string(image_ee, config=custom_config)
        #print("pytessact", text) 
        for line in text.split("\n"):
            # if the line is empty, ignore it
                if len(line) == 0:
                    continue
                lower = line.lower()
                count = sum([lower.count(x) for x in loc.filter_keywords])
                #print(count, lower)
                if count >= 0:
                    parsingResults.append((loc, line))
        # OCR the ROI using Tesseract
        rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        custom_config = r'--oem 3 --psm 3'
        text = pytesseract.image_to_string(rgb, config=custom_config)

        for i in loc.filter_keywords:
            #print(LCSubStr(i, text, len(i), len(text)))
            print("\ntitle:", loc.id, "\nOriginal:",i, "\nGenerated:",cleanup_text(text.strip()))
            if len(cleanup_text(text.strip()))>0:
                print(len(cleanup_text(text.strip())))
                print(levenshtein_ratio_and_distance(i,cleanup_text(text.strip()), ratio_calc=True))
            #results_with_confidence[loc.id]={"original":i, "generated":text.strip(), "accuracy":str(round(levenshtein_ratio_and_distance(i,text.strip(), ratio_calc=True),2)*100)+"%"}
    #print(results) 
    for (loc, line) in parsingResults:
        # grab any existing OCR result for the current ID of the document
        r = results.get(loc.id, None)
        # if the result is None, initialize it using the text and location
        # namedtuple (converting it to a dictionary as namedtuples are not
        # hashable)
        if r is None:
            results[loc.id] = (line, loc._asdict())
        # otherwise, there exists an OCR result for the current area of the
        # document, so we should append our existing line
        else:
            # unpack the existing OCR result and append the line to the
            # existing text
            (existingText, loc) = r
            text = "{}\n{}".format(existingText, line)
            # update our results dictionary
            results[loc["id"]] = (text, loc)
    for (locID, result) in results.items():
        # unpack the result tuple
        (text, loc) = result
        # display the OCR result to our terminal
        print(loc["id"])
        print("=" * len(loc["id"]))
        print("{}\n\n".format(text))
        # extract the bounding box coordinates of the OCR location and
        # then strip out non-ASCII text so we can draw the text on the
        # output image using OpenCV
        (x, y, w, h) = loc["bbox"]
        clean = cleanup_text(text)
        # draw a bounding box around the text
        #image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # loop over all lines in the text
        for (i, line) in enumerate(text.split("\n")):
            # draw the line on the output image
            startY = y + (i * 70) + 40
            #cv2.putText(image, line, (x-10, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    return {"image": image, "result":results_with_confidence}

def test_invoice(image):
    #OCR_LOCATIONS = template_locations[template_no]
    parsingResults = []
    results = {}
    results_with_confidence = {}
    custom_config = r'--oem 3 --psm 3'
    text = pytesseract.image_to_string(image, config=custom_config)
    clean = cleanup_text(text)
    return {"image": image, "result":clean}
    """
    for loc in OCR_LOCATIONS:
        (x, y, w, h) = loc.bbox
        roi = image[y:y + h, x:x + w]
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # OCR the ROI using Tesseract
        #cv2.imshow("roi", roi)
        #cv2.waitKey(1000)
        rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        image_ee = cv2.copyMakeBorder(rgb, 200, 200, 200, 200, cv2.BORDER_CONSTANT, value=[255,255,255])
        #cv2.imshow("test{}".format(x), image_ee)
        custom_config = r'--oem 3 --psm 3'
        text = pytesseract.image_to_string(image_ee, config=custom_config)
        #print("pytessact", text) 
        for line in text.split("\n"):
            # if the line is empty, ignore it
                if len(line) == 0:
                    continue
                lower = line.lower()
                count = sum([lower.count(x) for x in loc.filter_keywords])
                #print(count, lower)
                if count >= 0:
                    parsingResults.append((loc, line))
        # OCR the ROI using Tesseract
        rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        custom_config = r'--oem 3 --psm 3'
        text = pytesseract.image_to_string(rgb, config=custom_config)
        text = cleanup_text(text.strip())
        for i in loc.filter_keywords:
            #print(LCSubStr(i, text, len(i), len(text)))
            #print(i, text)
            if len(text)>0:
                print(levenshtein_ratio_and_distance(i.upper(),text.strip().upper(), ratio_calc=True))
                results_with_confidence[loc.id]={"original":i.upper(), "generated":text.strip().upper(), "accuracy":str(round(levenshtein_ratio_and_distance(i.upper(),text.strip().upper(), ratio_calc=True),2)*100)+"%"}
            #else:
                #results_with_confidence[loc.id]={"original":i.upper(), "generated":"", "accuracy":"0%"}
    #print(results) 
    for (loc, line) in parsingResults:
        # grab any existing OCR result for the current ID of the document
        r = results.get(loc.id, None)
        # if the result is None, initialize it using the text and location
        # namedtuple (converting it to a dictionary as namedtuples are not
        # hashable)
        if r is None:
            results[loc.id] = (line, loc._asdict())
        # otherwise, there exists an OCR result for the current area of the
        # document, so we should append our existing line
        else:
            # unpack the existing OCR result and append the line to the
            # existing text
            (existingText, loc) = r
            text = "{}\n{}".format(existingText, line)
            # update our results dictionary
            results[loc["id"]] = (text, loc)
    for (locID, result) in results.items():
        # unpack the result tuple
        (text, loc) = result
        # display the OCR result to our terminal
        print(loc["id"])
        print("=" * len(loc["id"]))
        print("{}\n\n".format(text))
        # extract the bounding box coordinates of the OCR location and
        # then strip out non-ASCII text so we can draw the text on the
        # output image using OpenCV
        (x, y, w, h) = loc["bbox"]
        clean = cleanup_text(text)
        # draw a bounding box around the text
        #image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # loop over all lines in the text
        for (i, line) in enumerate(text.split("\n")):
            # draw the line on the output image
            startY = y + (i * 70) + 40
            #cv2.putText(image, line, (x-10, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    return {"image": image, "result":results_with_confidence}
    """
if __name__ == '__main__':
    print(template_locations["0"])
