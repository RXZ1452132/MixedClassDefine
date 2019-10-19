use: 
from transformed import transformed
image = transformed(image,K,pitch,height,fx,fy,label,back,ww,hh,kernal=3)
transformed para:
image:图像或者标签
K:相机内参，这里u，v按照定义来定即可，fx=fy这个可以比较随意，两者变大在变换后的图中物体的尺寸变小，容纳的东西会减少，具体可以自己尝试后定一个，类型np.matrix
pitch：变换的俯仰角度可以再1.4-1.9间尝试，以0.01增量进行尝试，用个for循环，看看哪个效果比较好就用哪个
height：变换的高度，10-50每隔10 尝试一下，越大，图中物体尺寸越小，可以容纳的东西越多
fx，fy：变换后的图像在轴x，y上与原图的比例，可以用来调节车道线的宽度
label：如果变换的是label设置成True 否则 设置为False
back:用于前后，越大，结果图片向后平移的越大，推荐20,30,40,50尝试
ww，hh：输出图像的尺寸 ww：shape[1] hh:shape[0]
kernal :用于解决标签变换造成的空洞问题，默认是10，如果感觉空洞问题还有，可以加大
推荐初始参数设置：
K = np.matrix([[1000,0,h/2],[0,1000,w/2],[0,0,1]])
transformed(image,K,1.5,30,1.5,1.5,label=根据需要)
使用的实力见
/home/wenyongkun/MixedClassDefine/www.ananth.in/RoadMarkingDetection_files/RoadMarkingDataset
下边的t.py
