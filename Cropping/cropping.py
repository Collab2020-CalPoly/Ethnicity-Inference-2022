# Imports for CSV, OpenCV, Requests (for downloading urls), and Clarifai
import csv
import cv2
import requests
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2

stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

# Personal access tokens. Can be changed if needed, directly from Clarifai website.
YOUR_CLARIFAI_API_KEY = "2abc34d6ab30456aaeef1968b5866360"
# Name of your application goes here
YOUR_APPLICATION_ID = "detect_face"

# Important columns in CSV file
IMAGE_ADDRESS_COL = 8
FIRST_NAME_COL = 0
LAST_NAME_COL = 1

# Do not change
metadata = (("authorization", f"Key {YOUR_CLARIFAI_API_KEY}"),)

"""
Ensures that there is a URL and that it is not a default avatar.
"""
def check_valid_url(inp):
    if (inp is not None) and ("N\A" not in inp) and ("avatar" not in inp) and ("placeholder" not in inp):
        return True
    return False

"""
Downloads an online image to a given local destination
"""
def url_to_image(url, dst):
    response = requests.get(url)
    fp = open(dst, 'wb')
    fp.write(response.content)
    fp.close()

"""
Given an input image, function uses Clarifai API provided model "face-detection" to 
detect a face and generate a bounding box around the face. Outputs the bounding_box data.
The output dimensions could be accessed through .top_row, .bottom_row, left_col, .right_col
*NOTE: this function takes a local image as an argument, not a url
"""
def detect_face(image):
    with open(image, "rb") as f:
        file_bytes = f.read()
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            # Change model_id here, if needed
            model_id="face-detection",
            user_app_id=resources_pb2.UserAppIDSet(app_id=YOUR_APPLICATION_ID),
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(image=resources_pb2.Image(base64=file_bytes))
                )
            ],
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response)
        raise Exception(f"Request failed, status code: {post_model_outputs_response.status}")

    out = post_model_outputs_response.outputs[0]
    return out.data.regions[0].region_info.bounding_box

"""
Given an input image, function converts the image to an OpenCV object.
Crops this image to be just the human face. 
*NOTE: this function takes a local image as an argument, not a url
"""
def crop_face(image):
    img = cv2.imread(image)
    ROWS = img.shape[0]
    COLS = img.shape[1]

    bounding_box = detect_face(image)
    top = int(bounding_box.top_row * ROWS) 
    bottom = int(bounding_box.bottom_row * ROWS)
    left = int(bounding_box.left_col * COLS)
    right = int(bounding_box.right_col * COLS)

    crop = img[top:bottom, left:right] 
    # cv2.imshow('cropped', crop)    
    # use esc key to exit
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite(image, crop)

"""
Reads a csv file and attempts to download the image url from each row
"""
def process_csv(csv_reader):
    # outp = []

    # header = ['First Name', 'Last Name', 'White', 'Black', 'Asian', 'Other', 'Highest Prob. Score']
    # f = open('69_Cropped_Inferences.csv', 'w+', encoding='UTF8', newline='')

    # writer = csv.writer(f)
    # writer.writerow(header)

    for row in csv_reader:
        try:
            IMAGE_URL = row[IMAGE_ADDRESS_COL]
            if check_valid_url(IMAGE_URL):
                # Change the destination of the cropped images here
                image_dst = "./Cropping/Automated Cropped Faculty Images/{first_name}_{last_name}.jpg".format(first_name=row[FIRST_NAME_COL], last_name=row[LAST_NAME_COL])
                url_to_image(IMAGE_URL, image_dst)
                crop_face(image_dst)
        except Exception as e:
            print("{first_name} {last_name}: invalid image url: {url}".format(first_name=row[FIRST_NAME_COL], last_name=row[LAST_NAME_COL], url=row[IMAGE_ADDRESS_COL]))

def main():
    """
    Need To Do:
    1) check the 50 pixel by 50 pixel quality 
    2) what to do with these invalid url 
    3) do I need to append these new local images to the csv, 
    so that they can be used in face_recognition.py
    4) if an exception occurs a .jpg file is still is generated (in some cases)
    """
    file = open('./Cropping/69_Good_Quality_Photos.csv')
    reader = csv.reader(file)
    next(reader)
    process_csv(reader)

if __name__ == "__main__":
    main()
