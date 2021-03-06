# ==================================================================================================================== #
# Collaborators: Phuoc Nguyen + Tri Le
# Description: This file includes the function to upload the image from devices to webpage
# Filename: upload_image.py
# ==================================================================================================================== #

# Dependencies
import os
import streamlit as st
import cv2
from PIL import Image
import numpy as np
from color_transfer import convert_color_space_BGR_to_RGB


def upload_image(isShown=False):
    """
    Function to upload the image from computer/device

    :param isShown: Whether showing the image on the web page or not. Default: False
    :return: original image under numpy format
    """
    # Set original image to None
    original_img = []

    # Image extension file allowed
    extension_allowed = ['png', 'jpg', 'jpeg', 'svg']

    # Upload a file from user's computer/device
    uploaded_img = st.file_uploader(
        label="Upload Image",
        type=extension_allowed,
        accept_multiple_files=False,
    )

    # Image uploaded already?
    if uploaded_img is not None:
        # Open uploaded image
        pil_image = Image.open(uploaded_img)

        # Size of image
        w, h = pil_image.size

        # Resize Image
        stopped = True
        scale_img = w / h

        while stopped:
            if w <= 500 and h <= 500:
                stopped = False
            else:
                if w > 500:
                    w = 500
                    h = w * (1 / scale_img)

                if h > 500:
                    h = 500
                    w = h * scale_img

        ret_img = pil_image.resize((int(w), int(h)))

        # Show the image in the web page
        if isShown:
            st.subheader("Original Image:")
            st.image(image=ret_img, caption="Original Image")

        # Convert image into numpy
        # original_img = np.array(pil_image)
        original_img = np.array(ret_img)

    return original_img


def read_image(filename):
    """
    Function to read the image.

    :param filename: filename
    :return: image
    """
    result = []

    if os.path.isfile(filename):
        # Read file using OpenCV
        img = cv2.imread(filename)

        # Convert color from BGR to RGB
        img_RGB = convert_color_space_BGR_to_RGB(img)
        img_RGB = np.array(img_RGB).astype(np.uint8)

        # Showing the image
        st.image(image=img_RGB, caption="Original Image")

        return img_RGB

    else:
        # File not found
        st.warning("File Not Found!")
    return np.array(result)
