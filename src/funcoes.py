import numpy as np
import cv2
import matplotlib.pyplot as plt
import struct

def read_yuv(name, frames, width, height):
  Ys = []
  Us = []
  Vs = []
  with open(name, 'rb') as arq:
    for i in range(frames):
      # Leio 1 frame inteiro, sendo height*width da componente Y e height/2*width/2 para U e V
      # obtendo-se (1+0.25+0.25)*height*width = 1.5*height*width
      byte_data = [el[0] for el in struct.iter_unpack('B', arq.read(int(1.5 * width * height)))]
      # Converto cada pedaço em uma matriz numpy de bytes
      Y = np.reshape(np.asarray(byte_data[:height*width], dtype=np.uint8), (height, width))
      U = np.reshape(np.asarray(byte_data[height*width:int(1.25*height*width)], dtype=np.uint8), (int(height/2), int(width/2)))
      V = np.reshape(np.asarray(byte_data[int(1.25*height*width):], dtype=np.uint8), (int(height/2), int(width/2)))
      Ys.append(Y)
      Us.append(U)
      Vs.append(V)
  return (np.asarray(Ys), np.asarray(Us), np.asarray(Vs))

def cvt_YUV420_BGR(Y, U, V):
  img = join_YUV420(Y, U, V)
  img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR)
  return img

def join_YUV420(Y, U, V):
  height, width = Y.shape
  img = np.zeros((height, width, 3), dtype=np.uint8)
  img[:,:,0:1] = Y[:,:,np.newaxis]
  img[:,:,1:2] = cv2.resize(U, None, fx=2, fy=2)[:,:,np.newaxis]
  img[:,:,2:3] = cv2.resize(V, None, fx=2, fy=2)[:,:,np.newaxis]
  return img

def segment_kmeans(Y, U, V, k=2):
  # Defino os critérios máximo de iterações = 10 e epsilon = 1.0
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
  flags = cv2.KMEANS_RANDOM_CENTERS
  # Transformo as 3 componentes do frame em uma imagem só YUV
  Z = join_YUV420(Y, U, V)
  # Retiro somente as crominâncias
  Z = Z[:,:,1:3]
  # Transformo a matriz em um vetor 1D com os canais U e V separados
  Z = Z.reshape((-1, 2))
  # Converto para float32
  Z = np.float32(Z)
  # Realizo Kmeans a partir das componentes U e V
  _,labels,_ = cv2.kmeans(Z,k,None,criteria,10,flags)
  return labels

def smooth_segmentation_mask(mask, debug=False):
  if debug:
    cv2.imshow('K-means mask', mask*255)
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
  mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
  mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
  if debug:
    cv2.imshow('K-means mask after morph 1', mask*255)
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
  mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
  mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
  if debug:
    cv2.imshow('K-means mask after morph 2', mask*255)
  return mask

def reshape_labels(labels, shape):
  height, width = shape
  # Transformo o vetor 1D numa matriz do formato da imagem
  reshaped = np.uint8(labels.reshape(shape))
  # Pixel do meio da tela é pele, pego label dele para separar as segmentações melhor
  func = lambda el: 1 if reshaped.item((height//2, width//2)) == el else 0
  # Aplico a função
  processed = np.vectorize(func)(reshaped)
  # Trasformo em bytes para não ter problemas de formatos
  processed = np.uint8(processed)
  return processed
