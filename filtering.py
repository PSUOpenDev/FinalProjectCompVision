import numpy as np
import math

# use opencv for image loading
import cv2
import numpy as np
import cv2
from multiprocessing import Pool
import timeit
import os
import pickle

MAX_PROCESS_NUM = 6
EPSILON=1e-8


# Gaussian Filtering
def GaussianFunction(x, y, std_dev):
    return (1 / (2 * np.pi * std_dev ** 2)) * np.exp(-(x ** 2 + y ** 2) / (2 * std_dev ** 2))


def GaussianFiltering(img, std_dev, kernel_size):
    h = img.shape[0]
    w = img.shape[1]

    img_pad = np.pad(
        img,
        (math.floor(kernel_size / 2), math.floor(kernel_size / 2)),
        'constant'
    )

    kernel = np.zeros((kernel_size, kernel_size), dtype=np.float)

    for c in range(0, kernel_size):
        for r in range(0, kernel_size):
            gx = c - math.floor(kernel_size / 2)
            gy = r - math.floor(kernel_size / 2)
            kernel[r, c] = GaussianFunction(gx, gy, std_dev)

    sum_kernel = kernel.sum()
    kernel = np.divide(kernel, sum_kernel)

    for row in range(0, h):
        for col in range(0, w):
            img[row, col] = np.sum(
                img_pad[row: row + kernel_size, col: col + kernel_size] * kernel)
    return img


# MEDIAN FILTERING
def MedianFiltering(img, kernel_size):
    output_img = np.zeros_like(img)
    edge = math.floor(kernel_size / 2)

    for x in range(edge, img.shape[0] - edge):
        for y in range(edge, img.shape[1] - edge):
            mask_img = img[x - edge: x + edge + 1, y - edge: y + edge + 1]
            median = np.sort(np.ravel(mask_img))
            output_img[x, y] = median[int(kernel_size * kernel_size / 2)]

    return output_img


'''
bilateral_filter
'''
def run_bilateral_filter(start_col, end_col, window_width, thread_id, input_image, sigma_space, sigma_intensity):
    def gaussian_kernel(r2, sigma): return (
        np.exp(-0.5*r2/sigma**2)*3).astype(int)*1.0/3.0

    sum_fr = np.ones(input_image.shape)*EPSILON
    sum_gs_fr = input_image*EPSILON

    for w_col in range(start_col, end_col):
        for w_row in range(-window_width, window_width+1):

            gs = gaussian_kernel(w_col**2+w_row**2, sigma_space)

            w_image = np.roll(input_image, [w_row, w_col], axis=[0, 1])

            fr = gs*gaussian_kernel((w_image-input_image)**2, sigma_intensity)

            sum_gs_fr += w_image*fr
            sum_fr += fr

    pickle.dump(sum_fr, open('./sum_fr{0}.tmp'.format(thread_id), 'wb'),
                pickle.HIGHEST_PROTOCOL)
    pickle.dump(sum_gs_fr, open('./sum_gs_fr{0}.tmp'.format(thread_id), 'wb'),
                pickle.HIGHEST_PROTOCOL)


def bilateral_filter(input_image, sigma_space=10.0, sigma_intensity=0.1, radius_window_width=1):
    
    responses = []

    pool = Pool(processes=MAX_PROCESS_NUM)

    windows_width = 2*radius_window_width + 1
    total_window_length = 2*windows_width+1

    rows_every_workers = total_window_length // MAX_PROCESS_NUM
    start_row = -windows_width
    end_row = start_row + rows_every_workers

    data = input_image.astype(np.float32)/255.0

    for r in range(0, MAX_PROCESS_NUM):
        args = (start_row, end_row, windows_width, r,
                data, sigma_space, sigma_intensity)
        res = pool.apply_async(run_bilateral_filter, args)

        responses.append(res)

        start_row += rows_every_workers

        if r == MAX_PROCESS_NUM - 2:
            end_row = windows_width+1
        else:
            end_row += rows_every_workers

    for res in responses:
        res.wait()

    sum_fr = None
    sum_gs_fr = None
    for thread_id in range(0, MAX_PROCESS_NUM):

        if thread_id == 0:
            sum_fr = pickle.load(
                open('./sum_fr{0}.tmp'.format(thread_id), "rb"))
        else:
            sum_fr += pickle.load(open('./sum_fr{}.tmp'.format(thread_id), "rb"))

        if thread_id == 0:
            sum_gs_fr = pickle.load(
                open('./sum_gs_fr{0}.tmp'.format(thread_id), "rb"))
        else:
            sum_gs_fr += pickle.load(
                open('./sum_gs_fr{}.tmp'.format(thread_id), "rb"))

        os.remove('./sum_fr{0}.tmp'.format(thread_id))
        os.remove('./sum_gs_fr{0}.tmp'.format(thread_id))

    sum_gs_fr = sum_gs_fr/sum_fr

    return sum_gs_fr*255.0

'''
end bilateral filter
'''