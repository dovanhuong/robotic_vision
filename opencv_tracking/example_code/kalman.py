#!/usr/bin/env python
"""
   Tracking of rotating point.
   Rotation speed is constant.
   Both state and measurements vectors are 1D (a point angle),
   Measurement is the real point angle + gaussian noise.
   The real and the estimated points are connected with yellow line segment,
   the real and the measured points are connected with red line segment.
   (if Kalman filter works correctly,
    the yellow segment should be shorter than the red one).
   Pressing any key (except ESC) will reset the tracking with a different speed.
   Pressing ESC will stop the program.
"""
# # Python 2/3 compatibility
# import sys
# PY3 = sys.version_info[0] == 3
#
# if PY3:
#     long = int

import cv2 as cv
from math import cos, sin, sqrt
import numpy as np


# class Kalman_filt(object):
#     """docstring for Kalman_filt."""
#     def __init__(self, arg):
#         super(Kalman_filt, self).__init__()
#         self.arg = arg
#         img_height = 500
#         img_width = 500
#         kalman = cv.KalmanFilter(2, 1, 0)
#
#         code = long(-1)
#
#         cv.namedWindow("Kalman")


if __name__ == "__main__":

    img_height = 500
    img_width = 500
    kalman = cv.KalmanFilter(2, 1, 0)

    code = long(-1)
    Ts = 1/30.0

    cv.namedWindow("Kalman")

    while True:
        state = 0.01 * np.random.randn(2, 1)

        # kalman.transitionMatrix = np.array([[1,0,1,0],
        #                                     [0,1,0,1],
        #                                     [0,0,1,0],
        #                                     [0,0,0,1]],np.float32)

        # kalman.transitionMatrix = np.array([[1., Ts], [0., 1.]])
        # kalman.measurementMatrix = np.array([[1, 0, 0, 0],
        #                                      [0, 1, 0, 0]],np.float32)

        kalman.measurementMatrix = np.array([1.0, 0.0])
        kalman.processNoiseCov = 1e2 * np.array([[1/3*Ts**3, .5*Ts**2],
                                                  [.5*Ts**2,   Ts]])
        # kalman.processNoiseCov = 1e2* np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],np.float32)
        kalman.measurementNoiseCov = 1e-5 * np.eye(2)
        kalman.errorCovPost = -1. * np.eye(4)
        kalman.statePost = 0.1 * np.random.randn(2, 1)

        while True:
            def calc_point(angle,num):
                return (np.around(img_width/2 + img_width/3*cos(angle)+num, 0).astype(int),
                        np.around(img_height/2 - img_width/3*sin(angle)-num, 1).astype(int))

            state_angle = state[0, 0]
            num = float(np.random.randn(1))*10
            state_pt = calc_point(state_angle,0)

            prediction = kalman.predict()
            predict_angle = prediction[0, 0]
            predict_pt = calc_point(predict_angle,0)

            measurement = kalman.measurementNoiseCov * np.random.randn(1, 1)

            # generate measurement
            measurement = np.dot(kalman.measurementMatrix, state) + measurement

            measurement_angle = measurement[0, 0]
            measurement_pt = calc_point(measurement_angle,0)

            # plot points
            def draw_cross(center, color, d):
                cv.line(img,
                         (center[0] - d, center[1] - d), (center[0] + d, center[1] + d),
                         color, 1, cv.LINE_AA, 0)
                cv.line(img,
                         (center[0] + d, center[1] - d), (center[0] - d, center[1] + d),
                         color, 1, cv.LINE_AA, 0)

            img = np.zeros((img_height, img_width, 3), np.uint8)
            draw_cross(np.int32(state_pt), (255, 255, 255), 3)
            draw_cross(np.int32(measurement_pt), (0, 0, 255), 3)
            draw_cross(np.int32(predict_pt), (0, 255, 0), 3)

            cv.line(img, state_pt, measurement_pt, (0, 0, 255), 3, cv.LINE_AA, 0)
            cv.line(img, state_pt, predict_pt, (0, 255, 255), 3, cv.LINE_AA, 0)

            kalman.correct(measurement)

            process_noise = sqrt(kalman.processNoiseCov[0,0]) * np.random.randn(2, 1)
            state = np.dot(kalman.transitionMatrix, state) + process_noise

            cv.imshow("Kalman", img)

            code = cv.waitKey(100)
            if code != -1:
                break

        if code in [27, ord('q'), ord('Q')]:
            break

    cv.destroyWindow("Kalman")
