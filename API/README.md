To use Clarifai and Namsor APIs, you must have the API Keys.

Please create a .env file in this directory and add the following:

NAMSOR_API_KEY = 'XXXXXX'  
CLARIFAI_API_KEY = 'XXXXXX'

Replace with your API key from creating accounts for Namsor/Clarifai or ask for one in the group.

Notes (3/13/2024)

Upon first testing of 400 names achieved an accuracy score of 72.81% with combined model. Face yielded a 51.12% accuracy and Name yieled a 77.81%. This could be due to the fact that the faculty dataset images were less reliable than our training set, and the model gave more weight to the face than name.
