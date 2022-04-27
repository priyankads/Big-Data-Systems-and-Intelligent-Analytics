import h5py
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib.patches as patches
import pandas as pd
import os
# from display.display import get_cmap
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
import cv2
import subprocess
from starlette.responses import StreamingResponse
from geopy import distance
import urllib.parse
import requests
import io
import json
import h5py
import boto3
from botocore.handlers import disable_signing
from os import walk
from fastapi import FastAPI, Request
import uvicorn
import requests
import urllib.parse
import imageio
import glob
import streamlit as st
import plotly.express as px
import base64



with open("config.json", "r") as jsonfile:
    data_model = json.load(jsonfile)

mse_model_path = data_model["mse_model"]
print("Loading Model")
new_model = tf.keras.models.load_model(mse_model_path, compile=False, custom_objects={"tf": tf})

# http://127.0.0.1:8000

app = FastAPI()


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )



catalog_2events = pd.read_csv(data_model["catalog_storm_csv"])





################### Download H5 files for selected Event Id only ##########################################
def get_filename_index(event_id):
    catlog = pd.read_csv("https://raw.githubusercontent.com/MIT-AI-Accelerator/eie-sevir/master/CATALOG.csv")
    filtered = pd.DataFrame()
    for i in event_id:
        filtered = pd.concat([filtered, catlog[catlog["event_id"] == int(i)]])
        filename = filtered['file_name'].unique()
        fileindex = filtered['file_index'].unique()
    print("We have got the locations, Lets Download the files")
    return filename, fileindex


# def download_hf(filename):
#     resource = boto3.resource('s3')
#     resource.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
#     bucket = resource.Bucket('sevir')

#     for i in range(len(filename)):
#         filename1 = "data/" + filename[i]
#         print("Downloading", filename1)
#         bucket.download_file(filename1, "SEVIR/" + filename[i].split('/')[2])


def One_Sample_HF(directory, fileindex):
    filenames = next(walk(directory), (None, None, []))[2]  # [] if no file
    for i in range(len(filenames)):
        print(directory + filenames[i])
        if filenames[i] == '.DS_Store' or filenames[i] == '.gitkeep':
            continue
        with h5py.File(directory + "/" + filenames[i], 'r') as hf:
            image_type = filenames[i].split('_')[1]
            # if image_type == "IR107":
            #     event_id = hf['id'][int(fileindex[1])]
            #     IR107 = hf['ir107'][int(fileindex[1])]
            if image_type == "VIL":
                VIL = hf['vil'][int(fileindex)]
            # if image_type == "IR069":
            #     IR069 = hf['ir069'][int(fileindex[2])]
            # if image_type == "VIS":
            #     VIS = hf['vis'][int(fileindex[0])]
    hf1 = h5py.File('filtered_data.h5', 'w')
    hf1.create_dataset('vil', data=VIL)
    # hf1.create_dataset('vis', data=VIS)
    # hf1.create_dataset('IR107', data=IR107)
    # hf1.create_dataset('IR069', data=IR069)
    print("downloded")

def testdata(dir):
    rank=0
    size=1 
    end=None
    s = np.s_[rank:end:size]
    MEAN=33.44 
    SCALE=47.54
    # file_name = data_model['images_path']
    with h5py.File(dir) as hf:
        x_test = hf['vil'][s]
    x_test = (x_test.astype(np.float32)-MEAN)/SCALE
    return x_test

def get_lat_long(location):

    """
    Python script that does not require an API key nor external libraries 
    you can query the Nominatim service which in turn queries 
    the Open Street Map database.

    For more information on how to use it see
    https://nominatim.org/release-docs/develop/api/Search/

    """
    address = location
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'

    response = requests.get(url).json()
    # print(response[0]["lat"])
    # print(response[1]["lon"])
    return response[0]["lat"], response[1]["lon"]


# def get_data_from_google_cloud_storage():

#     storage_client = storage.Client()
#     print("Downloading the data from Google Cloud Storage")
#     bucket_name = 'sevir'
#     file_name = 'data/' + data_model['images_path']
#     print(file_name)
#     blob = storage_client.bucket(bucket_name).blob(file_name)
#     blob.download_to_filename('data/' + data_model['images_path'])
#     print("Downloaded the data from Google Cloud Storage")



