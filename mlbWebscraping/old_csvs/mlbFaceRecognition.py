################################################################################
# Demographics Inference Program                                               #
# Utilizing Clarifai API, Inputs and outputs CSV files                         #
################################################################################

# Imports for Clarifai and CSV output
import csv
import requests
import os
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2

stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

# Personal access tokens. Can be changed if needed, directly from Clarifai website.
YOUR_CLARIFAI_API_KEY = "089d22e2f2ed4a25aeb365fc23badb42"
YOUR_APPLICATION_ID = "mlbFaceRecognition"


# Do not change
#channel = ClarifaiChannel.get_grpc_channel()
metadata = (("authorization", f"Key {YOUR_CLARIFAI_API_KEY}"),)


# Where the image URL and name is located in the input file. Change if needed.
IMAGE_ADDRESS_COL = 2
FIRST_NAME_COL = 0
LAST_NAME_COL = 1


# Clarifai-provided method for using API. model_id can be found online, and is
# currently set as the demographics predictor's id. Outputs prediction for one
# photo.

# modify this so it takes an image instead of an image url
def get_demographic_info(image_bytes):
    # with open(image_bytes, 'rb') as f:
    #     file_bytes = f.read()
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            # This is the model ID of a publicly available General model. You may use any other public or custom model ID.
            model_id="ethnicity-demographics-recognition",
            user_app_id=resources_pb2.UserAppIDSet(app_id=YOUR_APPLICATION_ID),
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(image=resources_pb2.Image(base64=image_bytes))
                )
            ],
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response)
        raise Exception(f"Request failed, status code: {post_model_outputs_response.status}")

    out = post_model_outputs_response.outputs[0]
    return out.data.concepts



# Sorts the data outputted to an array for output purposes. Columns are as follows:
# 0: First name
# 1: Last name
# 2: White confidence score
# 3: Black confidence score
# 4: Asian confidence score (Southeast Asian, East Asian, or Indian)
# 5: "Other" confidence score (Middle Eastern, Latino_Hispanic)
# 6: The ethnicity inference with the highest confidence score
def generate_data(first_name, last_name, concepts):
    result = [0] * 7
    result[0] = first_name
    result[1] = last_name
    max_prob_score = 0
    max_prob_eth = None
    for concept in concepts:
        cn = concept.name
        if cn == "White":
            result[2] = concept.value
            if concept.value > max_prob_score:
                max_prob_score = concept.value
                max_prob_eth = "White"
        elif cn == "Black":
            result[3] = concept.value
            if concept.value > max_prob_score:
                max_prob_score = concept.value
                max_prob_eth = "Black"
        elif cn == "East Asian" or cn == "Southeast Asian" or cn == "Indian":
            result[4] = result[4] + concept.value
            if result[4] > max_prob_score:
                max_prob_score = result[4]
                max_prob_eth = "Asian"
        elif cn == "Middle Eastern" or cn == "Latino_Hispanic":
            result[5] = result[5] + concept.value
            if result[5] > max_prob_score:
                max_prob_score = result[5]
                max_prob_eth = "Other"
    result[6] = max_prob_eth
    return result


# Reads all image files in the specified folder and runs the demographic predictor on each.
def process_images(folder_path):
    outp = []

    header = ['First Name', 'Last Name', 'White', 'Black', 'Asian', 'Other', 'Highest Prob. Score']
    with open('cropped_output.csv', 'w+', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    try:
                        with open(os.path.join(folder_path, filename), "rb") as f:
                            file_bytes = f.read()
                        ethnicity_list = get_demographic_info(file_bytes)
                        cleaned_concepts = generate_data(os.path.splitext(filename)[0], "", ethnicity_list)
                        outp.append(cleaned_concepts)
                    except Exception as e:
                        outp.append([os.path.splitext(filename)[0], "", None, None, None, None, str(e)])
                else:
                    outp.append([os.path.splitext(filename)[0], "", None, None, None, None, "Not an image file"])

            writer.writerows(outp)
        else:
            print("Error: folder_path is not a directory")

# Runs the program.
def main():
    folder_path = "C:\MAVACResearchMugizi\Winter2023\mlbWebscraping\CroppedMLBPlayers"
    process_images(folder_path)


if __name__ == "__main__":
    main()