# -*- coding: utf-8 -*-
"""
@author:Wen
"""
import torch as t
import math
import numpy as np
import cv2
class PrepareSTN(object):
    def __init__(self,size,K ,z ,roll,pitch,yaw ,back):
        """
        :param size: tensor
        :param K: np.matrix()
        :param z: int
        :param roll: int
        :param pitch: int
        :param yaw: int
        """
        self.__size  = size
        self.__K = K
        self.__roll = roll
        self.__pitch = pitch
        self.__yaw = yaw
        self.__z = z
        self.back = back
    def MakeGrid(self):
        N, C, H, W = self.__size
        HomogeneousMatrix =t.from_numpy( self.MakeHomogeneous() ).view(1,3,3).expand(N,3,3).float()
        base_grid = HomogeneousMatrix.new(N, H, W, 3)
        linear_points = t.linspace(0, W - 1, W) if W > 1 else t.Tensor([-1])
        base_grid[:, :, :, 0] = t.ger(t.ones(H), linear_points).expand_as(base_grid[:, :, :, 0])
        linear_points = t.linspace(0, H - 1, H) if H > 1 else t.Tensor([-1])
        base_grid[:, :, :, 1] = t.ger(linear_points, t.ones(W)).expand_as(base_grid[:, :, :, 1])
        base_grid[:, :, :, 2] = 1
        grid = t.bmm(base_grid.view(N, H * W, 3), HomogeneousMatrix)
        grid = grid.view(N, H, W, 3)
        grid2dim = grid[:, :, :, 0:2].contiguous()
        grid3dim = grid[:, :, :, 2].contiguous().view(N, H, W, 1).expand_as(grid2dim)
        a = t.tensor([10,20]).float()
        grid = (grid2dim / grid3dim) / t.tensor([W / 2, H / 2],dtype = t.float32).float()- 1
        return grid
    def MakeRotationMatrix (self):
        rollMatrix = np.matrix([
            [1, 0, 0],
            [0, math.cos(self.__roll), -math.sin(self.__roll)],
            [0, math.sin(self.__roll), math.cos(self.__roll)]])

        pitchMatrix = np.matrix([
            [math.cos(self.__pitch), 0, math.sin(self.__pitch)],
            [0, 1, 0],
            [-math.sin(self.__pitch), 0, math.cos(self.__pitch)]])

        yawMatrix = np.matrix([
            [math.cos(self.__yaw), -math.sin(self.__yaw), 0],
            [math.sin(self.__yaw), math.cos(self.__yaw), 0],
            [0, 0, 1]])
        R =  pitchMatrix * rollMatrix * yawMatrix
        return R
    def MakeHomogeneous(self):
        u0 = self.__K[0,2]
        v0 = self.__K[1,2]
        fx = self.__K[0,0]
        fy = self.__K[1,1]
        roll = self.__roll
        pitch = self.__pitch
        yaw = self.__yaw
        R = self.MakeRotationMatrix()
        n = R.I * np.matrix([[0],[0],[1]])
        tz = self.__z
        tx = -(v0*math.sin(yaw))/(fy*math.cos(roll) + v0*math.cos(yaw)*math.sin(roll))
        ty = -(fy**2*math.sin(roll) + fy*v0*math.cos(roll) + v0**2*math.cos(yaw)*math.sin(roll) - tz*v0**2*math.cos(yaw)*math.sin(roll) - fy*tz*v0*math.cos(roll) - \
               fy*v0*math.cos(roll)*math.cos(yaw))/(fy*(fy*math.cos(roll) + v0*math.cos(yaw)*math.sin(roll)))
        t = np.matrix([[tx],[ty-self.back],[tz]])
        HomogeneousMatrix = self.__K*(R - t*n.T)*self.__K.I
        HomogeneousMatrix = np.array(HomogeneousMatrix.T.I)
        return HomogeneousMatrix
    def K (self):
        print(self.__K)
    def R(self):
        print(self.MakeRotationMatrix())
    def H(self):
        print(self.MakeHomogeneous())
    def Grid (self):
        print(self.MakeGrid())
def transformed (image,K,pitch,height,fx,fy,label,back,ww,hh,kernal=3):
        kernal = np.ones((kernal,kernal))
        H,W,_ = image.shape 
        size = t.tensor([1,1,H,W])
        a = PrepareSTN(size,K,-1*height,pitch,0,-0.0,back)
        H_ = a.MakeHomogeneous()
        H_ = np.array(np.matrix(H_).I.T)
        if not label : 
            image = cv2.warpPerspective(image,H_,(ww,hh),flags=cv2.INTER_LINEAR)
            image = cv2.resize(image,(0,0),fx=fx,fy=fy,interpolation=cv2.INTER_LINEAR) 
        else : 
            image = cv2.warpPerspective(image,H_,(ww,hh),flags=cv2.INTER_NEAREST)
            image = cv2.resize(image,(0,0),fx=fx,fy=fy,interpolation=cv2.INTER_NEAREST) 
            image = cv2.dilate(image,kernal,iterations=1)
            image = cv2.erode(image,kernal,iterations=1) 
        return image 
