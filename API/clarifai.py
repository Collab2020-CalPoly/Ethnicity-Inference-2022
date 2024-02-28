# Last Modified: 2/28/24 by Ethan Outangoun


# Remove Warnings
import warnings
warnings.filterwarnings("ignore")

# Load environment variables
from dotenv import load_dotenv
import os
load_dotenv()

# Imports for Clarifai and CSV output
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())  

# Personal access tokens. Can be changed if needed, directly from Clarifai website.
YOUR_CLARIFAI_API_KEY = os.getenv("CLARIFAI_API_KEY") or " "
YOUR_APPLICATION_ID = "dem_inference"
metadata = (("authorization", f"Key {YOUR_CLARIFAI_API_KEY}"),)



def get_demographic_info(image_url):
    with open(image_url, "rb") as f:
        file_bytes = f.read()
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            # This is the model ID of a publicly available General model. You may use any other public or custom model ID.
            model_id="ethnicity-demographics-recognition",
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
    return out.data.concepts

def process_info(info):
    result = [0] * 7
  
    max_prob_score = 0
    max_prob_eth = None
    for concept in info:
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
  

    return result[6]


def clarifaiPredict(image_url):
    info = get_demographic_info(image_url)
    race = process_info(info)

    return race

    
    

if __name__=="__main__":
    name = clarifaiPredict("./Pictures/caeleb_dressel.jpg")
    print(name)