def nearest_location(lat, lon, flag):
    # Returns the row from the combined csv that has 
    # least distance from the given lat and lon

    catalog_2events['distance'] = catalog_2events.apply(lambda row: distance.distance((lat, lon), (row['LATITUDE'], row['LONGITUDE'])).km, axis=1)
    nearest_loc_vil = catalog_2events.loc[catalog_2events['img_type'] == 'vil']
    nearest_loc = nearest_loc_vil.loc[nearest_loc_vil['distance'].idxmin()]
    top_min_distances = nearest_loc_vil.loc[nearest_loc_vil['distance'].nsmallest(5).index]
    top_min_distances.to_csv('top_5_min_distances.csv')
    if nearest_loc['distance'] >= 100:
        flag == True
    print(nearest_loc)
    return nearest_loc, flag

def read_data_local(filename, rank=0, size=1, end=None, dtype=np.float32, MEAN=33.44, SCALE=47.54):
    
    s = np.s_[rank:end:size]
    with h5py.File(filename, mode='r') as hf:
        x_test  = hf['vil'][s]
    x_test = (x_test.astype(dtype)-MEAN)/SCALE
    
    return x_test


# def create_nowcast(idx):
#     norm = {'scale': 47.54, 'shift': 33.44}
#     hmf_colors = np.array([
#         [82, 82, 82],
#         [252, 141, 89],
#         [255, 255, 191],
#         [145, 191, 219]
#     ]) / 255

#     # Model that implements persistence forecast that just repeats last frame of input
#     class persistence:
#         def predict(self, x_test):
#             return np.tile(x_test[:, :, :, -1:], [1, 1, 1, 12])

#     def plot_hit_miss_fa(ax, y_true, y_pred, thres):
#         mask = np.zeros_like(y_true)
#         mask[np.logical_and(y_true >= thres, y_pred >= thres)] = 4
#         mask[np.logical_and(y_true >= thres, y_pred < thres)] = 3
#         mask[np.logical_and(y_true < thres, y_pred >= thres)] = 2
#         mask[np.logical_and(y_true < thres, y_pred < thres)] = 1
#         cmap = ListedColormap(hmf_colors)
#         ax.imshow(mask, cmap=cmap)

#     def visualize_result(models, x_test, y_test, idx, labels):
#         fs = 10
#         cmap_dict = lambda s: {'cmap': get_cmap(s, encoded=True)[0],
#                                'norm': get_cmap(s, encoded=True)[1],
#                                'vmin': get_cmap(s, encoded=True)[2],
#                                'vmax': get_cmap(s, encoded=True)[3]}

#         pers = persistence().predict(x_test[idx:idx + 1])
#         pers = pers * norm['scale'] + norm['shift']
#         x_test = x_test[idx:idx + 1]
#         y_test = y_test[idx:idx + 1] * norm['scale'] + norm['shift']
#         y_preds = []
#         for i, m in enumerate(models):
#             yp = m.predict(x_test)
#             if isinstance(yp, (list,)):
#                 yp = yp[0]
#             y_preds.append(yp * norm['scale'] + norm['shift'])
#             with h5py.File("y_pred1.h5", 'w') as data:
#                 data['pred'] = y_preds[0]

#     visualize_result([new_model], x_test, y_test, idx, labels=['MSE'])


# get endpoint -> state


"""
1. model loading
2. predict
3. save 12 images
4. Save the input image for that 

"""


@app.get("/nowcast/{img_Id}")
async def predict_img(img_Id: int):
    """
    **Pass Image Id to show 1 out of 12 images!!**
    """

    # create_nowcast(1)
    str1 = ""
    path = data_model["images_path"]

    # with h5py.File('y_pred.h5', 'r') as hf:
    #     # plt.imshow(hf['pred'][0][:,:,11])
    #     print("Image " + str(img_Id) + "selected")
    #     str1 = str(hf['pred'][0][:, :, img_Id].shape)
    #     image_data = hf['pred'][0][:, :, img_Id]

    #     # for i in range(0, 11):
    #     #     name = path + "test" +  str(i) + '.png'
    #     #     plt.imsave(name, hf['pred'][0][:,:,i])
    #     plt.imsave("test.png", image_data)

    filepath = os.path.join(data_model['images_path'], "test" + str(img_Id) +".png")
    if os.path.exists(filepath):
        return FileResponse(filepath)

    return {"error": "File not found!"}


