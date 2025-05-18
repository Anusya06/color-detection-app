import numpy as np
import pandas as pd

def get_closest_color_name(R, G, B, df):
    diff = np.abs(df[['R', 'G', 'B']] - np.array([R, G, B])).sum(axis=1)
    return df.loc[diff.idxmin(), 'color_name']

def simulate_color_blindness(img, mode='deuteranopia'):
    if mode == 'deuteranopia':
        matrix = np.array([[0.625, 0.375, 0], [0.7, 0.3, 0], [0, 0.3, 0.7]])
    elif mode == 'protanopia':
        matrix = np.array([[0.567, 0.433, 0], [0.558, 0.442, 0], [0, 0.242, 0.758]])
    else:
        return img
    img = np.dot(img[..., :3], matrix.T)
    return np.clip(img, 0, 255).astype('uint8')
