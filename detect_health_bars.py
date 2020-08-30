import numpy as np
import os
import skimage.io as io
import cv2

from detect_spaces import detect_spaces
from detect_edges import detect_edges

def detect_health_bars(input_image):
    edges = detect_edges(input_image)
    spaces = []
    indicies = detect_spaces(edges, offset=3, pixels=3, min_len_bright=50, min_len_dark=5, axis=0)

    for item in indicies:
        indicies2 = detect_spaces(edges[:, item[0]:item[1]], offset=3, pixels=3, min_len_bright=10, min_len_dark=3, axis=1)
        spaces.extend([(item2[0], item2[1], item[0], item[1]) for item2 in indicies2])
    spaces2 = []

    for space in spaces:
        indicies = detect_spaces(edges[space[0]:space[1], space[2]:space[3]], offset=3, pixels=3, min_len_bright=50, min_len_dark=5, axis=0)
        spaces2.extend([(space[0], space[1], space[2] + item[0], space[2] + item[1]) for item in indicies])
    # #here you can check where were spaces detected:
    # import matplotlib.patches as patches
    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots(1,figsize=(16,16))
    # ax.imshow(edges, cmap='gray')
    #
    # for space in spaces2:
    #     rect = patches.Rectangle((space[2], space[0]), space[3] - space[2], space[1] - space[0],linewidth=1,edgecolor='r',facecolor='none')
    #     ax.add_patch(rect)
    # plt.show()

    #load health bar image
    data_path = os.path.join(os.path.abspath(os.getcwd()), 'data')
    bar_path = os.path.join(data_path, 'perfect_bar.png')
    bar_image = cv2.imread(bar_path)
    bar_image = cv2.cvtColor(bar_image, cv2.COLOR_BGR2GRAY)

    #load important pixels form health bar
    pixels_path = os.path.join(data_path, 'pixels_horiz.txt')
    with open(pixels_path) as f:
        pixels_horiz = []
        for line in f:
            indicies = line.strip().split()
            pixels_horiz.append((int(indicies[0]), int(indicies[1])))
    pixels_path = os.path.join(data_path, 'pixels_vert.txt')
    with open(pixels_path) as f:
        pixels_vert = []
        for line in f:
            indicies = line.strip().split()
            pixels_vert.append((int(indicies[0]), int(indicies[1])))

    y, x = bar_image.shape
    minim_width = 15
    minim_length = 70
    pixel_threshold = 3
    threshold_vert = 0.41
    threshold_horiz = 0.41
    #vector containing down-left corners of possible health bars
    poss_bars = []
    for space in spaces2:
        y1 = space[0]
        y2 = space[1]
        x1 = space[2]
        x2 = space[3]
        #check if the image isn't too short
        if y2 - y1 < y:
            y1 = y1 - ((y - y2 + y1)//2 + 1)
            y2 = y2 + ((y - y2 + y1)//2 + 1)
            if y1 < 0:
                y2 = min(y2 + abs(y1), input_image.shape[0] - 1)
                y1 = 0
            if y2 > input_image.shape[0] - 1:
                y1 = max(y1 - abs(input_image.shape[0] - 1 - y2), 0)
                y2 = input_image.shape[0] - 1
        if x2 - x1 < x:
            x1 = x1 - ((x - x2 + x1)//2 + 1)
            x2 = x2 + ((x - x2 + x1)//2 + 1)
            if x1 < 0:
                x2 = min(x2 + abs(x1), input_image.shape[1] - 1)
                x1 = 0
            if x2 > input_image.shape[1] - 1:
                x1 = max(x1 - abs(input_image.shape[1] - 1 - x2), 0)
                x2 = input_image.shape[1] - 1
        #check if the image is on the border
        image2check = input_image[y1:y2, x1:x2]
        if y1 == 0:
            temp_image = np.zeros((image2check.shape[0] + minim_width, image2check.shape[1]))
            temp_image[minim_width:, :] = image2check
            image2check = temp_image
        if y2 == input_image.shape[0]:
            temp_image = np.zeros((image2check.shape[0] + minim_width, image2check.shape[1]))
            temp_image[:-minim_width, :] = image2check
            image2check = temp_image
        if x1 == 0:
            temp_image = np.zeros((image2check.shape[0], image2check.shape[1] + minim_length))
            temp_image[:, minim_length:] = image2check
            image2check = temp_image
        if x2 == input_image.shape[1]:
            temp_image = np.zeros((image2check.shape[0], image2check.shape[1] + minim_length))
            temp_image[:, :-minim_length] = image2check
            image2check = temp_image
        #check spaces
        for i in range(image2check.shape[0] - y):
            for j in range(image2check.shape[1] - x):
                part_image = image2check[i:i+y, j:j+x]
                if sum([1 for pixel in pixels_vert if np.abs(int(part_image[pixel]) - int(bar_image[pixel])) <= pixel_threshold])/len(pixels_vert) >= threshold_vert:
                    if sum([1 for pixel in pixels_horiz if np.abs(int(part_image[pixel]) - int(bar_image[pixel])) <= pixel_threshold])/len(pixels_horiz) >= threshold_horiz:
                        poss_bars.append((y2 - image2check.shape[0] + i + y, x2 - image2check.shape[1] + j + x))
    return poss_bars