# Need to generate new H5 file from user selection of location HERE


@app.get("/weatherviz/{location}")
async def filter_nowcast(location: str, next_nearest: str):
    """
    **Get Nowcast Images for the exact or nearest location in SEVIR**

    """
    # w, c = "", ""
    # t, v = "", ""

    # if state == "MISSOURI":
    #     w = catalog_2events['event_type_y'].loc[catalog_2events['state'] == 'MISSOURI']
    #     t = catalog_2events['event_narrative'].loc[catalog_2events['state'] == 'MISSOURI']
    #     return {"Event Type": w, "Event Narrative": t}

    # elif state == "MINNESOTA":
    #     c = catalog_2events['event_type_y'].loc[catalog_2events['state'] == 'MINNESOTA']
    #     v = catalog_2events['event_narrative'].loc[catalog_2events['state'] == 'MINNESOTA']
    #     print(c, v)
    #     return {"Event Type": c, "Event Narrative": v}
    
    flag = False
    norm = {'scale': 47.54, 'shift': 33.44}
    location_lat_long = get_lat_long(location)
    print(location_lat_long)
    # gives me the row in catalog with nearest location
    nearest_location_catalog, not_nearest = nearest_location(location_lat_long[0], location_lat_long[1], flag)
    # print("FLAG VALUE", not_nearest)
    # not_nearest flag stores if the nearest datapoint is within 100 kms of user input location
    # if flag is true -> nearest location is outside 100 kms of user input location
    
    event_file_name = nearest_location_catalog['file_name']
    event_file_index = nearest_location_catalog['file_index']
    event_id_nearest = nearest_location_catalog['event_id']
    One_Sample_HF(data_model['images_path'], event_file_index)
    # x_test = read_data_local('filtered_data.h5', end=50)
    x_test = testdata('filtered_data.h5')
    x_test = x_test.reshape(1, 384, 384, 49)
    x_test_now = x_test[:, :, :, :13]

    # Check what is shape of x_test
    # x_test = x_test[idx:idx + 1]
    # y_test = y_test[idx:idx + 1] * norm['scale'] + norm['shift']
    y_preds = []
    # cmap_dict = lambda s: {'cmap': get_cmap(s, encoded=True)[0],
    #                            'norm': get_cmap(s, encoded=True)[1],
    #                            'vmin': get_cmap(s, encoded=True)[2],
    #                            'vmax': get_cmap(s, encoded=True)[3]}
    # for i, m in enumerate(models):
    yp = new_model.predict(x_test_now)
    if isinstance(yp, (list,)):
        yp = yp[0]
    y_preds.append(yp * norm['scale'] + norm['shift'])
    with h5py.File("y_pred.h5", 'w') as data:
        data['pred'] = y_preds[0]

    
    # Read the y pred h5 file

    with h5py.File('y_pred.h5', 'r') as hf:
        # plt.imshow(hf['pred'][0][:,:,11])
        # print("Image " + str(img_Id) + "selected")
        # str1 = str(hf['pred'][0][:, :, img_Id].shape)
        for i in range(0, 12):
            name = data_model['images_path'] + "test" +  str(i) + '.png'
            plt.imsave(name, hf['pred'][0][:,:,i])
            # image_data = hf['pred'][0][:, :, 1]
            # plt.imsave("test.png", image_data)

        # Create a GIF out of images
        

        filenames = glob.glob(data_model['images_path']+'test*.png')
        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))
        imageio.mimsave(data_model['images_path']+"nowcast"+ '.gif', images)

    # if nearest_location_catalog['distance'] >= 100:
    #     return {"data": None, "message": "No nearest location found within 100 kms of your location"}

    # Based on next_nearest variable -> yes/no show message or images
    if next_nearest.lower() == "yes":
        filepath = os.path.join(data_model['images_path'], "nowcast.gif")
        if os.path.exists(filepath):
            return FileResponse(filepath)

        return {"error": "File not found!"}
        
    else:

        return {"message": "No nearest location found within 100 kms of your location"}


