# ==================================================================================================================== #
# Collaborators: Phuoc Nguyen + Tri Le
# Description: Main user interface using streamlit framework
# Filename: project_final.py
# ==================================================================================================================== #

# Dependencies
import streamlit as st
import cv2
import numpy as np
from upload_image import upload_image
from color_transfer import convert_color_space_RGB_to_BGR
from our_algorithm import landscape, portrait


def save_and_display_image(img, label, path, is_shown=False):
    """
    Function to save and display the image on the webpage.

    :param img: image
    :param label: label of image
    :param path: where to store image
    :param is_shown: whether showing image on the webpage or not
    :return: image result
    """
    image = np.array(img).astype(np.uint8)

    if is_shown:
        st.image(image, label)

    filename = path + label.strip() + ".png"

    image = convert_color_space_RGB_to_BGR(image)
    image = image.astype(np.uint8)
    cv2.imwrite(filename, image)

    return image


def gen_landscape_image(img, path):
    with st.spinner('Please waiting...'):
        img_landscape = landscape(img)
    img_landscape = save_and_display_image(
        img_landscape, "Landscape Image", path, True, True, False)
    return img_landscape


def gen_portrait_image(img, path):
    with st.spinner('Please waiting...'):
        img_portrait = portrait(img)
    img_portrait = save_and_display_image(
        img_portrait, "Portrait Image", path, True, True, False)
    return img_portrait


# ==================================================================================================================== #
# USER INTERFACE
# ==================================================================================================================== #
st.title("Real Image To Artistic Picture")
section = st.sidebar.selectbox(
    label="Choose a section:",
    options=[
        "",
        "Landscape",
        "Portrait"
    ]
)

if section == "":
    st.header("Welcome to our application!")
    st.subheader("Description:")
    st.markdown(
        'Our application is built to generate an artistic picture from a real image.')
    st.subheader("Author:")
    st.markdown('Phuoc Nguyen and Tri Le.')

elif section == "Landscape":
    # Sub header
    st.header("Artistic Landscape Picture Transformation")

    # Upload image
    original_img = upload_image(isShown=True)

    # Image processing
    if len(original_img) != 0:
        st.subheader("Result: ")
        gen_landscape_image(original_img, path="./img/result/landscape/")
        st.stop()

elif section == "Portrait":
    # Sub header
    st.header("Artistic Portrait Picture Transformation")

    # Upload image
    original_img = upload_image(isShown=True)

    # Image processing
    if len(original_img) != 0:
        st.subheader("Result: ")
        gen_portrait_image(original_img, path="./img/result/portrait/")
        st.stop()
