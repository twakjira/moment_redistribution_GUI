#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import PySimpleGUI as sg
import numpy as np
import pandas as pd
from pickle import load
from PIL import Image
from PIL import ImageOps

#import the dataset
dd1 = pd.read_excel('data.xlsx', sheet_name = 'data')
df=dd1.copy(deep=True)

t=40
td=45
td2=12

# define the range of values for each parameter
Ag_range = [24900, 154530]
ad_range = [4.669261, 16.806723]
fc_range = [14.560000, 81.000000]
long_rein_type_range = [0, 4]
Fu_sagging_range = [731.000000, 1773.000000]
E_sagging_range = [42.700000, 137.000000]
Fu_hogging_range = [731.000000, 1773.000000]
E_hogging_range = [42.700000, 137.000000]
sagging_hogging_reinforcement_ratio_range = [0.213333, 4.687500]
stirrups_type_range = [0, 3]
stirrups_strength_range = [0, 1383]
transverse_reinforcement_ratio_range = [0, 1.867116]

stirrups_type_choices = ['None', 'BFRP', 'GFRP', 'Steel']
long_type_choices = ['BFRP', 'BFRP+steel', 'CFRP', 'GFRP', 'GFRP+steel']

sg.theme('DefaultNoMoreNagging')
# sg.theme_background_color('lightgray')

layout = [
    [sg.Text('Developed by Abushanab A., Wakjira T., Alnahhal W., Alam MS.')],
            [sg.Text('University of British Columbia Okanagan, Qatar University')],
#             [sg.Text('Contact: tgwakjira@gmail.com, www.tadessewakjira.com/Contact')],
            #[sg.Text('Input parameters')],
    [
      sg.Column(layout=[
            [sg.Frame(layout=[                      
            [sg.Text('Gross area (Ag)', size=(t, 1)), sg.InputText(key='-f1-', size=(td2, 1)), sg.Text('mm²')],
            [sg.Text('Shear span-to-effective depth ratio (a/d)', size=(t, 1)), sg.InputText(key='-f2-', size=(td2, 1)), sg.Text('')],
            [sg.Text('Concrete compressive strength (fc)', size=(t, 1)), sg.InputText(key='-f3-', size=(td2, 1)), sg.Text('MPa')],               
                
            
            [sg.Text('Type of longitudinal reinforcement bar', size=(t, 1)), 
            sg.Combo(long_type_choices, default_value='BFRP', key='-f4-', size=(td2, 1)),
            sg.Text('')], 
                
#             [sg.Text('long. Rein type', size=(t, 1)), sg.InputText(key='-f4-', size=(td2, 1)), sg.Text('')],
                
            [sg.Text('Ultimate strength of sagging reinforcement (Fu sagging)', size=(t, 1)), sg.InputText(key='-f5-', size=(td2, 1)), sg.Text('MPa')],
            [sg.Text('Elastic modulus of sagging reinforcement (E sagging)', size=(t, 1)), sg.InputText(key='-f6-', size=(td2, 1)), sg.Text('GPa')],
            [sg.Text('Ultimate strength of hogging reinforcement (Fu hogging)', size=(t, 1)), sg.InputText(key='-f7-', size=(td2, 1)), sg.Text('MPa')],
            [sg.Text('Elastic modulus of hogging reinforcement (E hogging)', size=(t, 1)), sg.InputText(key='-f8-', size=(td2, 1)), sg.Text('GPa')],
            [sg.Text('Ratio of sagging to hogging reinforcement ratio', size=(t, 1)), sg.InputText(key='-f9-', size=(td2, 1)), sg.Text('')],
#             [sg.Text('stirrups type', size=(t, 1)), sg.InputText(key='-f10-', size=(td2, 1)), sg.Text('')],
                
            [sg.Text('Type of bar used for stirrups, if any', size=(t, 1)), 
            sg.Combo(stirrups_type_choices, default_value='None', key='-f10-', size=(td2, 1)),
            sg.Text('')],           
            
            [sg.Text('stirrups strength (fy or Fu)', size=(t, 1)), sg.InputText(key='-f11-', size=(td2, 1)), sg.Text('MPa')],
            [sg.Text('transverse reinforcement ratio', size=(t, 1)), sg.InputText(key='-f12-', size=(td2, 1)), sg.Text('')]],          

            title='Input parameters')],
        ], justification='left'),
        
            
            
            sg.Column(layout=[
            [sg.Frame(layout=[
            
            [sg.Text('24900 mm² ≤ Ag ≤ 154530 mm²')],
            [sg.Text('4.669261 ≤ a/d ≤ 16.806723')],
            [sg.Text('14.56 MPa ≤ fc ≤ 81 MPa')],
            [sg.Text('')],
            [sg.Text('731 MPa ≤ Fu sagging ≤ 1773 MPa')],
            [sg.Text('42.7 GPa ≤ E sagging ≤ 137 GPa')],
            [sg.Text('731 MPa ≤ Fu hogging ≤ 1773 MPa')],
            [sg.Text('42.7 GPa ≤ E hogging ≤ 137 GPa')],
            [sg.Text('0.213333 ≤ sagging/hogging reinforcement ratio ≤ 4.6875')],
            [sg.Text(' ')],
            [sg.Text('0 MPa ≤ stirrups strength (fy or Fu) ≤ 1383 MPa')],
            [sg.Text('0 ≤ transverse reinforcement ratio ≤ 1.867116')]],
            title='Range of applications of the model')],             
            
                     ], justification='center') 
  ],
[sg.Frame(layout=[   
            [sg.Text('Moment redistribution',size=(40, 1)), sg.InputText(key='-OP-', size=(td2,1)),sg.Text('%')]],
                      title='Output')],
            [sg.Button('Predict'),sg.Button('Cancel')]
]


