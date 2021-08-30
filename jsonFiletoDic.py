# Python program to demonstrate
# Conversion of JSON data to
# dictionary
  
  
# importing the module
import json
  
# Opening JSON file
with open('postman_json.json') as json_file:
    data = json.load(json_file)
  
    # Print the type of data variable
    print("Type:", type(data))
  
    # Print the data of dictionary
    print("\nstatuses:", len(data['statuses']))