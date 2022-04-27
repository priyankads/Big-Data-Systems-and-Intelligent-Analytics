import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import requests
import base64
import json
import os





################# STREAMLIT ####################

base_url = 'http://127.0.0.1:8000/weatherviz/'

with open("config.json", "r") as jsonfile:
    data_model = json.load(jsonfile)




    
NOWCAST_HTML_TEMPLATE = """
<div style="width:100%;height:100%;margin:1px;padding:5px;position:relative;border-radius:5px;border-bottom-right-radius: 10px;
box-shadow:0 0 1px 1px #eee; background-color: #31333F;
  border-left: 5px solid #6c6c6c;color:white;">
<h4>{}</h4>
<h4>{}</h4>
<h5>{}</h5>
<h6>{}</h6>
</div>
"""

NOWCAST_DES_HTML_TEMPLATE = """
<div style='color:#fff'>
{}
</div>
"""



menu = ["Home","About"]
choice = st.sidebar.selectbox("Menu",menu)

# st.title("DevDeeds -Search Jobs")
st.title('Media Nowcasting System')
st.write("")
        

if choice == "Home":
    st.subheader("Home")

    # Nav  Search Form
    with st.form(key='searchform'):
        nav1,nav2,nav3 = st.columns([3,2,1])

        with nav1:
            location = st.text_input("Enter a Location")
            
        with nav2:
            show_next_nearest = st.text_input("Show Next Nearest Location? (yes/no)")

        with nav3:
            submit_search = st.form_submit_button(label='Search')
            clear = st.form_submit_button(label="Reset")

    st.success("You searched for {} and need next nearest location : {}".format(location,show_next_nearest))



    # Results
    col1, col2 = st.columns([2,1])

    with col1:
        pics = {}
        showWarningOnDirectExecution = False
        if submit_search:
            # Create Search Query
            search_url = base_url+location+'?'+'next_nearest='+show_next_nearest
            # st.write(search_url)
            res = requests.get(search_url)
            print("RESPONSE", res)
            df = pd.read_csv('/Users/priyankashinde/Desktop/neurips-2020-sevir-master/backend/top_5_min_distances.csv')
            df1 = df[:1]
            print("NEWWWWWWWW")
            print(df1['distance'])
            # if int(df1['distance']) >= 100:
            #     for i in range(0, 12):
            #         os.remove(data_model['images_path'] + "test" +  str(i) + '.png')
            #     os.remove(data_model['images_path'] + "nowcast.gif")
            #     os.remove(data_model['event_narrative_path'])
            #     os.remove('/Users/priyankashinde/Desktop/neurips-2020-sevir-master/backend/filtered_data.h5')
            #     os.remove('/Users/priyankashinde/Desktop/neurips-2020-sevir-master/backend/y_pred.h5')
            #     st.header("No nearest (location found within 100 kms of your location")
            # if show_next_nearest.lower() != "no" or show_next_nearest.lower() != "yes":
            #     for i in range(0, 12):
            #         os.remove(data_model['images_path'] + "test" +  str(i) + '.png')
            #     os.remove(data_model['images_path'] + "nowcast.gif")
            #     os.remove(data_model['event_narrative_path'])
            #     os.remove('/Users/priyankashinde/Desktop/neurips-2020-sevir-master/backend/filtered_data.h5')
            #     os.remove('/Users/priyankashinde/Desktop/neurips-2020-sevir-master/backend/y_pred.h5')
            #     # st.header("No nearest (location found within 100 kms of your location")
            #     st.header("Please enter yes or no")

            
        if clear:
            for i in range(0, 12):
                os.remove(data_model['images_path'] + "test" +  str(i) + '.png')
            os.remove(data_model['images_path'] + "nowcast.gif")
            os.remove(data_model['event_narrative_path'])
            os.remove('/Users/priyankashinde/Desktop/neurips-2020-sevir-master/backend/filtered_data.h5')
            os.remove('/Users/priyankashinde/Desktop/neurips-2020-sevir-master/backend/y_pred.h5')
        # if submit_search and show_next_nearest.lower() == "no":
        #     for i in range(0, 12):
        #         os.remove(data_model['images_path'] + "test" +  str(i) + '.png')
        #     os.remove(data_model['images_path'] + "nowcast.gif")
        #     os.remove(data_model['event_narrative_path'])
        #     os.remove('/Users/priyankashinde/Desktop/neurips-2020-sevir-master/backend/filtered_data.h5')
        #     os.remove('/Users/priyankashinde/Desktop/neurips-2020-sevir-master/backend/y_pred.h5')
        #     st.header("No nearest location found within 100 kms of your location")
        # elif submit_search and show_next_nearest.lower() == "yes" and :

        
            

            
            
            # image_path = data_model['images_path']+"test0.png"
            # if os.path.exists(image_path):
        for i in range(0, 12):
            pics[i] = data_model['images_path'] + "test" +  str(i) + '.png'
        if len(pics) == 0:
            st.write("Enter params to get results!")

        else:

            pic = st.select_slider('Select a Picture', options=list(pics.keys()))
            st.image(pics[pic], use_column_width=True)



    with col2:
        col2.subheader("Weather Nowcast - Next Hour")
        data_url = ""
        gif_path = data_model['images_path']+'nowcast.gif'

        if os.path.exists(gif_path):
            file_ = open(data_model['images_path']+ "nowcast.gif", "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="nowcast gif">',
            unsafe_allow_html=True,
        )

    
    st.header("Event Narrative Nearby Locations")

    event_narrative_path1 = data_model['event_narrative_path']
    if os.path.exists(event_narrative_path1):

        event_narrative_data = pd.read_csv(event_narrative_path1)
        print(event_narrative_data.head(1))
        event_narrative_data = event_narrative_data.drop(columns=['Unnamed: 0'])

        nearby_locations_list = []
        nearby_narrative_list = []
        event_type = []
        
        for i in range(0, 4):
            nearby_locations_list.append(event_narrative_data['LOCATION'][i])
            event_type.append(event_narrative_data['EVENT_TYPE'][i])
            nearby_narrative_list.append(event_narrative_data['EVENT_NARRATIVE'][i])
            
            # nearby_locations_list.append(nearest_loc)
        # print("NEARBY LIST __",len(nearby_narrative_list))
        select = st.selectbox('STATE', nearby_locations_list)
        
    
        for i in range(0, 4):
            if select == nearby_locations_list[i]:
                st.header("Event Narrative")
                st.write(nearby_narrative_list[i])
                st.header("Event Type")
                st.write(event_type[i])

        df = event_narrative_data.filter(['LATITUDE','LONGITUDE','EVENT_TYPE', 'LOCATION', 'STATE'], axis=1)
        df = df.rename({'LATITUDE':'lat', 'LONGITUDE' : 'lon'},axis='columns')


        st.header("Geo Locations of Nearby Events")


        fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="LOCATION", hover_data=["STATE", "EVENT_TYPE"],
                                color_discrete_sequence=["fuchsia"], zoom=3, height=300)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig)

