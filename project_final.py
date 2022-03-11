# ==================================================================================================================== #
# Collaborators: Phuoc Nguyen + Tri Le
# Description: Main user interface using streamlit framework
# Filename: project_final.py
# ==================================================================================================================== #

# Dependencies
import streamlit as st
import cv2
import numpy as np
from upload_image import upload_image, read_image
from filtering import bilateral_filter, median_filter, sobel_filter, gaussian_filters
from color_transfer import convert_color_space_RGB_to_GRAY, convert_color_space_RGB_to_BGR
from color_quantization import color_quantization
from our_algorithm import landscape_pictures, portrait_pictures


@st.cache(suppress_st_warning=True)
def download_image(filename):
    """
    Function helper to download the target image.

    :param filename: filename
    :return: None
    """
    with open(filename, "rb") as file:
        st.download_button(
            label="Download image",
            data=file,
            file_name=filename,
            mime="image/png"
        )


def save_and_display_image(img, label, path, is_shown=False, is_downloaded=False, is_saved=False):
    """
    Function to save and display the image on the webpage.

    :param img: image
    :param label: label of image
    :param path: where to store image
    :param is_shown: whether showing image on the webpage or not
    :param is_downloaded: whether download the image or not
    :param is_saved:
    :return: image result
    """
    image = np.array(img).astype(np.uint8)

    if is_shown:
        st.image(image, label)

    filename = path + label.strip() + ".png"

    if is_downloaded:
        image = convert_color_space_RGB_to_BGR(image)
        image = image.astype(np.uint8)
        cv2.imwrite(filename, image)
        download_image(filename)

    if is_saved:
        cv2.imwrite(filename, image)

    return image


def generate_image(img_RGB, path, is_shown=False, is_saved=False):
    """
    Function helper to generate the final image from the original image.

    :param img_RGB: original image
    :param path: where to store image
    :param is_shown: whether showing image or not
    :param is_saved:
    :return: image result
    """
    if len(img_RGB) != 0:
        # Gray scale
        with st.spinner('Please waiting...'):
            gray_img = convert_color_space_RGB_to_GRAY(img_RGB)
        gray_img = save_and_display_image(gray_img, "Gray scale", path, is_shown, False, is_saved)

        # Median blur
        with st.spinner('Please waiting...'):
            img_median = median_filter(gray_img, 5)
        img_median = save_and_display_image(img_median, "Median Blur with kernel (5x5)", path, is_shown, False,
                                            is_saved)

        # Sobel
        with st.spinner('Please waiting...'):
            img_sobel = sobel_filter(img_median)
        img_sobel = save_and_display_image(img_sobel, "Sobel Edge Detection 1", path, is_shown, False, is_saved)

        with st.spinner('Please waiting...'):
            img_sobel2 = cv2.bitwise_not(img_sobel)
        img_sobel2 = save_and_display_image(img_sobel2, "Sobel Edge Detection 2", path, is_shown, False, is_saved)

        # Remove noise
        with st.spinner('Please waiting...'):
            img_bilateral = bilateral_filter(img_RGB, 30, 0.1, 1)
        img_bilateral = save_and_display_image(img_bilateral, "Bilateral Blurring", path, is_shown, False, is_saved)

        # Color quantization
        with st.spinner('Please waiting...'):
            img_quantization = color_quantization(img_bilateral, 5)
        img_quantization = save_and_display_image(img_quantization, "Color Quantization", path, is_shown, False,
                                                  is_saved)

        with st.spinner('Please waiting...'):
            final_img = cv2.bitwise_and(img_quantization, img_quantization, mask=img_sobel2)
        final_img = save_and_display_image(final_img, "Final", path, True, True, is_saved)
        return final_img
    return np.array(([]))


def generate_example_image(img_RGB):
    """
    Function to generate the example demo step by step.

    :param img_RGB: original image
    :return: image
    """
    final_img = generate_image(img_RGB, path="./img/result/example/", is_shown=True, is_saved=True)
    return final_img


def customize_image(img_RGB, is_shown=True):
    """
    Function helper to customize the final image from the original image.

    :param img_RGB: original image
    :param is_shown: whether showing image or not
    :return: image result
    """
    # Initialize path, which is where we going to store the image result
    path = "./img/result/customize/"

    if len(img_RGB) != 0:
        # Gray scale
        with st.spinner('Please waiting...'):
            gray_img = convert_color_space_RGB_to_GRAY(img_RGB)
        gray_img = save_and_display_image(gray_img, "Gray scale", path, is_shown, False, False)

        # ------------------------------------------------------------------------------------- #
        # Choose blur algorithm
        # ------------------------------------------------------------------------------------- #
        # Select the algorithm to style the image
        blur_option = st.selectbox(
            label='What algorithm would you like to choose?',
            options=(
                'None',
                'Median',
                'Gaussian',
                'Bilateral')
        )

        image_blur = gray_img
        # Median blur
        if blur_option == 'Median':
            with st.spinner('Please waiting...'):
                img_median = median_filter(gray_img, 5)
            image_blur = save_and_display_image(img_median, "Median Blurring with kernel (5x5)", path, is_shown, False)
        elif blur_option == 'Gaussian':
            with st.spinner('Please waiting...'):
                img_gaussian = gaussian_filters(gray_img, 5)
            image_blur = save_and_display_image(img_gaussian, "Median Blurring with kernel (5x5)", path, is_shown,
                                                False)

        # Sobel
        with st.spinner('Please waiting...'):
            img_sobel = sobel_filter(img_median)
        img_sobel = save_and_display_image(img_sobel, "Sobel Edge Detection 1", path, is_shown, False)

    return np.array(([]))


def gen_landscape_image(img, path):
    with st.spinner('Please waiting...'):
        img_landscape = landscape_pictures(img)
    img_landscape = save_and_display_image(img_landscape, "Landscape Image", path, True, True, False)
    return img_landscape


def gen_portrait_image(img, path):
    with st.spinner('Please waiting...'):
        img_portrait = portrait_pictures(img)
    img_portrait = save_and_display_image(img_portrait, "Portrait Image", path, True, True, False)
    return img_portrait


# ==================================================================================================================== #
# USER INTERFACE
# ==================================================================================================================== #
st.title("Real Image To Artistic Picture")
section = st.sidebar.selectbox(
    label="Choose a section:",
    options=[
        "",
        "Customize",
        "Landscape",
        "Portrait",
        "Example"
    ]
)

if section == "":
    st.header("Welcome to our application!")
    st.subheader("Description:")
    st.markdown('Our application is built to generate an artistic picture from a real image.')
    st.subheader("Author:")
    st.markdown('Phuoc Nguyen and Tri Le.')

if section == "Example":
    # Upload image
    original_img = read_image("./img/src/christopher.jpg")
    generate_example_image(original_img)
    st.stop()

elif section == "Customize":
    # Upload image
    original_img = upload_image(isShown=True)
    customize_image(original_img)
    st.stop()

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
