import numpy as np
import cv2
import matplotlib.pyplot as plt
# from src.funcoes import *
from funcoes import *
# import funcoes

## Main ##
Ys, Us, Vs = read_yuv('img/foreman.yuv', 2, 352,288)

frame1 = {
  'Y':Ys[0:1,:,:].squeeze(),
  'U':Us[0:1,:,:].squeeze(),
  'V':Vs[0:1,:,:].squeeze(),
}
frame2 = {
  'Y':Ys[1:2,:,:].squeeze(),
  'U':Us[1:2,:,:].squeeze(),
  'V':Vs[1:2,:,:].squeeze(),
}
cv2.imshow('frame1', frame1['Y'])
cv2.imshow('frame2', frame2['Y'])



cv2.waitKey(0)
cv2.destroyAllWindows()