else:
    st.subheader("About")










################### OLDER ############################



# col1, col2 = st.columns(2)

# with col2:
#     col2.subheader("Weather Nowcast - Next Hour")
#     data_url = ""
#     gif_path = data_model['images_path']+'nowcast.gif'
#     if os.path.exists(gif_path):
#         file_ = open(data_model['images_path']+ "nowcast.gif", "rb")
#         contents = file_.read()
#         data_url = base64.b64encode(contents).decode("utf-8")
#         file_.close()

#     st.markdown(
#         f'<img src="data:image/gif;base64,{data_url}" alt="nowcast gif">',
#         unsafe_allow_html=True,
#     )


# with col1:

#     pics = {}
#     image_path = data_model['images_path']+"test0.png"
#     if os.path.exists(image_path):
#         for i in range(0, 11):
#             pics[i] = data_model['images_path'] + "test" +  str(i) + '.png'

#         pic = st.select_slider(
#             'Select a Picture',
#             options=list(pics.keys()))
#         st.image(pics[pic], use_column_width=True)




# st.header("Event Narrative Nearby Locations")

# event_narrative_data = pd.read_csv('top_5_min_distances.csv')
# event_narrative_data = event_narrative_data.drop(columns=['Unnamed: 0'])

# nearby_locations_list = []
# nearby_narrative_list = []
# event_type = []
# if location:
#     for i in range(0, len(event_narrative_data)):
#         nearby_locations_list.append(event_narrative_data['LOCATION'][i])
#         event_type.append(event_narrative_data['EVENT_TYPE'][i])
#         if event_narrative_data.iloc[i]['STATE'] == location:
#             nearby_narrative_list.append(event_narrative_data.iloc[i]['EVENT_NARRATIVE'])
#     # nearby_locations_list.append(nearest_loc)
# select = st.selectbox('STATE', nearby_locations_list)
  
# for i in range(0, len(nearby_narrative_list)):
#     if select == nearby_locations_list[i]:
#         st.write(nearby_narrative_list[i])
#         st.write(event_type[i])


# # if select == 'KENTUCKY':
# #     st.write(data[data['STATE']=="KENTUCKY"][["EVENT_NARRATIVE", "EVENT_TYPE"]])

# # elif select == 'MINNESOTA':
# #     st.write(data[data['STATE']=="MINNESOTA"][["EVENT_NARRATIVE", "EVENT_TYPE"]])

# # elif select == 'CALIFORNIA':
# #     st.write(data[data['STATE']=="CALIFORNIA"][["EVENT_NARRATIVE", "EVENT_TYPE"]])

# # elif select == 'FLORIDA':
# #     st.write(data[data['STATE']=="FLORIDA"][["EVENT_NARRATIVE", "EVENT_TYPE"]])

# # else:
# #     st.write(data[data['STATE']=="NORTH DAKOTA"][["EVENT_NARRATIVE", "EVENT_TYPE"]])


# # top 5 events lat long Maps


# df = event_narrative_data.filter(['LATITUDE','LONGITUDE','EVENT_TYPE', 'LOCATION', 'STATE'], axis=1)
# df = df.rename({'LATITUDE':'lat', 'LONGITUDE' : 'lon'},axis='columns')


# st.header("Geo Locations of Nearby Events")


# fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="LOCATION", hover_data=["STATE", "EVENT_TYPE"],
#                         color_discrete_sequence=["fuchsia"], zoom=3, height=300)
# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# st.plotly_chart(fig)
# fig.show()