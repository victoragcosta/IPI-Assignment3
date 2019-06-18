import numpy as np
import cv2
import matplotlib.pyplot as plt
# from src.funcoes import *
from funcoes import *

## Main ##
fig, axes = plt.subplots(1, 2)
img = cv2.imread('img/img_cells.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imshow('Original', img)

# Binarize
_, binary = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY)
cv2.imshow('Binarizada', binary)

# Preenche espaços desconectados
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
processed = cv2.morphologyEx(binary, cv2.MORPH_ERODE, kernel)
# processed = binary.copy()
cv2.imshow('Apos morfologia', processed)

# Preencher buracos
height, width = processed.shape[:2]
mask = np.zeros((height+2, width+2), dtype=np.uint8)
_, holes, *_ = cv2.floodFill(255-processed, mask, (height-1,width-1), (255,255,255))
unholed = processed & holes
cv2.imshow('Desburacada', unholed)

# Calcular função distância
dist = cv2.distanceTransform(255-unholed, cv2.DIST_L2, 3)
dist = np.uint8(255*(cv2.normalize(dist, None, 0.0, 1.0, cv2.NORM_MINMAX)))
cv2.imshow('Distance Transform', dist)

_, peaks = cv2.threshold(dist, 255-110, 255, cv2.THRESH_BINARY)
cv2.imshow('Picos', peaks)

cells = peaks + unholed
cv2.imshow('Celulas', cells)

# Achar marcadores
contours, _ = cv2.findContours(peaks, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours2, _ = cv2.findContours(unholed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Cria imagem de marcadores
markers = np.zeros(dist.shape, dtype=np.int32)
# Desenha os marcadores
for i in range(len(contours+contours2)):
  cv2.drawContours(markers, contours, i, (i+1), -1)
axes[0].imshow(markers)

# Computar watershed
water = cv2.watershed(np.repeat(img[:,:,np.newaxis], 3, axis=2), markers)
axes[1].imshow(water)

plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()
