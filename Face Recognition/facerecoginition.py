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
YOUR_CLARIFAI_API_KEY = "7bbefe8ab9b04848bad0ab95fcf2da29"
YOUR_APPLICATION_ID = "dem_inference"


# Do not change
#channel = ClarifaiChannel.get_grpc_channel()
metadata = (("authorization", f"Key {YOUR_CLARIFAI_API_KEY}"),)


# Where the image URL and name is located in the input file. Change if needed.
IMAGE_ADDRESS_COL = 8
FIRST_NAME_COL = 0
LAST_NAME_COL = 1


# Clarifai-provided method for using API. model_id can be found online, and is
# currently set as the demographics predictor's id. Outputs prediction for one
# photo.
def get_demographic_info(image_url):
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            # This is the model ID of a publicly available General model. You may use any other public or custom model ID.
            model_id="ethnicity-demographics-recognition",
            user_app_id=resources_pb2.UserAppIDSet(app_id=YOUR_APPLICATION_ID),
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(image=resources_pb2.Image(url=image_url))
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

    #    elif cn == "East Asian":
    #        result[4] = concept.value
    #        if concept.value > max_prob_score:
    #            max_prob_score = concept.value
    #            max_prob_eth = "East Asian"
    #    elif cn == "Southeast Asian" or cn == "Middle Eastern" or cn == "Latino_Hispanic" or cn == "Indian":
    #        result[5] = result[5] + concept.value
    #        if result[5] > max_prob_score:
    #            max_prob_score = result[5]
    #            max_prob_eth = "Other"
    #result[6] = max_prob_eth
    #return result


# Ensures that there is a URL and that it is not a default avatar.
def check_valid_url(inp):
    if (inp is not None) and ("N\A" not in inp) and ("avatar" not in inp) and ("placeholder" not in inp):
        return True
    return False


# Reads the input CSV file as specified, and runs the demographic predictor on each
# valid image URL. Catches any errors that Clarifai produces while running. Outputs
# to the file.
def process_input(inp):
    outp = []

    header = ['First Name', 'Last Name', 'White', 'Black', 'Asian', 'Other', 'Highest Prob. Score']
    f = open('Inferences_78.csv', 'w+', encoding='UTF8', newline='')

    writer = csv.writer(f)
    writer.writerow(header)

    for row in inp:
        if check_valid_url(row[IMAGE_ADDRESS_COL]):
            print(row[IMAGE_ADDRESS_COL])
            try:
                ethnicity_list = get_demographic_info(row[IMAGE_ADDRESS_COL])
            except Exception as e:
                outp.append([row[FIRST_NAME_COL], row[LAST_NAME_COL], None, None, None, None, "Invalid image URL"])
            else:
                cleaned_concepts = generate_data(row[FIRST_NAME_COL], row[LAST_NAME_COL], ethnicity_list)
                outp.append(cleaned_concepts)
        else:
            outp.append([row[FIRST_NAME_COL], row[LAST_NAME_COL], None, None, None, None, "Not given image"])
    writer.writerows(outp)


# Runs the program.
def main():
    file = open('78_Photos.csv')
    reader = csv.reader(file)
    next(reader)
    process_input(reader)


if __name__ == "__main__":
    main()