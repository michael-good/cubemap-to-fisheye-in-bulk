#!/usr/bin python3
# -*- coding: utf-8 -*-

"""

@author: michael-good

"""

import cv2

import time

from tqdm import tqdm

from cubemap2fisheye import *


# -------------------------   Constants to define   --------------------------#

NUMBER_OF_FRAMES = 1
WINDOW_SIZE = 1
FACE_SIZE = 1024
FOV = 196  # degrees
output_width = 1344
output_height = 1344


# ----------------------------------------------------------------------------#

def load_images(pointer):
    """
    Loads input images from the path specified and creates a list of
    cubemaps generated with the imported images.
    :param pointer: indicates the position of the window
    :return: A list of cubemaps.
    """

    print('\nGenerating cubemaps...\n')

    cubemap = []

    for i in tqdm(range(WINDOW_SIZE)):

        output_image = np.zeros((3072, 4096, 3))
        zero_string = '0'

        if i + pointer < 10:
            zero_string = 5 * '0'
        elif 10 <= i + pointer < 100:
            zero_string = 4 * '0'
        elif 100 <= i + pointer < 1000:
            zero_string = 3 * '0'
        elif 1000 <= i + pointer < 10000:
            zero_string = 2 * '0'

        front = cv2.imread('./input/front/' + zero_string + str(pointer + i) + '.png')
        left = cv2.imread('./input/left/' + zero_string + str(pointer + i) + '.png')
        right = cv2.imread('./input/right/' + zero_string + str(pointer + i) + '.png')
        top = cv2.imread('./input/top/' + zero_string + str(pointer + i) + '.png')
        bottom = cv2.imread('./input/bottom/' + zero_string + str(pointer + i) + '.png')
        back = cv2.imread('./input/back/' + zero_string + str(pointer + i) + '.png')

        if not(front is None):

            h = front.shape[0]
            w = front.shape[1]

            output_image[h:h + h, 0:w] = left
            output_image[h:h + h, w:w + w] = front
            output_image[h:h + h, 2 * w:2 * w + w] = right
            output_image[0:h, w:w + w] = top
            output_image[2 * h:2 * h + h, w:w + w] = bottom

            try:
                output_image[1024:1024 + h, 3072:3072 + w] = \
                    back
            except NameError:
                output_image[1024:1024 + h, 3072:3072 + w] = \
                    np.zeros((h, w, 3))

            cv2.imwrite('./cubemaps/frame' +
                        str(i) + '.png', output_image)

            cubemap.append(output_image)

    return cubemap


def main():
    """
    main function
    """

    cubemap_to_fisheye()

    elapsed_time = time.time() - start_time

    print('\nElapsed time: ', elapsed_time, ' seconds')


def cubemap_to_fisheye():
    """
    Converts loaded cube maps into fisheye images
    """

    # Create new output image with the dimentions computed above
    output_image = np.zeros((output_height, output_width, 3))
    fov = FOV * np.pi / 180

    # counter allows for correct naming when cropping
    pointer = 0

    r, phi = get_spherical_coordinates(output_height, output_width)
    x, y, z = spherical_to_cartesian(r, phi, fov)

    number_of_frames = 0

    while number_of_frames < NUMBER_OF_FRAMES:
        cubemap = load_images(pointer)
        print('\nCubemaps successfully loaded...\n')
        for image in tqdm(cubemap):
            for row in range(0, output_height):
                for column in range(0, output_width):
                    if np.isnan(r[row, column]):

                        output_image[row, column, 0] = 0
                        output_image[row, column, 1] = 0
                        output_image[row, column, 2] = 0

                    else:
                        face = get_face(x[row, column],
                                        y[row, column],
                                        z[row, column])
                        u, v = raw_face_coordinates(face,
                                                    x[row, column],
                                                    y[row, column],
                                                    z[row, column])
                        xn, yn = normalized_coordinates(face,
                                                        u,
                                                        v,
                                                        FACE_SIZE)

                        output_image[row, column, 0] = image[yn, xn, 0]
                        output_image[row, column, 1] = image[yn, xn, 1]
                        output_image[row, column, 2] = image[yn, xn, 2]

            cv2.imwrite('./output/frame' +
                        str(number_of_frames) +
                        '.png', output_image)

            number_of_frames += 1
        pointer += WINDOW_SIZE
    return


if __name__ == "__main__":
    start_time = time.time()
    main()