# Open the images
img1 = Image.open('image1.png')
img2 = Image.open('image2.png')
img3 = Image.open('image3.png')
img4 = Image.open('image4.png')

# Get the minimum width and height among the images
widths = [img1.width, img2.width, img3.width, img4.width]
heights = [img1.height, img2.height, img3.height, img4.height]
min_width = min(widths)
min_height = min(heights)

# Resize the images to the minimum size
img1 = ImageOps.fit(img1, (min_width, min_height))
img2 = ImageOps.fit(img2, (min_width, min_height))
img3 = ImageOps.fit(img3, (min_width, min_height))
img4 = ImageOps.fit(img4, (min_width, min_height))

# Define the scale factor
scale_factor = 0.8

# Resize the images
img1 = img1.resize((int(min_width * scale_factor), int(min_height * scale_factor)))
img2 = img2.resize((int(min_width * scale_factor), int(min_height * scale_factor)))
img3 = img3.resize((int(min_width * scale_factor), int(min_height * scale_factor)))
img4 = img4.resize((int(min_width * scale_factor), int(min_height * scale_factor)))

# Save the resized images
img1.save('image11.png')
img2.save('image22.png')
img3.save('image33.png')
img4.save('image44.png')

# To add figures in two columns
fig1 = sg.Image(filename='image11.png', key='-fig1-', size=(min_width * scale_factor, min_height * scale_factor))
fig2 = sg.Image(filename='image22.png', key='-fig2-', size=(min_width * scale_factor, min_height * scale_factor))
fig3 = sg.Image(filename='image33.png', key='-fig3-', size=(min_width * scale_factor, min_height * scale_factor))
fig4 = sg.Image(filename='image44.png', key='-fig4-', size=(min_width * scale_factor, min_height * scale_factor))

# # To add description of the image
# fig1_desc = sg.Text('Image 1')
# fig2_desc = sg.Text('Image 2')
layout += [[sg.Column([[sg.Text('Authors: Abushanab A., Wakjira T., Alnahhal W., Alam MS.')],
                [sg.Text('Contact: tgwakjira@gmail.com,'+ '\n'
                         '             www.tadessewakjira.com/Contact')],
            ],
            element_justification='left'
        ),
        sg.Column(
            [   [fig1,
                fig2,
                fig3,
                fig4,
                ],
            ],
            element_justification='center'
        ),
    ]
]


# Create the Window
window = sg.Window('Novel hybrid ML-based moment redistribution prediction for FRP-reinforced concrete beams', layout)

import pickle

with open("model1.pkl", "rb") as file:
    m1 = pickle.load(file)

with open("model2.pkl", "rb") as file:
    m2 = pickle.load(file)

with open("model3.pkl", "rb") as file:
    m3 = pickle.load(file)



while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    elif event == 'Predict':
        try:
            # get the input values
            Ag = float(values['-f1-'])
            a_d = float(values['-f2-'])
            fc = float(values['-f3-'])
            
            long_rein_type = 0  # default value (BFRP)
            if values['-f4-'] == 'BFRP+steel':
                long_rein_type = 1
            elif values['-f4-'] == 'CFRP':
                long_rein_type = 2
            elif values['-f4-'] == 'GFRP':
                long_rein_type = 3
            elif values['-f4-'] == 'GFRP+steel':
                long_rein_type = 4
            
            
