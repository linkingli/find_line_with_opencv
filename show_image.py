import cv2
import numpy as numpy
import matplotlib.pyplot as plt



def make_coordinates(image,line_parameters):
    slope,intercept=line_parameters
    print(image.shape)
    y1=image.shape[0]
    y2=int(y1*(3/5))
    x1=int((y1-intercept)/slope)
    x2=int((y2-intercept)/slope)
    return numpy.array([x1,y1,x2,y2])
#归一化处理,huigui
def average_slope_intercept(image,lines):
    left_fit=[]
    right_fit=[]
    for line in lines:
        x1,y1,x2,y2=line.reshape(4)
        parameters=numpy.polyfit((x1,x2),(y1,y2),1)
        slope=parameters[0]
        intercept=parameters[1]
        if slope<0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))
    left_fit_average=numpy.average(left_fit,axis=0)
    right_fit_average=numpy.average(right_fit,axis=0)
    left_line=make_coordinates(image,left_fit_average)
    right_line=make_coordinates(image,right_fit_average)
    return numpy.array([left_line,right_line])




def canny(image):
    gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    bulr=cv2.GaussianBlur(gray,(5,5),0)
    canny=cv2.Canny(bulr,50,150)
    return canny

def display_lines(image,lines):
    line_image=numpy.zeros_like(image)
    if lines  is not None:
        for x1,y1,x2,y2 in lines:
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)
    return line_image


def region_os_interest(image):
    height=image.shape[0]
    polygons=numpy.array([
        [(200,height),(1100,height),(550,250)]
        ])
    mask=numpy.zeros_like(image)
    cv2.fillPoly(mask,polygons,255)
    masked_image=cv2.bitwise_and(image,mask)
    return masked_image

image=cv2.imread('test_image.jpg')
lane_image=numpy.copy(image)
canny=canny(lane_image)

cropped_image=region_os_interest(canny)
lines=cv2.HoughLinesP(cropped_image,2,numpy.pi/180,100,numpy.array([]),minLineLength=40,maxLineGap=5)
average_lines=average_slope_intercept(image,lines)
linne_image=display_lines(lane_image,average_lines)
combo_image=cv2.addWeighted(lane_image,0.8,linne_image,1,1)
cv2.imshow("result",combo_image)
cv2.waitKey(0)