################################################################################
# Demographics Inference Program                                               #
# Utilizing Clarifai API, Inputs and outputs CSV files                         #
################################################################################

# Imports for Clarifai and CSV output
import csv
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2

stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

# Personal access tokens. Can be changed if needed, directly from Clarifai website.
YOUR_CLARIFAI_API_KEY = "6132926d458145c0b54df487722c2cfe"
YOUR_APPLICATION_ID = "dem_infer"


# Do not change
#channel = ClarifaiChannel.get_grpc_channel()
metadata = (("authorization", f"Key {YOUR_CLARIFAI_API_KEY}"),)


# Where the image URL and name is located in the input file. Change if needed.
IMAGE_ADDRESS_COL = 8
FIRST_NAME_COL = 0
LAST_NAME_COL = 1
#NAME_COL = 0


# Clarifai-provided method for using API. model_id can be found online, and is
# currently set as the demographics predictor's id. Outputs prediction for one
# photo.
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

# Ensures that there is a URL and that it is not a default avatar.
def check_valid_url(inp):
    if (inp is not None) and ("N\A" not in inp) and ("avatar" not in inp) and ("placeholder" not in inp):
        return True
    return False

def process_input(inp):
    outp = []

    header = ['First Name', 'Last Name', 'White', 'Black', 'East Asian', 'Southeast Asian', 'Indian', 'Middle Eastern', 'Latino Hispanic', 'Prediction']
    f = open('ImDB_Inferences.csv', 'w+', encoding='UTF8', newline='')

    writer = csv.writer(f)
    writer.writerow(header)

    for row in inp:
        out = get_demographic_info(row[IMAGE_ADDRESS_COL])
        results = [0] * 10
        results[0] = row[FIRST_NAME_COL]
        results[1] = row[LAST_NAME_COL]
        #print(row[FIRST_NAME_COL], row[LAST_NAME_COL])
        for var in out:
            eth = var.name
            confidence = var.value
            max_confidence = 0
            probable_eth = None

            # White, Black, East Asian, SEA, Indian, Middle Eastern, Latino/Hispanic
            if eth == 'White':
                results[2] = confidence
                if confidence > max_confidence:
                    max_confidence = confidence
                    probable_eth = 'White'
            elif eth == 'Black':
                results[3] = confidence
                if confidence > max_confidence:
                    max_confidence = confidence
                    probable_eth = 'Black'
            elif eth == 'East Asian':
                results[4] = confidence
                if confidence > max_confidence:
                    max_confidence = confidence
                    probable_eth = 'East Asian'
            elif eth == 'Southeast Asian':
                results[5] = confidence
                if confidence > max_confidence:
                    max_confidence = confidence
                    probable_eth = 'Southeast Asian'
            elif eth == 'Indian':
                results[6] = confidence
                if confidence > max_confidence:
                    max_confidence = confidence
                    probable_eth = 'Indian'
            elif eth == 'Middle Eastern':
                results[7] = confidence
                if confidence > max_confidence:
                    max_confidence = confidence
                    probable_eth = 'Middle Eastern'
            elif eth == 'Latino Hispanic':
                results[8] = confidence
                if confidence > max_confidence:
                    max_confidence = confidence
                    probable_eth = 'Latino Hispanic'
            results[9] = probable_eth
        outp.append(results)
    writer.writerows(outp)


# Runs the program.
def main():
    file = open(r'C:\Users\2alex\OneDrive\Documents\GitHub\Ethnicity-Inference-2022\ImDB Webcrawling\imdb_no_data.csv')
    reader = csv.reader(file)
    next(reader)
    process_input(reader)


if __name__ == "__main__":
    main()