#             long_rein_type = float(values['-f4-'])
            Fu_sagging = float(values['-f5-'])
            E_sagging = float(values['-f6-'])
            Fu_hogging = float(values['-f7-'])
            E_hogging = float(values['-f8-'])
            sag_hog_rein_ratio = float(values['-f9-'])
#             stirrups_type = float(values['-f10-'])

            stirrups_type = 0  # default value
            if values['-f10-'] == 'BFRP':
                stirrups_type = 1
            elif values['-f10-'] == 'GFRP':
                stirrups_type = 2
            elif values['-f10-'] == 'Steel':
                stirrups_type = 3

            stirrups_strength = float(values['-f11-']) if values['-f10-'] != 'None' else 0.0
            transverse_reinforcement_ratio = float(values['-f12-']) if values['-f10-'] != 'None' else 0.0


            # check if the input values are within the defined range
            if Ag < 24900 or Ag > 154530:
                sg.popup("Ag must be between 24,900 mm² and 154,530 mm².")
                continue
            if a_d < 4.669261 or a_d > 16.806723:
                sg.popup("a/d must be between 4.669261 and 16.806723.")
                continue
            if fc < 14.56 or fc > 81:
                sg.popup("Concrete compressive strength (fc) must be between 14.56 MPa and 81 MPa.")
                continue
#             if long_rein_type < 0 or long_rein_type > 4:
#                 sg.popup("Longitudinal Reinforcement type must be between 0 and 4.")
#                 continue
            if Fu_sagging < 731 or Fu_sagging > 1773:
                sg.popup("Fu sagging must be between 731 MPa and 1773 MPa.")
                continue
            if E_sagging < 42.7 or E_sagging > 137:
                sg.popup("E sagging must be between 42.7 GPa and 137 GPa.")
                continue
            if Fu_hogging < 731 or Fu_hogging > 1773:
                sg.popup("Fu hogging must be between 731 MPa and 1773 MPa.")
                continue
            if E_hogging < 42.7 or E_hogging > 137:
                sg.popup("E hogging must be between 42.7 GPa and 137 GPa.")
                continue
            if sag_hog_rein_ratio < 0.213333 or sag_hog_rein_ratio > 4.6875:
                sg.popup("Sagging/Hogging reinforcement ratio must be between 0.213333 and 4.6875.")
                continue
#             if stirrups_type < 0 or stirrups_type > 3:
#                 sg.popup("Stirrups type must be between 0 and 3.")
#                 continue
            if stirrups_strength < 0 or stirrups_strength > 1383:
                sg.popup("Stirrups strength (fy or Fu) must be between 0 MPa and 1383 MPa.")
            if transverse_reinforcement_ratio < 0 or transverse_reinforcement_ratio > 1.867116:
                sg.popup("Transverse reinforcement ratio must be between 0% and 1.867116%")
                continue

            
            # Combine the input values into a DataFrame
            df11 = np.array([[Ag, a_d, fc, long_rein_type, Fu_sagging, E_sagging, Fu_hogging, E_hogging, sag_hog_rein_ratio, stirrups_type, stirrups_strength, transverse_reinforcement_ratio]])
            df1 = pd.DataFrame(df11)

#           # normalize the user defined variables
            dfn=[]
            for i in range(0,df1.shape[1]):
#                 a = (df1.iloc[:,i]-df.iloc[:,i].min())/(df.iloc[:,i].max()-df.iloc[:,i].min())
                a = (df1.iloc[:,i][0]-df.iloc[:,i].min())/(df.iloc[:,i].max()-df.iloc[:,i].min())
                dfn.append(a)

            dfn = pd.DataFrame(np.array(dfn)).T.values           
            
            # make the prediction                   
            # Perform prediction and display results
            # Predict with the first model (XGBoost)
            m1_preds = m1.predict(dfn)

            # Calculate the residuals and predict with the second model (SVR or KNeighborsRegressor)
            residuals = m1_preds
            m2_preds = m2.predict(dfn)

            # Calculate the residuals and predict with the third model (SVR or KNeighborsRegressor)
            residuals = m1_preds + m2_preds
            m3_preds = m3.predict(dfn)

            # Combine the predictions from all three models
            hybrid_preds = m1_preds + m2_preds + m3_preds

            y_pred = hybrid_preds[0]
            
            # Inverse normalization
            # observed responses
            yy1 = df['sagging moment redistribution (%)'].values

            # predicted responses
            y1=round(yy1.min()+(yy1.max()-yy1.min()) * y_pred, 2)
            
            window['-OP-'].update(np.round(y1,2))
  
        except Exception as e:
            sg.popup(f"Error: {e}\n\nInvalid input. Please make sure to enter numeric values and make sure the input values are within the defined range.")
            continue
       
                    
            
window.close()

