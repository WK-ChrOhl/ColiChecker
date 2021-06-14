# ==========================================================================================================================================================#
#                                                   colorExtraction.py 
#                             file for analysing images from the image_2_rois directory looking for a certain color
# ==========================================================================================================================================================#
# State: working
# TODO: need to check for optimal color for 'images' and maybe code clean up

# ==========================================================================
#   Imports
# ==========================================================================
import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt

import utils as xct

from PIL import Image
from collections import Counter
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, deltaE_cie76

# ==========================================================================
#   Setup
# ==========================================================================
COLORS = { # Source: http://www.workwithcolor.com/cyan-color-hue-range-01.htm
        'Test': [200,213,48],
        'Bubbles': [231,254,255],
        'Cyan': [0,255,255],
        'Columbia Blue': [155,221,255],
        'Bright Turquoise': [8,232,222],
        'Baby Blue': [137,207,240],
        'Sky Blue': [135,206,235],
        'Pastel Blue': [174,198,207],
        'Turquoise': [48,213,200],
        'Dark Cyan': [0,139,139],
        'Cerulean': [0,123,167],
        'Teal': [0,128,128],
        'Pine Green': [1,121,111],
        'Dark Slate Gray': [47,79,79],					
         }

IMAGE_DIRECTORY_ROI = glob.glob(xct.path_folder_roi+"/*.jpeg") # create list based on image names --> strings
IMAGE_DIRECTORY_ROI.sort()         # sort list
images_roi = [cv2.imread(img) for img in IMAGE_DIRECTORY_ROI] # create additional list for storing images --> ndarrays
images_roi = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in images_roi] # convert from bgr back to rgb

# ==========================================================================
#   Main
# ==========================================================================
def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def get_colors(image, number_of_colors, show_chart):
    
    modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
    
    clf = KMeans(n_clusters = number_of_colors)
    labels = clf.fit_predict(modified_image)
    
    counts = Counter(labels)
    # sort to ensure correct color percentage
    counts = dict(sorted(counts.items())) 
    
    center_colors = clf.cluster_centers_
    # get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]

    if (show_chart):
        plt.figure(figsize = (8, 6))
        plt.pie(counts.values(), labels = hex_colors, colors = hex_colors)
        plt.show()

    return rgb_colors

def match_image_by_color(image, color, threshold, number_of_colors ): 
    
    image_colors = get_colors(image, number_of_colors, False)
    selected_color = rgb2lab(np.uint8(np.asarray([[color]])))

    select_image = False
    for i in range(number_of_colors):
        curr_color = rgb2lab(np.uint8(np.asarray([[image_colors[i]]])))
        diff = deltaE_cie76(selected_color, curr_color)
        if (diff < threshold):
            select_image = True
    
    return select_image

def show_selected_images(images, color, threshold, colors_to_match, IMAGE_DIRECTORY_ROI):
    
    for i in range(len(images)):
        selected = match_image_by_color(images[i],
                                        color,
                                        threshold,
                                        colors_to_match)
        if (selected):
            # ============================
            #   Get and Print Image Name
            # ============================
            with Image.open(IMAGE_DIRECTORY_ROI) as img:
                print("Sample: {}\n Result: EXPOSED\n" .format(img.filename))

            # ============================
            #   Output Exposed Image
            # ============================
            #images[i] = cv2.cvtColor(images[i],cv2.COLOR_BGR2RGB) # convert again to RGB Color Model because OpenCV uses BGR as Default Model
            #cv2.imshow("Exposed Sample: ",images[i])
            #cv2.waitKey(0)

        else:
            # ============================
            #   Get and Print Image Name
            # ============================
            with Image.open(IMAGE_DIRECTORY_ROI) as img:
                print("Sample: {}\n Result: CLEAN\n" .format(img.filename))

            
if __name__ == '__main__':
    print ("\nRunning colorExraction.py ...")
else:
    print ("\nImporting colorExraction.py ...")