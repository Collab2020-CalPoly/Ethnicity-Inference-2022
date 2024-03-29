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
YOUR_CLARIFAI_API_KEY = "cfcf6f25b806467993c20b575fb043d1"
# Name of your application goes here
YOUR_APPLICATION_ID = "mlbFaceRecognition"

# Important columns in CSV file
IMAGE_ADDRESS_COL = 4
FIRST_NAME_COL = 1
LAST_NAME_COL = 2

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
NOTE: this function takes a local image as an argument, not a url
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
        # print(post_model_outputs_response)
        raise Exception(f"Request failed, status code: {post_model_outputs_response.status}")

    out = post_model_outputs_response.outputs[0]
    return out.data.regions[0].region_info.bounding_box

"""
Given an input image, function converts the image to an OpenCV object.
Crops this image to be just the human face. 
NOTE: this function takes a local image as an argument, not a url
"""
def crop_face(image):
    img = cv2.imread(image)
    ROWS = img.shape[0]
    COLS = img.shape[1]

    try:
        bounding_box = detect_face(image)
    except Exception as e:
        print(e)
    else:
        top = int(bounding_box.top_row * ROWS) 
        bottom = int(bounding_box.bottom_row * ROWS)
        left = int(bounding_box.left_col * COLS)
        right = int(bounding_box.right_col * COLS)

        crop = img[top:bottom, left:right] 
        cv2.imwrite(image, crop)

"""
Reads a csv file and attempts to download the image url from each row.
Additionally, a new csv file containing the local paths of the cropped images
will be created.
"""
def process_csv(csv_reader):
    outp = []
    invalid_outp = [] 
    header = ['First Name', 'Last Name', 'White', 'Black', 'Asian', 'Other', 'Highest Prob. Score', 'Filler', 'Image']
    # NOTE: Change the destination of the new cropped photos csv file here
    f = open('C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/CroppedMLBPlayers/MLB_Cropped_Photos_No_Data.csv', 'w+', encoding='utf8', newline='')
    writer = csv.writer(f)
    writer.writerow(header)

    # Open the CSV file for invalid URLs
    invalid_f = open('invalid_urls.csv', 'w+', encoding='utf8', newline='')
    invalid_writer = csv.writer(invalid_f)
    invalid_writer.writerow(['First Name', 'Last Name', 'Image URL'])

    for row in csv_reader:
        IMAGE_URL = row[IMAGE_ADDRESS_COL]
        if check_valid_url(IMAGE_URL):
            # NOTE: Change the destination of the cropped images here
            image_dst = "C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/CroppedMLBPlayers/{first_name}_{last_name}.jpg".format(first_name=row[FIRST_NAME_COL].encode('unicode_escape').decode('utf-8'), 
                                                                                                                                   last_name=row[LAST_NAME_COL].encode('unicode_escape').decode('utf-8'))
            try:
                url_to_image(IMAGE_URL, image_dst)
                crop_face(image_dst)
            except Exception as e:
                print("{first_name} {last_name}: invalid image url: {url}".format(first_name=row[FIRST_NAME_COL], last_name=row[LAST_NAME_COL], url=row[IMAGE_ADDRESS_COL]))
                invalid_outp.append([row[FIRST_NAME_COL], row[LAST_NAME_COL], row[IMAGE_ADDRESS_COL]])
            else:
                outp.append([row[FIRST_NAME_COL], row[LAST_NAME_COL], None, None, None, None, None, None, image_dst])
        else:
            outp.append([row[FIRST_NAME_COL], row[LAST_NAME_COL], None, None, None, None, None, None, "Invalid image URL"])
    writer.writerows(outp)
    invalid_writer.writerows(invalid_outp)

def main():
    # NOTE: Change the csv file being read here
    file = open('C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/cleaned_mlb_players.csv', encoding="utf8")
    reader = csv.reader(file)
    next(reader)
    process_csv(reader)

if __name__ == "__main__":
    main()
