import cv2
import numpy as np

def preprocess_for_gray_channel(img):
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    target_shape = (64, 256)

    # Resize and convert to array
    resized_image = cv2.resize(img, (target_shape[1], target_shape[0]))
    rotated_image = cv2.rotate(resized_image, cv2.ROTATE_90_CLOCKWISE)
    image_arr = np.array(rotated_image).reshape(-1,256,64,1)
    image_arr = image_arr/255

    return image_arr

def preprocess_for_rgb_channel(img):
    
    target_shape = (32, 128)

    # Resize and convert to array
    resized_image = cv2.resize(img, (target_shape[1], target_shape[0]))
    rotated_image = cv2.rotate(resized_image, cv2.ROTATE_90_CLOCKWISE)
    image_arr = np.array(rotated_image).reshape(-1,128,32,3)
    image_arr = image_arr/255

    return image_arr