############### STREAMLIT #######################

# def filter_nowcast1(location, next_nearest):
#     """
#     **Get Nowcast Images for the exact or nearest location in SEVIR**

#     """
#     # w, c = "", ""
#     # t, v = "", ""

#     # if state == "MISSOURI":
#     #     w = catalog_2events['event_type_y'].loc[catalog_2events['state'] == 'MISSOURI']
#     #     t = catalog_2events['event_narrative'].loc[catalog_2events['state'] == 'MISSOURI']
#     #     return {"Event Type": w, "Event Narrative": t}

#     # elif state == "MINNESOTA":
#     #     c = catalog_2events['event_type_y'].loc[catalog_2events['state'] == 'MINNESOTA']
#     #     v = catalog_2events['event_narrative'].loc[catalog_2events['state'] == 'MINNESOTA']
#     #     print(c, v)
#     #     return {"Event Type": c, "Event Narrative": v}
    
#     flag = False
#     norm = {'scale': 47.54, 'shift': 33.44}
#     location_lat_long = get_lat_long(location)
#     # gives me the row in catalog with nearest location
#     nearest_location_catalog, not_nearest = nearest_location(location_lat_long[0], location_lat_long[1], flag)
#     # not_nearest flag stores if the nearest datapoint is within 100 kms of user input location
#     # if flag is true -> nearest location is outside 100 kms of user input location
#     event_file_name = nearest_location_catalog['file_name']
#     event_file_index = nearest_location_catalog['file_index']
#     event_id_nearest = nearest_location_catalog['event_id']
#     One_Sample_HF(data_model['images_path'], event_file_index)
#     # x_test = read_data_local('filtered_data.h5', end=50)
#     x_test = testdata('filtered_data.h5')
#     x_test = x_test.reshape(1, 384, 384, 49)
#     x_test_now = x_test[:, :, :, :13]

#     # Check what is shape of x_test
#     # x_test = x_test[idx:idx + 1]
#     # y_test = y_test[idx:idx + 1] * norm['scale'] + norm['shift']
#     y_preds = []
#     cmap_dict = lambda s: {'cmap': get_cmap(s, encoded=True)[0],
#                             'norm': get_cmap(s, encoded=True)[1],
#                             'vmin': get_cmap(s, encoded=True)[2],
#                             'vmax': get_cmap(s, encoded=True)[3]}
#     # for i, m in enumerate(models):
#     yp = new_model.predict(x_test_now)
#     if isinstance(yp, (list,)):
#         yp = yp[0]
#     y_preds.append(yp * norm['scale'] + norm['shift'])
#     with h5py.File("y_pred.h5", 'w') as data:
#         data['pred'] = y_preds[0]

    
#     # Read the y pred h5 file

#     with h5py.File('y_pred.h5', 'r') as hf:
#         # plt.imshow(hf['pred'][0][:,:,11])
#         # print("Image " + str(img_Id) + "selected")
#         # str1 = str(hf['pred'][0][:, :, img_Id].shape)
#         for i in range(0, 12):
#             name = data_model['images_path'] + "test" +  str(i) + '.png'
#             plt.imsave(name, hf['pred'][0][:,:,i])
#         # image_data = hf['pred'][0][:, :, 1]
#         # plt.imsave("test.png", image_data)

#     # Create a GIF out of images
    

#     filenames = glob.glob(data_model['images_path']+'test*.png')
#     images = []
#     for filename in filenames:
#         images.append(imageio.imread(filename))
#     imageio.mimsave(data_model['images_path']+"nowcast"+ '.gif', images)


#     # Based on next_nearest variable -> yes/no show message or images
#     if next_nearest.lower() == "yes":
#         filepath = os.path.join(data_model['images_path'], "nowcast.gif")
#         if os.path.exists(filepath):
#             return FileResponse(filepath)

#         return {"error": "File not found!"}
        
#     else:
        
#         return {"message": "No nearest location found within 100 kms of your location"}







