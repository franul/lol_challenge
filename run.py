#!/usr/bin/env python3

from pathlib import Path
from sys import argv, stderr
import skimage.io as io
from detect_health_bars import detect_health_bars
import matplotlib.pyplot as plt
import cv2

if __name__ == '__main__':
    image_path = Path(argv[1])

    if not image_path.exists():
        print(f'{image_path} does not exist!', file=stderr)
        exit(-1)

    img = io.imread(image_path, as_gray=False)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    poss_bars = detect_health_bars(img)
    # print(poss_bars)
    print(len(poss_bars))
