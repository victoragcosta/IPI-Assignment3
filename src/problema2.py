import numpy as np
import cv2
import matplotlib.pyplot as plt
from funcoes import *

## Main ##
quant_frames = 1
Ys, Us, Vs = read_yuv('img/foreman.yuv', quant_frames, 352,288)
frame_position = 0
Y = Ys[frame_position:frame_position+1,:,:].squeeze()
U = Us[frame_position:frame_position+1,:,:].squeeze()
V = Vs[frame_position:frame_position+1,:,:].squeeze()
height, width = Y.shape
img = cvt_YUV420_BGR(Y, U, V)

cv2.imshow('Original', img)
cv2.imwrite('img/quest2_original.jpg', img)
cv2.imshow('Original Y', Y)
cv2.imwrite('img/quest2_original_Y.jpg', Y)
cv2.imshow('Original U', cv2.resize(U, None, fx=2, fy=2))
cv2.imwrite('img/quest2_original_U.jpg', cv2.resize(U, None, fx=2, fy=2))
cv2.imshow('Original V', cv2.resize(V, None, fx=2, fy=2))
cv2.imwrite('img/quest2_original_V.jpg', cv2.resize(V, None, fx=2, fy=2))

# Segmento em vários elementos
labels = segment_kmeans(Y, U, V, k=3)
# Formato o resultado para o formato da imagem e com
# a pele segmentada como 1 e o resto como 0
mask = reshape_labels(labels, (height, width))

cv2.imshow('K-means Segmentada', mask*255)
cv2.imwrite('img/quest2_segmentada.jpg', mask*255)
cv2.imshow('K-means Original Mascarada', img * mask[:,:,np.newaxis])
cv2.imwrite('img/quest2_segmentada_mascara.jpg', img * mask[:,:,np.newaxis])

smooth = smooth_segmentation_mask(mask)
cv2.imshow('K-means Segmentada suavizada', smooth*255)
cv2.imwrite('img/quest2_segmentada_suave.jpg', smooth*255)
cv2.imshow('K-means Original Mascarada suavizada', img * smooth[:,:,np.newaxis])
cv2.imwrite('img/quest2_segmentada_suave_mascara.jpg', img * smooth[:,:,np.newaxis])

cv2.waitKey(0)

cv2.destroyAllWindows()
