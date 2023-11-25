# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 19:45 2023
@author: PZB
"""

import numpy as np
from pyts.image import GramianAngularField
from pyts.image import MarkovTransitionField
from pyts.image import RecurrencePlot
import scipy.io as scio
import seaborn as sns
import matplotlib.pyplot as plt

def calculate_GAF(data, image_size, method='summation'):
    """
    :param 性能最快
    :param data: 传入numpy类型数据，格式：（n_samples, n_timestamps）
    :param method: 可选，想用GASF：summation； GADF：difference
    :return:numpy数据类型，格式：（n_samples, image_size, image_size, channels）
    """
    num_samples = data.shape[0]
    gaf_images = np.zeros((num_samples, image_size, image_size))
    for i in range(num_samples):
        print(i)
        gasf = GramianAngularField(image_size=image_size, method=method)
        gaf_images[i] = gasf.fit_transform(data[i].reshape(-1, 1).T)

    return gaf_images

def calculate_MTF(data, image_size, strategy='quantile'):
    """
    :param data:传入numpy类型数据，格式：（n_samples, n_timestamps）
    :param strategy: 可选 uniform， quantile， normal
    :return:numpy数据类型，格式：（n_samples, image_size, image_size, channels）
    """
    num_samples = data.shape[0]
    mtf_images = np.zeros((num_samples, image_size, image_size))
    for i in range(num_samples):
        print(i)
        mtf = MarkovTransitionField(image_size=image_size, strategy=strategy)
        mtf_images[i] = mtf.fit_transform(data[i].reshape(-1, 1).T)

    return mtf_images

def calculate_RP(data, image_size, time_delay=1, percentage=10):
    """
    :param data: 传入numpy类型数据，格式：（n_samples, n_timestamps）
    :param image_size = n_timestamps - demension + 1
    :param dimension: int
    :return:numpy数据类型，格式：（n_samples, image_size, image_size, channels）
    """
    num_samples = data.shape[0]
    dimension = data.shape[1] - image_size + 1
    rp_images = np.zeros((num_samples, image_size, image_size))
    rp = RecurrencePlot(dimension=dimension, time_delay=time_delay, percentage=percentage)
    for i in range(num_samples):
        print(i)
        rp_images[i] = rp.fit_transform(data[i].reshape(-1, 1).T)

    return rp_images

def calculate_RPM(data, reduction_factor=1):
    """
    :param data: numpy数据类型，格式（n_samples, n_timestamps）
    :return:
    """
    def relative_position_matrix(x, k):
        """
        :param Calculate the Relative Position Matrix (RPM)
        :param x: 输入单个时间序列，numpy形式，格式可以为（n_timestamps,）或者（n_timestamps, 1）
        :param k: image_size = n_timestamps / k    除法按照不满 1 取 1 的规则   reduction factor for Piecewise Aggregate Approximation (PAA)
        :return: RPM, Relative Position Matrix
        """
        mu = np.mean(x)
        delta = np.sqrt(np.var(x))
        z = (x - mu) / delta
        # PAA
        N = len(x)
        m = np.ceil(N / k).astype(int)
        if np.ceil(N / k) - np.floor(N / k) == 0:
            X = [np.sum(z[k * (i - 1):k * i]) / k for i in range(1, m + 1)]
        else:
            X = [np.sum(z[k * (i - 1):k * i]) / k for i in range(1, m)]
            X.append(np.sum(z[k * (m - 1):N]) / (N - k * (m - 1)))
        # Calculate relative positions between two timestamps
        M = np.outer(X, np.ones(m)) - np.outer(np.ones(m), X)
        # Relative Position Matrix (RPM)
        RPM = (M - np.min(M)) / (np.max(M) - np.min(M)) * 255
        return RPM
    image_size = data.shape[1] / reduction_factor
    if image_size % 1 == 0:
        image_size = image_size
    else:
        image_size = int(image_size) + 1
    image_size = int(image_size)
    num_samples = data.shape[0]
    rpm_images = np.zeros((num_samples, image_size, image_size))
    for i in range(data.shape[0]):
        print(i)
        rpm_images[i] = relative_position_matrix(data[i], k=reduction_factor)

    return rpm_images
