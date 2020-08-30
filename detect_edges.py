import cv2
import numpy as np


def detect_edges(input_image, kernel_size_laplacian=5, minvalue=10, maxvalue=80, laplacian_thr=21, edge_thr=10):

# img = images_gray[1]
    img = cv2.bitwise_not(input_image)
    img = cv2.GaussianBlur(img,(3,3),0)
    #laplacian
    laplacian = cv2.Laplacian(img, cv2.CV_64F, ksize=kernel_size_laplacian)
    laplacian = ((laplacian - laplacian.min()) * (1/(laplacian.max() - laplacian.min()) * 255))
    laplacian = np.clip(laplacian - 128, 0, 255)
    laplacian = np.where(laplacian>laplacian_thr, 255, laplacian).astype('uint8')

    edges = cv2.Canny(laplacian, minvalue, maxvalue)
    edges = ((edges - edges.min()) * (1/(edges.max() - edges.min()) * 255))
    edges = np.where(edges>edge_thr, 255, 0).astype('uint8')
    #deleting map and replay hud
    edges[802:, 1642:] = np.zeros(edges[802:, 1642:].shape)
    edges[960:, :308] = np.zeros(edges[960:, :308].shape)
    edges[1005:, 605:1335] = np.zeros(edges[1005:, 605:1335].shape)
    return edges
