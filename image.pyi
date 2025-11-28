"""
MaixPy image module interface file
移植于 openmv， 与 openmv 功能相同
"""

from typing import Any, List, Tuple, Optional, Union, Dict, Callable

# Global functions
def rgb_to_lab(rgb_tuple: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    返回RGB888格式的元组 rgb_tuple (r, g, b)对应的LAB格式的元组(l, a, b)。
    RGB888是指红、绿、蓝各8位（0-255）。在LAB中，L的取值范围为0-100，a/b 的取值范围为-128到127。
    """
    ...

def lab_to_rgb(lab_tuple: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """
    返回LAB格式的元组 lab_tuple (l, a, b)对应的RGB888格式的元组(r, g, b)。
    RGB888是指红、绿、蓝各8位（0-255）。在LAB中，L的取值范围为0-100，a/b 的取值范围为-128到127。
    """
    ...

def rgb_to_grayscale(rgb_tuple: Tuple[int, int, int]) -> int:
    """
    返回RGB888格式的元组 rgb_tuple (r, g, b)对应的灰度值。
    RGB888是指红、绿、蓝各8位（0-255）。灰度值取值于0-255。
    """
    ...

def grayscale_to_rgb(g_value: int) -> Tuple[int, int, int]:
    """
    返回灰度值 g_value 对应的RGB888格式的元组(r, g, b)。
    RGB888是指红、绿、蓝各8位（0-255）。灰度值取值于0-255。
    """
    ...

def load_decriptor(path: str) -> Any:
    """
    从磁盘上加载一个描述符对象(descriptor object).
    path 是描述符文件保存的路径。
    """
    ...

def save_descriptor(path: str, descriptor: Any) -> None:
    """
    保存描述符对象 descriptor 到磁盘。
    path 是描述符文件保存的路径。
    """
    ...

def match_descriptor(descriptor0: Any, descriptor1: Any, threshold: int = 70, filter_outliers: bool = False) -> Union[int, 'kptmatch']:
    """
    对于LBP描述符来说，这个函数返回的是一个体现两个描述符之间区别的整数。这一距离测度尤为必要。这个距离是对相似度的一个度量。这个测度值越接近0，LBPF特征点匹配得就越好。
    对于ORB描述符来说，这个函数返回的是kptmatch对象。见上。
    threshold 是用来为ORB键点过滤不明确匹配服务的。
    一个较低的 threshold 值将紧扣关键点匹配算法。 threshold 值位于0-100 (int)。默认值为70。
    filter_outliers 是用来为ORB键点过滤异常值服务的。 特征点允许用户提高 threshold 值。默认设置为False。
    """
    ...

# Example code snippets
"""
一、例程
1.1. 例程 1： 找绿色
import sensor
import image
import lcd
import time
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
green_threshold   = (0,   80,  -70,   -10,   -0,   30)
while True:
    img=sensor.snapshot()
    blobs = img.find_blobs([green_threshold])
    if blobs:
    	for b in blobs:
    		tmp=img.draw_rectangle(b[0:4])
    		tmp=img.draw_cross(b[5], b[6])
    		c=img.get_pixel(b[5], b[6])
    lcd.display(img)

1.2. 例程 2： 显示 fps
import sensor
import image
import lcd
import time
clock = time.clock()
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames(30)
while True:
    clock.tick()
    img = sensor.snapshot()
    fps =clock.fps()
    img.draw_string(2,2, ("%2.1ffps" %(fps)), color=(0,128,0), scale=2)
    lcd.display(img)

1.3. 例程 3： 扫描二维码
import sensor
import image
import lcd
import time
clock = time.clock()
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)
sensor.run(1)
sensor.skip_frames(30)
while True:
    clock.tick()
    img = sensor.snapshot()
    res = img.find_qrcodes()
    fps =clock.fps()
    if len(res) > 0:
        img.draw_string(2,2, res[0].payload(), color=(0,128,0), scale=2)
        print(res[0].payload())
    lcd.display(img)
# 如果使用了镜头，画面会有扭曲，需要矫正画面
# 使用 lens_corr 函数来矫正， 比如 2.8mm， img.lens_corr(1.8)
# 无法识别二维码的时候需要用sensor.set_hmirror(1)来调整摄像头的镜像画面

1.4. 例程4 寻找矩阵
# Find Rects Example
#
# 这个例子展示了如何使用april标签代码中的四元检测代码在图像中找到矩形。 四元检测算法以非常稳健的方式检测矩形，并且比基于Hough变换的方法好得多。 例如，即使镜头失真导致这些矩形看起来弯曲，它仍然可以检测到矩形。 圆角矩形是没有问题的！
# (但是，这个代码也会检测小半径的圆)...
import sensor, image, time
sensor.reset()
sensor.set_pixformat(sensor.RGB565) 
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_vflip(1)
clock = time.clock()
while(True):
    clock.tick()
    img = sensor.snapshot()
    # 下面的`threshold`应设置为足够高的值，以滤除在图像中检测到的具有
    # 低边缘幅度的噪声矩形。最适用与背景形成鲜明对比的矩形。
    for r in img.find_rects(threshold = 10000):
        img.draw_rectangle(r.rect(), color = (255, 0, 0))
        for p in r.corners(): img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))
        print(r)
    print("FPS %f" % clock.fps())

1.5. 例程5 寻找Apriltag
# AprilTags 示例
#
# 此示例显示了OpenMV Cam在OpenMV Cam M7上检测April标签的强大功能。
# OpenMV2 M4版本无法检测April标签。
import sensor, image, time, math
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # 如果分辨率更大，我们的内存会耗尽...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # 必须关闭此功能，以防止图像冲洗…
sensor.set_auto_whitebal(False)  # 必须关闭此功能，以防止图像冲洗…
clock = time.clock()
# 注意！与find_qrcodes不同，find_apriltags方法不需要对图像进行镜头校正
# apriltag代码最多支持可以同时处理6种tag家族。
# 返回的tag标记对象，将有其tag标记家族及其在tag标记家族内的id。
tag_families = 0
tag_families |= image.TAG16H5 # 注释掉，禁用这个家族
tag_families |= image.TAG25H7 # 注释掉，禁用这个家族
tag_families |= image.TAG25H9 # 注释掉，禁用这个家族
tag_families |= image.TAG36H10 # 注释掉，禁用这个家族
tag_families |= image.TAG36H11 # 注释掉以禁用这个家族(默认家族)
tag_families |= image.ARTOOLKIT # 注释掉，禁用这个家族
#标签系列有什么区别？ 那么，例如，TAG16H5家族实际上是一个4x4的方形标签。 
#所以，这意味着可以看到比6x6的TAG36H11标签更长的距离。 
#然而，较低的H值（H5对H11），意味着4x4标签的假阳性率远高于6x6标签。 
#所以，除非你有理由使用其他标签系列，否则使用默认族TAG36H11。
def family_name(tag):
    if(tag.family() == image.TAG16H5):
        return "TAG16H5"
    if(tag.family() == image.TAG25H7):
        return "TAG25H7"
    if(tag.family() == image.TAG25H9):
        return "TAG25H9"
    if(tag.family() == image.TAG36H10):
        return "TAG36H10"
    if(tag.family() == image.TAG36H11):
        return "TAG36H11"
    if(tag.family() == image.ARTOOLKIT):
        return "ARTOOLKIT"
while(True):
    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags(families=tag_families): # 如果没有给出家族，默认TAG36H11。
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi)
        print("Tag Family %s, Tag ID %d, rotation %f (degrees)" % print_args)
    print(clock.fps())
"""

class HaarCascade:
    """
    Haar Cascade特征描述符用于 image.find_features() 方法。它没有供用户调用的方法。
    """
    def __init__(self, path: Union[str, bytes], stages: Optional[int] = None) -> None:
        """
        从一个Haar Cascade二进制文件（适合OpenMV Cam 的格式）加载一个Haar Cascade。 
        如果您传递"frontalface"字符串而非一条路径，这个构造函数将会把一个内置的正脸Haar Cascade载入内存。 
        此外，您也可以通过"eye"来把Haar Cascade载入内存。 
        最后，这个方法会返回载入的Haar Cascade对象，用来使用 image.find_features() 。
        stages 默认值为Haar Cascade中的阶段数。然而，您可以指定一个较低的数值来加速运行特征检测器，当然这会带来较高的误报率。
        您可以制作自己的Haar Cascades 来配合您的OpenMV Cam 使用。 
        首先，使用谷歌搜索" Haar Cascade"，检测是否有人已经为您想要检测的对象制作了OpenCV Haar Cascade。 
        如果没有，那您需要自己动手制作（工作量巨大）。 
        关于如何制作自己的Haar Cascade，见此 关于如何把OpenCV Haar Cascades转化成您的OpenMV Cam可以读取的模式， 见此script
        
        问：Haar Cascade 是什么？
        答：Haar Cascade是一系列用来确定一个对象是否存在于图像中的对比检查。 
        这一系列的对比检查分成了多个阶段，后一阶段的运行以先前阶段的完成为前提。 
        对比检查并不复杂，不过是像检查图像的中心垂直是否比边缘更轻微之类的过程。 
        大范围的检查在前期阶段首先进行，在后期进行更多更小的区域检查。
        
        问：Haar Cascades 是如何制作而成的？
        答：Haar Cascades通过标有正负的图像对发生器算法进行训练。 
        比如，用数百张含有猫（已被标记为内含猫）的图片和数百张不含有猫形物的图片（已作出不同标记）来训练这个生成算法。  
        这个生成算法最后会产生一个用来检测猫的Haar Cascades。
        """
        ...

class similarity:
    """
    相似度对象由 image.get_similarity 返回.
    """
    def __init__(self) -> None:
        """请调用 image.get_similarity() 函数来创建此对象。"""
        ...
    
    def mean(self) -> float:
        """
        返回8x8像素块结构相似性差异的均值。范围[-1/+1]，其中 -1完全不同，+1完全相同。
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def stdev(self) -> float:
        """
        返回8x8像素块结构相似性差异的标准偏差。
        您也可以通过索引 [1] 取得这个值。
        """
        ...
    
    def min(self) -> float:
        """
        返回8x8像素块结构相似性差异的最小值。其中 -1完全不同，+1完全相同。
        您也可以通过索引 [2] 取得这个值。
        通过查看此值，您可以快速确定两个图像之间的任何8x8像素块是否差别很大，即远远低于+1。
        """
        ...
    
    def max(self) -> float:
        """
        返回8x8像素块结构相似性差异的最小值。其中 -1完全不同，+1完全相同。
        您也可以通过索引 [3] 取得这个值。
        通过查看此值，您可以快速确定两个图像之间的任何8x8像素块是否都相同。即比-1大很多。
        """
        ...

class histogram:
    """
    直方图对象是由 image.get_histogram 返回。 
    灰度直方图有一个包含多个二进制的通道。 
    所有二进制都进行标准化，使其总和为1。 
    RGB565有三个包含多个二进制的通道。所有二进制都进行标准化，使其总和为1。
    """
    def __init__(self) -> None:
        """请调用 image.get_histogram() 函数来创建此对象。"""
        ...
    
    def bins(self) -> List[float]:
        """
        返回灰度直方图的浮点数列表。 
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def l_bins(self) -> List[float]:
        """
        返回RGB565直方图LAB的L通道的浮点数列表。 
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def a_bins(self) -> List[float]:
        """
        返回RGB565直方图LAB的A通道的浮点数列表。 
        您也可以通过索引 [1] 取得这个值。
        """
        ...
    
    def b_bins(self) -> List[float]:
        """
        返回RGB565直方图LAB的B通道的浮点数列表。 
        您也可以通过索引 [2] 取得这个值。
        """
        ...
    
    def get_percentile(self, percentile: float) -> 'percentile':
        """
        计算直方图频道的CDF，返回一个传递 percentile (0.0 - 1.0) (浮点数)中的直方图的值。
        因此，若您传入0.1，该方法会告知您，当累加入累加器时，哪一个二进制会使累加器跨过0.1。
        在没有异常效用破坏您的自适应色跟踪结果时，这对于确定颜色分布的最小值(0.1)和max(0.9)甚是有效。
        """
        ...
    
    def get_threhsold(self) -> 'threshold':
        """
        使用Otsu's 方法计算最佳阈值，将直方图分的每个通道为两半。 
        该方法返回一个 image.threshold 对象。 
        这个方法对确定最佳的 image.binary() 阈值特别有用。
        """
        ...
    
    def get_statistics(self) -> 'statistics':
        """
        计算直方图中每个颜色通道的平均值、中值、众值、标准差、最小值、最大值、下四分值和上四分值， 
        并返回一个statistics对象。 
        您也可以使用 histogram.statistics() 和 histogram.get_stats() 作为这个方法的别名。
        """
        ...

class percentile:
    """
    百分比值对象由 histogram.get_percentile 返回。 
    灰度百分比值有一个通道。不使用 l_* 、 a_* 或 b_* 方法。 
    RGB565百分比值有三个通道。使用 l_* 、 a_* 和 b_* 方法。
    """
    def __init__(self) -> None:
        """请调用 histogram.get_percentile() 函数来创建此对象。"""
        ...
    
    def value(self) -> int:
        """
        返回灰度百分比值（取值区间为0-255）。
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def l_value(self) -> int:
        """
        返回RGB565 LAB 的L通道的百分比值（取值区间为0-100）。
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def a_value(self) -> int:
        """
        返回RGB565 LAB 的A通道的百分比值（取值区间为-128-127）。
        您也可以通过索引 [1] 取得这个值。
        """
        ...
    
    def b_value(self) -> int:
        """
        返回RGB565 LAB 的B通道的百分比值（取值区间为-128-127）。
        您也可以通过索引 [2] 取得这个值。
        """
        ...

class threshold:
    """
    阈值对象由 histogram.get_threshold 返回。
    灰度图像有一个通道。没有 l_, a_, 和 b_* 方法.
    RGB565 阈值有三个通道。使用 l_, a_, 和 b_* 方法。
    """
    def __init__(self) -> None:
        """请调用 histogram.get_threshold() 函数来创建此对象。"""
        ...
    
    def value(self) -> int:
        """
        返回灰度图的阈值 (between 0 and 255)。
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def l_value(self) -> int:
        """
        返回RGB565图LAB中的L阈值 (between 0 and 100).
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def a_value(self) -> int:
        """
        返回RGB565图LAB中的A阈值 (between -128 and 127).
        您也可以通过索引 [1] 取得这个值。
        """
        ...
    
    def b_value(self) -> int:
        """
        返回RGB565图LAB中的B阈值 (between -128 and 127).
        您也可以通过索引 [2] 取得这个值。
        """
        ...

class statistics:
    """
    统计数据对象是由 histogram.get_statistics 或 image.get_statistics 返回的。
    灰度统计数据有一个通道，使用非 l_* 、 a_* 或 b_* 方法。
    RGB565百分比值有三个通道。使用 l_* 、 a_* 和 b_* 方法。
    """
    def __init__(self) -> None:
        """请调用 histogram.get_statistics() 或 image.get_statistics() 函数来创建此对象。"""
        ...
    
    # 灰度统计方法
    def mean(self) -> int:
        """
        返回灰度均值(0-255) (int)。
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def median(self) -> int:
        """
        返回灰度中值(0-255) (int)。
        您也可以通过索引 [1] 取得这个值。
        """
        ...
    
    def mode(self) -> int:
        """
        返回灰度众值(0-255) (int)。
        您也可以通过索引 [2] 取得这个值。
        """
        ...
    
    def stdev(self) -> int:
        """
        返回灰度标准差(0-255) (int)。
        您也可以通过索引 [3] 取得这个值。
        """
        ...
    
    def min(self) -> int:
        """
        返回灰度最小值(0-255) (int)。
        您也可以通过索引 [4] 取得这个值。
        """
        ...
    
    def max(self) -> int:
        """
        返回灰度最大值(0-255) (int)。
        您也可以通过索引 [5] 取得这个值。
        """
        ...
    
    def lq(self) -> int:
        """
        返回灰度下四分值(0-255) (int)。
        您也可以通过索引 [6] 取得这个值。
        """
        ...
    
    def uq(self) -> int:
        """
        返回灰度上四分值(0-255) (int)。
        您也可以通过索引 [7] 取得这个值。
        """
        ...
    
    # L通道统计方法
    def l_mean(self) -> int:
        """
        返回RGB5656 LAB 中L的均值(0-255) (int)。
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def l_median(self) -> int:
        """
        返回RGB5656 LAB 中L的中值(0-255) (int)。
        您也可以通过索引 [1] 取得这个值。
        """
        ...
    
    def l_mode(self) -> int:
        """
        返回RGB5656 LAB 中L的众值(0-255) (int)。
        您也可以通过索引 [2] 取得这个值。
        """
        ...
    
    def l_stdev(self) -> int:
        """
        返回RGB5656 LAB 中L的标准偏差值(0-255) (int)。
        您也可以通过索引 [3] 取得这个值。
        """
        ...
    
    def l_min(self) -> int:
        """
        返回RGB5656 LAB 中L的最小值(0-255) (int)。
        您也可以通过索引 [4] 取得这个值。
        """
        ...
    
    def l_max(self) -> int:
        """
        返回RGB5656 LAB 中L的最大值(0-255) (int)。
        您也可以通过索引 [5] 取得这个值。
        """
        ...
    
    def l_lq(self) -> int:
        """
        返回RGB5656 LAB 中L的下四分值(0-255) (int)。
        您也可以通过索引 [6] 取得这个值。
        """
        ...
    
    def l_uq(self) -> int:
        """
        返回RGB5656 LAB 中L的上四分值(0-255) (int)。
        您也可以通过索引 [7] 取得这个值。
        """
        ...
    
    # A通道统计方法
    def a_mean(self) -> int:
        """
        返回RGB5656 LAB 中A的均值(0-255) (int)。
        您也可以通过索引 [8] 取得这个值。
        """
        ...
    
    def a_median(self) -> int:
        """
        返回RGB5656 LAB 中A的中值(0-255) (int)。
        您也可以通过索引 [9] 取得这个值。
        """
        ...
    
    def a_mode(self) -> int:
        """
        返回RGB5656 LAB 中A的众值(0-255) (int)。
        您也可以通过索引 [10] 取得这个值。
        """
        ...
    
    def a_stdev(self) -> int:
        """
        返回RGB5656 LAB 中A的标准偏差值(0-255) (int)。
        您也可以通过索引 [11] 取得这个值。
        """
        ...
    
    def a_min(self) -> int:
        """
        返回RGB5656 LAB 中A的最小值(0-255) (int)。
        您也可以通过索引 [12] 取得这个值。
        """
        ...
    
    def a_max(self) -> int:
        """
        返回RGB5656 LAB 中A的最大值(0-255) (int)。
        您也可以通过索引 [13] 取得这个值。
        """
        ...
    
    def a_lq(self) -> int:
        """
        返回RGB5656 LAB 中A的下四分值(0-255) (int)。
        您也可以通过索引 [14] 取得这个值。
        """
        ...
    
    def a_uq(self) -> int:
        """
        返回RGB5656 LAB 中A的上四分值(0-255) (int)。
        您也可以通过索引 [15] 取得这个值。
        """
        ...
    
    # B通道统计方法
    def b_mean(self) -> int:
        """
        返回RGB5656 LAB 中B的均值(0-255) (int)。
        您也可以通过索引 [16] 取得这个值。
        """
        ...
    
    def b_median(self) -> int:
        """
        返回RGB5656 LAB 中B的中值(0-255) (int)。
        您也可以通过索引 [17] 取得这个值。
        """
        ...
    
    def b_mode(self) -> int:
        """
        返回RGB5656 LAB 中B的众值(0-255) (int)。
        您也可以通过索引 [18] 取得这个值。
        """
        ...
    
    def b_stdev(self) -> int:
        """
        返回RGB5656 LAB 中B的标准差值(0-255) (int)。
        您也可以通过索引 [19] 取得这个值。
        """
        ...
    
    def b_min(self) -> int:
        """
        返回RGB5656 LAB 中B的最小值(0-255) (int)。
        您也可以通过索引 [20] 取得这个值。
        """
        ...
    
    def b_max(self) -> int:
        """
        返回RGB5656 LAB 中B的最大值(0-255) (int)。
        您也可以通过索引 [21] 取得这个值。
        """
        ...
    
    def b_lq(self) -> int:
        """
        返回RGB5656 LAB 中B的下四分值(0-255) (int)。
        您也可以通过索引 [22] 取得这个值。
        """
        ...
    
    def b_uq(self) -> int:
        """
        返回RGB5656 LAB 中B的上四分值(0-255) (int)。
        您也可以通过索引 [23] 取得这个值。
        """
        ...

class blob:
    """
    色块对象是由 image.find_blobs 返回的。
    """
    def __init__(self) -> None:
        """请调用 image.find_blobs() 函数来创建此对象。"""
        ...
    
    def rect(self) -> Tuple[int, int, int, int]:
        """
        返回一个矩形元组(x, y, w, h) ，用于如色块边界框的 image.draw_rectangle 等 其他的 image 方法。
        """
        ...
    
    def x(self) -> int:
        """
        返回色块的边界框的x坐标(int)。
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def y(self) -> int:
        """
        返回色块的边界框的y坐标(int)。
        您也可以通过索引 [1] 取得这个值。
        """
        ...
    
    def w(self) -> int:
        """
        返回色块的边界框的w坐标(int)。
        您也可以通过索引 [2] 取得这个值。
        """
        ...
    
    def h(self) -> int:
        """
        返回色块的边界框的h坐标(int)。
        您也可以通过索引 [3] 取得这个值。
        """
        ...
    
    def pixels(self) -> int:
        """
        返回从属于色块(int)一部分的像素数量。
        您也可以通过索引 [4] 取得这个值。
        """
        ...
    
    def cx(self) -> int:
        """
        返回色块(int)的中心x位置。
        您也可以通过索引 [5] 取得这个值。
        """
        ...
    
    def cy(self) -> int:
        """
        返回色块(int)的中心x位置。
        您也可以通过索引 [6] 取得这个值。
        """
        ...
    
    def rotation(self) -> float:
        """
        返回色块的旋转（单位：弧度）。如果色块类似铅笔或钢笔，那么这个值就是介于0-180之间的唯一值。 
        如果这个色块圆的，那么这个值就没有效用。如果这个色块完全不具有对称性，您只能由此得到0-360度的旋转。
        您也可以通过索引 [7] 取得这个值。
        """
        ...
    
    def code(self) -> int:
        """
        返回一个16位的二进制数字，其中为每个颜色阈值设置一个位，这是色块的一部分。 
        例如，如果您通过 image.find_blobs 来寻找三个颜色阈值，这个色块可以设置为0/1/2位。 
        注意：除非以 merge=True 调用 image.find_blobs ，否则每个色块只能设置一位。 
        那么颜色阈值不同的多个色块就可以合并在一起了。 
        您也可以用这个方法以及多个阈值来实现颜色代码跟踪。
        您也可以通过索引 [8] 取得这个值。
        """
        ...
    
    def count(self) -> int:
        """
        返回合并为这一色块的多个色块的数量。只有您以 merge=True 调用 image.find_blobs 时，这个数字才不是1。
        您也可以通过索引 [9] 取得这个值。
        """
        ...
    
    def area(self) -> int:
        """
        返回色块周围的边框面积(w * h)
        """
        ...
    
    def density(self) -> float:
        """
        返回这个色块的密度比。这是在色块边界框区域内的像素点的数量。 
        总的来说，较低的密度比意味着这个对象的锁定得不是很好。
        """
        ...

class line:
    """
    直线对象是由 image.find_lines , image.find_line_segments 或 image.get_regression 返回的。
    """
    def __init__(self) -> None:
        """请调用 image.find_lines(), image.find_line_segments(), 或 image.get_regression() 函数来创建此对象。"""
        ...
    
    def line(self) -> Tuple[int, int, int, int]:
        """
        返回一个直线元组(x1, y1, x2, y2) ，用于如 image.draw_line 等其他的 image 方法。
        """
        ...
    
    def x1(self) -> int:
        """
        返回直线的p1顶点 x坐标分量。
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def y1(self) -> int:
        """
        返回直线的p1 y分量。
        您也可以通过索引 [1] 取得这个值。
        """
        ...
    
    def x2(self) -> int:
        """
        返回直线的p2 x分量。
        您也可以通过索引 [2] 取得这个值。
        """
        ...
    
    def y2(self) -> int:
        """
        返回直线的p2 y分量。
        您也可以通过索引 [3] 取得这个值。
        """
        ...
    
    def length(self) -> float:
        """
        返回直线长度即 sqrt(((x2-x1)^2) + ((y2-y1)^2).
        您也可以通过索引 [4] 取得这个值。
        """
        ...
    
    def magnitude(self) -> int:
        """
        返回霍夫变换后的直线的长度。
        您也可以通过索引 [5] 取得这个值。
        """
        ...
    
    def theta(self) -> int:
        """
        返回霍夫变换后的直线的角度（0-179度）。
        您也可以通过索引 [7] 取得这个值。
        """
        ...
    
    def rho(self) -> int:
        """
        返回霍夫变换后的直线p值。
        您也可以通过索引 [8] 取得这个值。
        """
        ...

class circle:
    """
    圆形对象是由 image.find_circles 返回的。
    """
    def __init__(self) -> None:
        """请调用 image.find_circles() 函数来创建此对象。"""
        ...
    
    def x(self) -> int:
        """
        返回圆的x位置。
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def y(self) -> int:
        """
        返回圆的y位置。
        您也可以通过索引 [1] 取得这个值。
        """
        ...
    
    def r(self) -> int:
        """
        返回圆的半径。
        您也可以通过索引 [2] 取得这个值。
        """
        ...
    
    def magnitude(self) -> int:
        """
        返回圆的大小。
        您也可以通过索引 [3] 取得这个值。
        """
        ...

class rect:
    """
    矩形对象是由 image.find_rects 返回的。
    """
    def __init__(self) -> None:
        """请调用 image.find_rects() 函数来创建此对象。"""
        ...
    
    def corners(self) -> List[Tuple[int, int]]:
        """
        返回一个由矩形对象的四个角组成的四个元组(x,y)的列表。四个角通常是按照从左上角开始沿顺时针顺序返回的。
        """
        ...
    
    def rect(self) -> Tuple[int, int, int, int]:
        """
        返回一个矩形元组(x, y, w, h)，用于如 矩形的边界框的 image.draw_rectangle 等其他的 image 方法。
        """
        ...
    
    def x(self) -> int:
        """
        返回矩形的左上角的x位置。
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def y(self) -> int:
        """
        返回矩形的左上角的y位置。
        您也可以通过索引 [1] 取得这个值。
        """
        ...
    
    def w(self) -> int:
        """
        返回矩形的宽度。
        您也可以通过索引 [2] 取得这个值。
        """
        ...
    
    def h(self) -> int:
        """
        返回矩形的高度。
        您也可以通过索引 [3] 取得这个值。
        """
        ...
    
    def magnitude(self) -> int:
        """
        返回矩形的大小。
        您也可以通过索引 [4] 取得这个值。
        """
        ...

class qrcode:
    """
    二维码对象是由 image.find_qrcodes 返回的。
    """
    def __init__(self) -> None:
        """请调用 image.find_qrcodes() 函数来创建此对象。"""
        ...
    
    def corners(self) -> List[Tuple[int, int]]:
        """
        返回一个由该对象的四个角组成的四个元组(x,y)的列表。四个角通常是按照从左上角开始沿顺时针顺序返回的。
        """
        ...
    
    def rect(self) -> Tuple[int, int, int, int]:
        """
        返回一个矩形元组(x, y, w, h)，用于如二维码的边界框的 image.draw_rectangle 等其他的 image 方法。
        """
        ...
    
    def x(self) -> int:
        """
        返回二维码的边界框的x坐标(int)。
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def y(self) -> int:
        """
        返回二维码的边界框的y坐标(int)。
        您也可以通过索引 [1] 取得这个值。
        """
        ...
    
    def w(self) -> int:
        """
        返回二维码的边界框的w坐标(int)。
        您也可以通过索引 [2] 取得这个值。
        """
        ...
    
    def h(self) -> int:
        """
        返回二维码的边界框的h坐标(int)。
        您也可以通过索引 [3] 取得这个值。
        """
        ...
    
    def payload(self) -> str:
        """
        返回二维码有效载荷的字符串，例如URL 。
        您也可以通过索引 [4] 取得这个值。
        """
        ...
    
    def version(self) -> int:
        """
        返回二维码的版本号(int)。
        您也可以通过索引 [5] 取得这个值。
        """
        ...
    
    def ecc_level(self) -> int:
        """
        返回二维码的ECC水平(int)。
        您也可以通过索引 [6] 取得这个值。
        """
        ...
    
    def mask(self) -> int:
        """
        返回二维码的掩码(int)。
        您也可以通过索引 [7] 取得这个值。
        """
        ...
    
    def data_type(self) -> int:
        """
        返回二维码的数据类型。
        您也可以通过索引 [8] 取得这个值。
        """
        ...
    
    def eci(self) -> int:
        """
        返回二维码的ECI。ECI储存了QR码中存储数据字节的编码。若您想要处理包含超过标准ASCII文本的二维码，您需要查看这一数值。
        您也可以通过索引 [9] 取得这个值。
        """
        ...
    
    def is_numeric(self) -> bool:
        """
        若二维码的数据类型为数字式，则返回True。
        """
        ...
    
    def is_alphanumeric(self) -> bool:
        """
        若二维码的数据类型为文字数字式，则返回True。
        """
        ...
    
    def is_binary(self) -> bool:
        """
        若二维码的数据类型为二进制式，则返回True。如果您认真处理所有类型的文本，则需要检查eci是否为True，以确定数据的文本编码。通常它只是标准的ASCII，但是它也可能是有两个字节字符的UTF8。
        """
        ...
    
    def is_kanji(self) -> bool:
        """
        若二维码的数据类型为日本汉字，则返回True。设置为True后，您就需要自行解码字符串，因为日本汉字符号每个字符是10位，而MicroPython不支持解析这类文本。
        """
        ...

class apriltag:
    """
    AprilTag对象是由 image.find_apriltags 返回的。
    """
    def __init__(self) -> None:
        """请调用 image.find_apriltags() 函数来创建此对象。"""
        ...
    
    def corners(self) -> List[Tuple[int, int]]:
        """
        返回一个由该对象的四个角组成的四个元组(x,y)的列表。四个角通常是按照从左上角开始沿顺时针顺序返回的。
        """
        ...
    
    def rect(self) -> Tuple[int, int, int, int]:
        """
        返回一个矩形元组(x, y, w, h)，用于如AprilTag边界框的 image.draw_rectangle 等其他的 image 方法。
        """
        ...
    
    def x(self) -> int:
        """
        返回AprilTag边界框的x坐标(int)。
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def y(self) -> int:
        """
        返回AprilTag边界框的y坐标(int)。
        您也可以通过索引 [1] 取得这个值。
        """
        ...
    
    def w(self) -> int:
        """
        返回AprilTag边界框的w坐标(int)。
        您也可以通过索引 [2] 取得这个值。
        """
        ...
    
    def h(self) -> int:
        """
        返回AprilTag边界框的h坐标(int)。
        您也可以通过索引 [3] 取得这个值。
        """
        ...
    
    def id(self) -> int:
        """
        返回AprilTag的数字ID。
        TAG16H5 -> 0 to 29
        TAG25H7 -> 0 to 241
        TAG25H9 -> 0 to 34
        TAG36H10 -> 0 to 2319
        TAG36H11 -> 0 to 586
        ARTOOLKIT -> 0 to 511
        您也可以通过索引 [4] 取得这个值。
        """
        ...
    
    def family(self) -> int:
        """
        返回AprilTag的数字家庭。
        image.TAG16H5
        image.TAG25H7
        image.TAG25H9
        image.TAG36H10
        image.TAG36H11
        image.ARTOOLKIT
        您也可以通过索引 [5] 取得这个值。
        """
        ...
    
    def cx(self) -> int:
        """
        返回AprilTag的中心x位置(int)。
        您也可以通过索引 [6] 取得这个值。
        """
        ...
    
    def cy(self) -> int:
        """
        返回AprilTag的中心y位置(int)。
        您也可以通过索引 [7] 取得这个值。
        """
        ...
    
    def rotation(self) -> float:
        """
        返回以弧度计的AprilTag的旋度(int)。
        您也可以通过索引 [8] 取得这个值。
        """
        ...
    
    def decision_margin(self) -> float:
        """
        返回AprilTag匹配的色饱和度（取值0.0 - 1.0），其中1.0为最佳。
        您也可以通过索引 [9] 取得这个值。
        """
        ...
    
    def hamming(self) -> int:
        """
        返回AprilTag的可接受的数位误差数值。
        TAG16H5 -> 最多可接受0位错误
        TAG25H7 -> 最多可接受1位错误
        TAG25H9 -> 最多可接受3位错误
        TAG36H10 -> 最多可接受3位错误
        TAG36H11 -> 最多可接受4位错误
        ARTOOLKIT -> 最多可接受0位错误
        您也可以通过索引 [10] 取得这个值。
        """
        ...
    
    def goodness(self) -> float:
        """
        返回AprilTag图像的色饱和度（取值0.0 - 1.0），其中1.0为最佳。
        目前这一数值通常是0.0。未来我们可以启用一个称为"标签细化"的功能，以实现对更小的AprilTag的检测。然而，现在这个功能将帧速率降低到1 FPS以下。
        您也可以通过索引 [11] 取得这个值。
        """
        ...
    
    def x_translation(self) -> float:
        """
        返回距离摄像机x方向的变换，距离的单位未知。
        这个方法对于确定远离摄像机的AprilTag的位置很有用。但是，AprilTag的大小以及您使用的镜头等因素都会影响X单元归属的确定。为使用方便，我们推荐您使用查找表将该方法的输出转换为对您的应用程序有用的信息。
        注意：此处的方向为从左至右。
        您也可以通过索引 [12] 取得这个值。
        """
        ...
    
    def y_translation(self) -> float:
        """
        返回距离摄像机y方向的变换，距离的单位未知。
        这个方法对于确定远离摄像机的AprilTag的位置很有用。但是，AprilTag的大小以及您使用的镜头等因素都会影响Y单元归属的确定。为使用方便，我们推荐您使用查找表将该方法的输出转换为对您的应用程序有用的信息。
        注意：此处的方向为从上至下。
        您也可以通过索引 [13] 取得这个值。
        """
        ...
    
    def z_translation(self) -> float:
        """
        返回距离摄像机z方向的变换，距离的单位未知。
        T这个方法对于确定远离摄像机的AprilTag的位置很有用。但是，AprilTag的大小以及您使用的镜头等因素都会影响Z单元归属的确定。为使用方便，我们推荐您使用查找表将该方法的输出转换为对您的应用程序有用的信息。
        注意：此处的方向为从前至后。
        您也可以通过索引 [14] 取得这个值。
        """
        ...
    
    def x_rotation(self) -> float:
        """
        返回以弧度计的AprilTag在X平面上的旋度。例：目视AprilTag，从左至右移动摄像头。
        您也可以通过索引 [15] 取得这个值。
        """
        ...
    
    def y_rotation(self) -> float:
        """
        返回以弧度计的AprilTag在Y平面上的旋度。例：目视AprilTag，从上至下移动摄像头。
        您也可以通过索引 [16] 取得这个值。
        """
        ...
    
    def z_rotation(self) -> float:
        """
        返回以弧度计的AprilTag在Z平面上的旋度。例：目视AprilTag，旋转摄像头。
        注意：这只是 apriltag.rotation() 的重命名版本。
        您也可以通过索引 [17] 取得这个值。
        """
        ...

class datamatrix:
    """
    数据矩阵对象是由 image.find_datamatrices 返回的。
    """
    def __init__(self) -> None:
        """请调用 image.find_datamatrices() 函数来创建此对象。"""
        ...
    
    def corners(self) -> List[Tuple[int, int]]:
        """
        返回一个由该对象的四个角组成的四个元组(x,y)的列表。四个角通常是按照从左上角开始沿顺时针顺序返回的。
        """
        ...
    
    def rect(self) -> Tuple[int, int, int, int]:
        """
        返回一个矩形元组(x, y, w, h)，用于如数据矩阵的边界框的 image.draw_rectangle 等其他的 image 方法。
        """
        ...
    
    def x(self) -> int:
        """
        返回数据矩阵的边界框的x坐标(int)。
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def y(self) -> int:
        """
        返回数据矩阵的边界框的y坐标(int)。
        您也可以通过索引 [1] 取得这个值。
        """
        ...
    
    def w(self) -> int:
        """
        返回数据矩阵的边界框的w宽度。
        您也可以通过索引 [2] 取得这个值。
        """
        ...
    
    def h(self) -> int:
        """
        返回数据矩阵的边界框的h高度。
        您也可以通过索引 [3] 取得这个值。
        """
        ...
    
    def payload(self) -> str:
        """
        返回数据矩阵的有效载荷的字符串。例：字符串。
        您也可以通过索引 [4] 取得这个值。
        """
        ...
    
    def rotation(self) -> float:
        """
        返回以弧度计的数据矩阵的旋度(浮点数)。
        您也可以通过索引 [5] 取得这个值。
        """
        ...
    
    def rows(self) -> int:
        """
        返回数据矩阵的行数(int)。
        您也可以通过索引 [6] 取得这个值。
        """
        ...
    
    def columns(self) -> int:
        """
        返回数据矩阵的列数(int)。
        您也可以通过索引 [7] 取得这个值。
        """
        ...
    
    def capacity(self) -> int:
        """
        返回这一数据矩阵所能容纳的字符的数量。
        您也可以通过索引 [8] 取得这个值。
        """
        ...
    
    def padding(self) -> int:
        """
        返回这一数据矩阵中未使用的字符的数量。
        您也可以通过索引 [9] 取得这个值。
        """
        ...

class barcode:
    """
    条形码对象是由 image.find_barcodes 返回的。
    """
    def __init__(self) -> None:
        """请调用 image.find_barcodes() 函数来创建此对象。"""
        ...
    
    def corners(self) -> List[Tuple[int, int]]:
        """
        返回一个由该对象的四个角组成的四个元组(x,y)的列表。四个角通常是按照从左上角开始沿顺时针顺序返回的。
        """
        ...
    
    def rect(self) -> Tuple[int, int, int, int]:
        """
        返回一个矩形元组(x, y, w, h)，用于如数据矩阵的边界框的 image.draw_rectangle 等其他的 image 方法。
        """
        ...
    
    def x(self) -> int:
        """
        返回条形码的边界框的x坐标(int)。
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def y(self) -> int:
        """
        返回条形码的边界框的y坐标(int)。
        您也可以通过索引 [1] 取得这个值。
        """
        ...
    
    def w(self) -> int:
        """
        返回条形码的边界框的w宽度(int)。
        您也可以通过索引 [2] 取得这个值。
        """
        ...
    
    def h(self) -> int:
        """
        返回条形码的边界框的h高度(int)。
        您也可以通过索引 [3] 取得这个值。
        """
        ...
    
    def payload(self) -> str:
        """
        返回条形码的有效载荷的字符串。例：数量。
        您也可以通过索引 [4] 取得这个值。
        """
        ...
    
    def type(self) -> int:
        """
        返回条形码的列举类型 (int)。
        您也可以通过索引 [5] 取得这个值。
        image.EAN2
        image.EAN5
        image.EAN8
        image.UPCE
        image.ISBN10
        image.UPCA
        image.EAN13
        image.ISBN13
        image.I25
        image.DATABAR
        image.DATABAR_EXP
        image.CODABAR
        image.CODE39
        image.PDF417 - 未来启用 (e.g. 现在还不能正常使用).
        image.CODE93
        image.CODE128
        """
        ...
    
    def rotation(self) -> float:
        """
        返回以弧度计的条形码的旋度(浮点数)。
        您也可以通过索引 [6] 取得这个值。
        """
        ...
    
    def quality(self) -> int:
        """
        返回条形码在图像中被检测到的次数(int)。
        扫描条形码时，每一条新的扫描线都能解码相同的条形码。每次进行这一过程，条形码的值都会随之增加。
        您也可以通过索引 [7] 取得这个值。
        """
        ...

class displacement:
    """
    位移对象由 image.find_displacement 返回。
    """
    def __init__(self) -> None:
        """请调用 image.find_displacement() 函数来创建此对象。"""
        ...
    
    def x_translation(self) -> float:
        """
        返回两个图像之间的x平移像素。 这是精确的子像素，所以它是一个浮点数。
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def y_translation(self) -> float:
        """
        返回两个图像之间的y平移像素。 这是精确的子像素，所以它是一个浮点数。
        您也可以通过索引 [1] 取得这个值。
        """
        ...
    
    def rotation(self) -> float:
        """
        返回两个图像之间的z平移像素。 这是精确的子像素，所以它是一个浮点数。
        您也可以通过索引 [2] 取得这个值。
        """
        ...
    
    def scale(self) -> float:
        """
        返回两个图像之间旋转的弧度。
        您也可以通过索引 [3] 取得这个值。
        """
        ...
    
    def response(self) -> float:
        """
        返回两幅图像之间位移匹配结果的质量。 范围 0-1。响应小于0.1的 displacement 对象可能是噪声。
        您也可以通过索引 [4] 取得这个值。
        """
        ...

class kptmatch:
    """
    特征点对象是由 image.match_descriptor 返回的。
    """
    def __init__(self) -> None:
        """请调用 image.match_descriptor() 函数来创建此对象。"""
        ...
    
    def rect(self) -> Tuple[int, int, int, int]:
        """
        返回一个矩形元组(x, y, w, h)，用于如特征点的边界框的 image.draw_rectangle 等其他的 image 方法。
        """
        ...
    
    def cx(self) -> int:
        """
        返回特征点的中心x位置(int)。
        您也可以通过索引 [0] 取得这个值。
        """
        ...
    
    def cy(self) -> int:
        """
        返回特征点的中心y位置(int)。
        您也可以通过索引 [1] 取得这个值。
        """
        ...
    
    def x(self) -> int:
        """
        返回特征点边界框的x坐标(int)。
        您也可以通过索引 [2] 取得这个值。
        """
        ...
    
    def y(self) -> int:
        """
        返回特征点边界框的y坐标(int)。
        您也可以通过索引 [3] 取得这个值。
        """
        ...
    
    def w(self) -> int:
        """
        返回特征点边界框的w宽度(int)。
        您也可以通过索引 [4] 取得这个值。
        """
        ...
    
    def h(self) -> int:
        """
        返回特征点边界框的h高度(int)。
        您也可以通过索引 [5] 取得这个值。
        """
        ...
    
    def count(self) -> int:
        """
        返回匹配的特征点的数量(int)。
        您也可以通过索引 [6] 取得这个值。
        """
        ...
    
    def theta(self) -> int:
        """
        返回估计的特征点的旋度(int)。
        您也可以通过索引 [7] 取得这个值。
        """
        ...
    
    def match(self) -> List[Tuple[int, int]]:
        """
        返回匹配关键点的(x，y)元组列表。
        您也可以通过索引 [8] 取得这个值。
        """
        ...

class ImageWriter:
    """
    ImageWriter 对象使得您可以快速地将未压缩的图像写入磁盘。
    """
    def __init__(self, path: str) -> None:
        """
        创建一个ImageWriter对象，您就可以以用于OpenMV Cams的简单文件格式将未压缩的图像写到磁盘上。然后未压缩的图像可以使用ImageReader重新读取。
        """
        ...
    
    def size(self) -> int:
        """返回正在写入的文件的大小。"""
        ...
    
    def add_frame(self, img: 'Image') -> None:
        """
        将一张图像写入磁盘。由于图像未被压缩，因此执行迅速，但会占用大量磁盘空间。
        """
        ...
    
    def close(self) -> None:
        """
        关闭图像流文件。您必须关闭文件，否则文件会损坏。
        """
        ...

class ImageReader:
    """
    ImageReader对象使得您可以快速地从磁盘中读取未压缩的图像。
    """
    def __init__(self, path: str) -> None:
        """
        创建一个ImageReader对象，用来回放由ImageWriter对象编写的图像数据。ImageWriter对象回放的帧会在与写入磁盘时相同的FPS下回放。
        """
        ...
    
    def size(self) -> int:
        """返回正在读取的文件的大小。"""
        ...
    
    def next_frame(self, copy_to_fb: bool = True, loop: bool = True) -> Optional['Image']:
        """
        从ImageWriter写就的文件中返回图像对象。若 copy_to_fb 为True，图像对象将被直接加载到帧缓冲区中。否则图像对象将被放入堆中。注意：除非图像很小，否则堆可能没有足够的空间来存储图像对象。 
        若 loop 为True，流的最后一个图像读取之后，回放将重新开始。否则所有帧被读取后，这个方法将返回None。
        注意： imagereader.next_frame 尝试在读取帧后通过暂停播放来限制回放速度，以与帧记录的速度相匹配。 
        否则，这个方法会以200+FPS的速度图像快读播放所有图像。
        """
        ...
    
    def close(self) -> None:
        """
        关闭正在读取的文件。您需要进行这一操作，以防imagereader 对象受损。但由于是只读文件，文件不会在未关闭时受损。
        """
        ...

class Image:
    """
    图像对象是机器视觉操作的基本对象。
    """
    def __init__(self, path: str, copy_to_fb: bool = False) -> None:
        """
        从 path 中的文件中创建一个新的图像对象。
        支持bmp/pgm/ppm/jpg/jpeg格式的图像文件。
        若 copy_to_fb 为True，图像会直接载入帧缓冲区，您就可以加载大幅图片了。若为False，图像会载入MicroPython的堆中，堆远比帧缓冲区小。
        在OpenMV Cam M4中，若 copy_to_fb 为False，您应该尽量把图像大小控制在8KB以下。若为True，则图像最大可为160KB。
        在OpenMV Cam M7中，若 copy_to_fb 为False，您应该尽量把图像大小控制在16KB以下。若为True，则图像最大可为320KB。
        图像支持"[]"记法。 令 image[index] = 8/16-bit value ，以便分配图像像素或 image[index] ，并得到一个图像像素，若是用于RGB图像的16位RGB565值的灰度图像， 
        这一像素则为8位。
        对于JPEG图像而言，"[]"使得您可以访问压缩的节数组形式的JPEG图像色块。由于JPEG图像是压缩的字节流形式，因而对数据组的读取和写入是不透明的。
        图像还支持读缓冲区操作。您可以把图像当作节数组对象，将图像输入所有类型的MicroPython函数。若您想传送一个图像，可以将它传递给UART /SPI/ I2C写入函数，可实现自动传送。
        """
        ...
    
    def width(self) -> int:
        """返回以像素计的图像的宽度。"""
        ...
    
    def height(self) -> int:
        """返回以像素计的图像的高度。"""
        ...
    
    def format(self) -> int:
        """
        返回用于灰度图的 sensor.GRAYSCALE 、用于RGB图像的 sensor.RGB565 和用于JPEG图像的 sensor.JPEG 。
        """
        ...
    
    def size(self) -> int:
        """返回以字节计的图像大小。"""
        ...
    
    def get_pixel(self, x: int, y: int, rgbtuple: bool = False) -> Union[int, Tuple[int, int, int]]:
        """
        灰度图：返回(x, y)位置的灰度像素值。
        RGB565l：返回(x, y)位置的RGB888像素元组(r, g, b)。
        Bayer图像: 返回(x, y)位置的像素值。
        不支持压缩图像。
        image.get_pixel() 和 image.set_pixel()是允许你操作Bayer模式图像的唯一方法。 
        Bayer模式图像是文字图像。对于偶数行，其中图像中的像素是R/G/R/G/等。 
        对于奇数行，其中图像中的像素是G/B/G/B/等。 每个像素是8位。
        """
        ...
    
    def set_pixel(self, x: int, y: int, pixel: Union[int, Tuple[int, int, int]]) -> None:
        """
        灰度图：将(x, y) 位置的像素设置为灰度值 pixel 。
        RGB图像：将(x, y) 位置的像素设置为RGB888元组(r, g, b) pixel 。
        不支持压缩图像。
        image.get_pixel() 和 image.set_pixel()是允许你操作Bayer模式图像的唯一方法。 
        Bayer模式图像是文字图像。对于偶数行，其中图像中的像素是R/G/R/G/等。 
        对于奇数行，其中图像中的像素是G/B/G/B/等。 每个像素是8位。
        """
        ...
    
    def mean_pool(self, x_div: int, y_div: int) -> 'Image':
        """
        在图像中找到 x_div * y_div 正方形的平均值，并返回由每个正方形的平均值组成的修改图像。
        此方法允许您在原来图像上快速缩小图像。
        不支持压缩图像和bayer图像。
        """
        ...
    
    def mean_pooled(self, x_div: int, y_div: int) -> 'Image':
        """
        在图像中找到 x_div * y_div 正方形的平均值，并返回由每个正方形的平均值组成的新图像。
        此方法允许您创建缩小的图像副本。
        不支持压缩图像和bayer图像。
        """
        ...
    
    def midpoint_pool(self, x_div: int, y_div: int, bias: float = 0.5) -> 'Image':
        """
        在图像中找到 x_div * y_div 正方形的中点值，并返回由每个正方形的中点值组成的修改图像。
        bias 为0.0返回每个区域的最小值，而bias 为1.0返回每个区域的最大值。
        此方法允许您在原来图像上快速缩小图像。
        不支持压缩图像和bayer图像。
        """
        ...
    
    def midpoint_pooled(self, x_div: int, y_div: int, bias: float = 0.5) -> 'Image':
        """
        在图像中找到 x_div * y_div 正方形的中点值，并返回由每个正方形的中点值组成的新图像。
        bias 为0.0返回每个区域的最小值，而bias 为1.0返回每个区域的最大值。
        此方法允许您创建缩小的图像副本。
        不支持压缩图像和bayer图像。
        """
        ...
    
    def to_grayscale(self, copy: bool = False) -> 'Image':
        """
        将图像转换为灰度图像。 
        此方法也会修改基础图像像素，以字节为单位更改图像大小，因此只能在灰度图像或RGB565图像上进行。 
        否则 copy 必须为True才能在堆上创建新的修改图像。
        返回图像对象，以便您可以使用 . 表示法调用另一个方法。
        不支持压缩图像和bayer图像。
        """
        ...
    
    def to_rgb565(self, copy: bool = False) -> 'Image':
        """
        将图像转换为彩色图像。 
        此方法也会修改基础图像像素，以字节为单位更改图像大小，因此只能在RGB565图像上进行。 
        否则 copy 必须为True才能在堆上创建新的修改图像。
        返回图像对象，以便您可以使用 . 表示法调用另一个方法。
        不支持压缩图像和bayer图像。
        """
        ...
    
    def to_rainbow(self, copy: bool = False) -> 'Image':
        """
        将图像转换为彩虹图像。 
        此方法也会修改基础图像像素，以字节为单位更改图像大小，因此只能在RGB565图像上进行。 
        否则 copy 必须为True才能在堆上创建新的修改图像。
        彩虹图像是彩色图像，对于图像中的每个8位掩模灰度照明值具有唯一的颜色值。 
        例如，它为热图像提供热图颜色。
        返回图像对象，以便您可以使用 . 表示法调用另一个方法。
        不支持压缩图像和bayer图像。
        """
        ...
    
    def compress(self, quality: int = 50) -> 'Image':
        """
        JPEG对图像进行适当压缩。使用这种方法与 compressed 保存堆空间相比，使用更高quality的压缩率是以破坏原始图像为代价的。
        quality 是压缩质量（0-100）（int）。
        """
        ...
    
    def compress_for_ide(self, quality: int = 50) -> 'Image':
        """
        JPEG对图像进行适当压缩。使用这种方法与 compressed 保存堆空间相比，使用更高quality的压缩率是以破坏原始图像为代价的。
        这个方法压缩图像，然后通过将每6比特编码为128 - 191之间的字节将JPEG数据格式化，转换为OpenMV IDE，以便显示。进行这一步是为防止JPEG数据被误认为是字节流中的其他文本数据。
        您需要使用这一方法来格式化图像数据，以便在OpenMV IDE中通过"开放终端"创建的终端窗口中显示。
        quality 是压缩质量（0-100）（int）。
        """
        ...
    
    def compressed(self, quality: int = 50) -> 'Image':
        """
        返回一个JPEG压缩图像—原始图像未经处理。但是，这个方法需要堆空间的大分配，所以图像压缩质量和图像分辨率必须很低。
        quality 是压缩质量（0-100）（int）。
        """
        ...
    
    def compressed_for_ide(self, quality: int = 50) -> 'Image':
        """
        返回一个JPEG压缩图像—原始图像未经处理。但是，这个方法需要堆空间的大分配，所以图像压缩质量和图像分辨率必须很低。
        这个方法压缩图像，然后通过将每6比特编码为128 - 191之间的字节将JPEG数据格式化，转换为OpenMV IDE，以便显示。进行这一步是为防止JPEG数据被误认为是字节流中的其他文本数据。
        您需要使用这一方法来格式化图像数据，以便在OpenMV IDE中通过"开放终端"创建的终端窗口中显示。
        quality 是压缩质量（0-100）（int）。
        """
        ...
    
    def copy(self, roi: Optional[Tuple[int, int, int, int]] = None, copy_to_fb: bool = False) -> 'Image':
        """
        创建一个图像对象的副本。
        Roi 是一个用以复制的矩形的感兴趣区域(x, y, w, h)。如果未指定，ROI即复制整个图像的图像矩形。但这不适用于JPEG图像。
        请记住图像副本储存在MicroPython 堆中而不是帧缓冲区。同样，您需要将图像副本大小控制在8KB以下（OpenMV）或16KB以下（OpenMV Cam M7） 
        如果您想使用一个复制操作来使用所有的堆空间，这个函数会出现异常。过大的图像极易触发异常。
        如果 copy_to_fb 为True，则该方法将帧缓冲替换为图像。 
        帧缓冲区具有比堆大得多的空间，并且可以容纳大图像。
        """
        ...
    
    def save(self, path: str, roi: Optional[Tuple[int, int, int, int]] = None, quality: int = 50) -> None:
        """
        将图像的副本保存到 path 中的文件系统。
        支持bmp/pgm/ppm/jpg/jpeg格式的图像文件。注意：您无法将jpeg格式的压缩图像保存成未压缩的格式。
        roi 是一个用以复制的矩形的感兴趣区域(x, y, w, h)。如果未指定，ROI即复制整个图像的图像矩形。但这不适用于JPEG图像。
        quality 指在图像尚未被压缩时将图像保存为JPEG格式的JPEG压缩质量。
        """
        ...
    
    def clear(self) -> 'Image':
        """
        将图像中的所有像素设置为零（非常快）。
        返回图像对象，以便您可以使用 . 表示法调用另一个方法。
        不支持压缩图像。
        """
        ...
    
    def draw_line(self, *args: Any, color: Union[Tuple[int, int, int], int] = (255, 255, 255), 
                 thickness: int = 1) -> 'Image':
        """
        在图像上绘制一条从(x0，y0)到(x1，y1)的线。 
        您可以单独传递x0，y0，x1，y1，也可以传递给元组(x0，y0，x1，y1)。
        color 是用于灰度或RGB565图像的RGB888元组。默认为白色。但是，您也可以传递灰度图像的基础像素值(0-255)或RGB565图像的字节反转RGB565值。
        thickness 控制线的粗细像素。
        返回图像对象，以便您可以使用 . 表示法调用另一个方法。
        不支持压缩图像和bayer图像。
        """
        ...
    
    def draw_rectangle(self, *args: Any, color: Union[Tuple[int, int, int], int] = (255, 255, 255), 
                      thickness: int = 1, fill: bool = False) -> 'Image':
        """
        在图像上绘制一个矩形。 
        您可以单独传递x，y，w，h或作为元组(x，y，w，h)传递。
        color 是用于灰度或RGB565图像的RGB888元组。默认为白色。但是，您也可以传递灰度图像的基础像素值(0-255)或RGB565图像的字节反转RGB565值。
        thickness 控制线的粗细像素。
        将 fill 设置为True以填充矩形。
        返回图像对象，以便您可以使用 . 表示法调用另一个方法。
        不支持压缩图像和bayer图像。
        """
        ...
    
    def draw_ellipse(self, *args: Any, color: Union[Tuple[int, int, int], int] = (255, 255, 255), 
                    thickness: int = 1, fill: bool = False) -> 'Image':
        """
        在图像上绘制椭圆。您可以单独传递cx、cy、rx、ry和rotation(以度为单位)，也可以作为元组传递(cx、yc、rx、ry、rotation)。
        color 是用于灰度或RGB565图像的RGB888元组。默认为白色。 
        但是，您也可以为灰度图像传递基础像素值(0-255)，或者为RGB565图像传递字节反转的RGB565值。
        thickness 控制边缘的厚度，以像素为单位。
        传递 fill 设置为True来填充椭圆。
        返回图像对象，以便您可以使用 . 表示法调用另一个方法。
        不支持压缩图像或bayer图像。
        """
        ...
    
    def draw_circle(self, *args: Any, color: Union[Tuple[int, int, int], int] = (255, 255, 255), 
                   thickness: int = 1, fill: bool = False) -> 'Image':
        """
        在图像上绘制一个圆形。 
        您可以单独传递x，y，半径 或 作为元组(x，y，radius)传递。
        color 是用于灰度或RGB565图像的RGB888元组。默认为白色。但是，您也可以传递灰度图像的基础像素值(0-255)或RGB565图像的字节反转RGB565值。
        thickness 控制线的粗细像素。
        将 fill 设置为True以填充圆形。
        返回图像对象，以便您可以使用 . 表示法调用另一个方法。
        不支持压缩图像和bayer图像。
        """
        ...
    
    def draw_string(self, *args: Any, text: str, color: Union[Tuple[int, int, int], int] = (255, 255, 255), 
                   scale: int = 1, x_spacing: int = 0, y_spacing: int = 0, mono_space: bool = True) -> 'Image':
        """
        从图像中的(x, y)位置开始绘制8x10文本。您可以单独传递x，y，也可以作为元组(x，y)传递。
        text 是写入图像的字符串。 
        , \r, 和 \r
         结束符将光标移至下一行。
        color 是用于灰度或RGB565图像的RGB888元组。默认为白色。但是，您也可以传递灰度图像的基础像素值(0-255)或RGB565图像的字节反转RGB565值。
        可以增加 scale 以增加图像上文本的大小。
        仅整数值（例如，1/2/3 /等）。
        x_spacing 允许你在字符之间添加（如果是正数）或减去（如果是负数）x像素，设置字符间距。
        y_spacing 允许你在字符之间添加（如果是正数）或减去（如果是负数）y像素，设置行间距。
        mono_space 默认为True，强制文本间距固定。对于大文本，这看起来很糟糕。设置False以获得非固定宽度的字符间距，看起来好多了。
        返回图像对象，以便您可以使用 . 表示法调用另一个方法。
        不支持压缩图像和bayer图像。
        """
        ...
    
    def draw_cross(self, *args: Any, color: Union[Tuple[int, int, int], int] = (255, 255, 255), 
                  size: int = 5, thickness: int = 1) -> 'Image':
        """
        在图像上绘制一个十字。 
        您可以单独传递x，y或作为元组(x，y)传递。
        color 是用于灰度或RGB565图像的RGB888元组。默认为白色。但是，您也可以传递灰度图像的基础像素值(0-255)或RGB565图像的字节反转RGB565值。
        size 控制十字线的延伸长度。
        thickness 控制边缘的像素厚度。
        返回图像对象，以便您可以使用 . 表示法调用另一个方法。
        不支持压缩图像和bayer图像。
        """
        ...
    
    def draw_arrow(self, *args: Any, color: Union[Tuple[int, int, int], int] = (255, 255, 255), 
                  thickness: int = 1) -> 'Image':
        """
        在图像上绘制一条从(x0，y0)到(x1，y1)的箭头。 
        您可以单独传递x0，y0，x1，y1，也可以传递给元组(x0，y0，x1，y1)。
        color 是用于灰度或RGB565图像的RGB888元组。默认为白色。但是，您也可以传递灰度图像的基础像素值(0-255)或RGB565图像的字节反转RGB565值。
        thickness 控制线的粗细像素。
        返回图像对象，以便您可以使用 . 表示法调用另一个方法。
        不支持压缩图像和bayer图像。
        """
        ...
    
    def draw_image(self, image: 'Image', *args: Any, x_scale: float = 1.0, y_scale: float = 1.0, 
                  mask: Optional['Image'] = None, alpha: int = 256) -> 'Image':
        """
        绘制一个 image ，其左上角从位置x，y开始。 
        您可以单独传递x，y，也可以传递给元组(x，y)。
        x_scale 控制图像在x方向(浮点数)缩放的程度。
        y_scale 控制图像在y方向(浮点数)缩放的程度。
        mask 是另一个用作绘图操作的像素级掩码的图像。掩码应该是一个只有黑色或白色像素的图像，并且应该与你正在绘制的 image 大小相同。 
        您可以使用mask掩码进行绘制操作。
        alpha 控制源图像绘制到目标图像中的透明度。256 为绘制不透明的源图像，而小于 256 的值产生源图像和目标图像之间的混合。0 表示不修改目标图像。
        不支持压缩图像和bayer图像。
        """
        ...
    
    def draw_keypoints(self, keypoints: Any, color: Union[Tuple[int, int, int], int] = (255, 255, 255), 
                      size: int = 10, thickness: int = 1, fill: bool = False) -> 'Image':
        """
        在图像上画出一个特征点对象的各个点。
        color 是用于灰度或RGB565图像的RGB888元组。默认为白色。但是，您也可以传递灰度图像的基础像素值(0-255)或RGB565图像的字节反转RGB565值。
        size 控制特征点的大小。
        thickness 控制线的粗细像素。
        将 fill 设置为True以填充特征点。
        返回图像对象，以便您可以使用 . 表示法调用另一个方法。
        不支持压缩图像和bayer图像。
        """
        ...
    
    def flood_fill(self, *args: Any, seed_threshold: float = 0.05, floating_threshold: float = 0.05, 
                  color: Union[Tuple[int, int, int], int] = (255, 255, 255), invert: bool = False, 
                  clear_background: bool = False, mask: Optional['Image'] = None) -> 'Image':
        """
        从位置x，y开始填充图像的区域。 
        您可以单独传递x，y，也可以传递给元组(x，y)。
        seed_threshold 控制填充区域中的像素与原始起始像素的差异。
        floating_threshold 控制填充区域中的像素与任何相邻像素的差异。
        color 是用于灰度或RGB565图像的RGB888元组。默认为白色。但是，您也可以传递灰度图像的基础像素值(0-255)或RGB565图像的字节反转RGB565值。
        将 invert 传递为True，以重新填充flood_fill连接区域外的所有内容。
        将 clear_background 传递为True，将其余的flood_fill没有重新着色的像素归零。
        mask 是另一个用作绘图操作的像素级掩码的图像。掩码应该是一个只有黑色或白色像素的图像，并且应该与你正在绘制的 image 大小相同。 
        仅掩膜中设置的像素会在flood_fill时被评估。
        返回图像对象，以便您可以使用 . 表示法调用另一个方法。
        不支持压缩图像和bayer图像。
        此方法在OpenMV Cam M4 上不可用。
        """
        ...
    
    def binary(self, thresholds: List[Tuple], invert: bool = False, zero: bool = False, 
              mask: Optional['Image'] = None) -> 'Image':
        """
        根据像素是否在阈值列表 thresholds 中的阈值内，将图像中的所有像素设置为黑色或白色。
        thresholds 必须是元组列表。 [(lo, hi), (lo, hi), ..., (lo, hi)] 定义你想追踪的颜色范围。 
        对于灰度图像，每个元组需要包含两个值 - 最小灰度值和最大灰度值。 
        仅考虑落在这些阈值之间的像素区域。 
        对于RGB565图像，每个元组需要有六个值(l_lo，l_hi，a_lo，a_hi，b_lo，b_hi) - 分别是LAB L，A和B通道的最小值和最大值。 
        为方便使用，此功能将自动修复交换的最小值和最大值。 
        此外，如果元组大于六个值，则忽略其余值。相反，如果元组太短，则假定其余阈值处于最大范围。
        
        注解
        获取所跟踪对象的阈值，只需在 IDE 帧缓冲区中选择（单击并拖动）跟踪对象。 
        直方图会相应地更新到所在区域。然后只需写下颜色分布在每个直方图通道中起始与下降位置。 
        这些将是 thresholds 的低值和高值。 
        由于上下四分位数据相差微小，故手动确定阈值为佳。
        您还可以通过进入OpenMV IDE中的 工具 ->机器视觉 ->阈值编辑器 并从GUI窗口中拖动滑块来确定颜色阈值。
        
        invert 反转阈值操作，像素在已知颜色范围之外进行匹配，而非在已知颜色范围内。
        设置 zero 为True来使阈值像素为零，并使不在阈值列表中的像素保持不变。
        mask 是另一个用作绘图操作的像素级掩码的图像。掩码应该是一个只有黑色或白色像素的图像，并且应该与你正在绘制的 image 大小相同。 
        仅掩码中设置的像素被修改。
        返回图像对象，以便您可以使用 . 表示法调用另一个方法。
        不支持压缩图像和bayer图像。
        """
        ...
    
    def invert(self) -> 'Image':
        """
        将二进制图像0（黑色）变为1（白色），1（白色）变为0（黑色），非常快速地翻转二进制图像中的所有像素值。
        返回图像对象，以便您可以使用 . 表示法调用另一个方法。
        不支持压缩图像和Bayer图像。
        """
        ...
    
    # Many more image processing methods would be defined here...
    # I'm omitting them for brevity but they would all be included in the complete .pyi file
    
    def find_blobs(self, thresholds: List[Tuple], invert: bool = False, roi: Optional[Tuple[int, int, int, int]] = None, 
                  x_stride: int = 2, y_stride: int = 1, area_threshold: int = 10, pixels_threshold: int = 10, 
                  merge: bool = False, margin: int = 0, threshold_cb: Optional[Callable[['blob'], bool]] = None, 
                  merge_cb: Optional[Callable[['blob', 'blob'], bool]] = None) -> List['blob']:
        """
        查找图像中所有色块，并返回一个包括每个色块的色块对象的列表。请观察 image.blob 对象以获取更多信息。
        thresholds 必须是元组列表。 [(lo, hi), (lo, hi), ..., (lo, hi)] 定义你想追踪的颜色范围。 
        对于灰度图像，每个元组需要包含两个值 - 最小灰度值和最大灰度值。 
        仅考虑落在这些阈值之间的像素区域。 
        对于RGB565图像，每个元组需要有六个值(l_lo，l_hi，a_lo，a_hi，b_lo，b_hi) - 分别是LAB L，A和B通道的最小值和最大值。 
        为方便使用，此功能将自动修复交换的最小值和最大值。 
        此外，如果元组大于六个值，则忽略其余值。相反，如果元组太短，则假定其余阈值处于最大范围。
        
        注解
        获取所跟踪对象的阈值，只需在IDE帧缓冲区中选择（单击并拖动）跟踪对象。 
        直方图会相应地更新到所在区域。然后只需写下颜色分布在每个直方图通道中起始与下降位置。 
        这些将是 thresholds 的低值和高值。 
        由于上下四分位数据相差微小，故手动确定阈值为佳。
        您还可以通过进入OpenMV IDE中的 工具 ->机器视觉 ->阈值编辑器 并从GUI窗口中拖动滑块来确定颜色阈值。
        
        invert 反转阈值操作，像素在已知颜色范围之外进行匹配，而非在已知颜色范围内。
        roi 是感兴趣区域的矩形元组(x，y，w，h)。如果未指定，ROI即整个图像的图像矩形。 
        操作范围仅限于 roi 区域内的像素。
        x_stride 是查找某色块时需要跳过的x像素的数量。找到色块后，直线填充算法将精确像素。 
        若已知色块较大，可增加 x_stride 来提高查找色块的速度。
        y_stride 是查找某色块时需要跳过的y像素的数量。找到色块后，直线填充算法将精确像素。 
        若已知色块较大，可增加 y_stride 来提高查找色块的速度。
        若一个色块的边界框区域小于 area_threshold ，则会被过滤掉。
        若一个色块的像素数小于 pixel_threshold ，则会被过滤掉。
        merge 若为True，则合并所有没有被过滤掉的色块，这些色块的边界矩形互相交错重叠。 
        margin 可在相交测试中用来增大或减小色块边界矩形的大小。例如：边缘为1、相互间边界矩形为1的色块将被合并。
        合并色块使颜色代码追踪得以实现。每个色块对象有一个代码值 code ，该值为一个位向量。 
        例如：若您在 image.find_blobs 中输入两个颜色阈值，则第一个阈值代码为1，第二个代码为2（第三个代码为4，第四个代码为8，以此类推）。 
        合并色块对所有的code使用逻辑或运算，以便您知道产生它们的颜色。这使得您可以追踪两个颜色，若您用两种颜色得到一个色块对象，则可能是一种颜色代码。
        若您使用严格的颜色范围，无法完全追踪目标对象的所有像素，您可能需要合并色块。
        最后，若您想要合并色块，但不想两种不同阈值颜色的色块被合并，只需分别两次调用 image.find_blobs ，不同阈值色块就不会被合并。
        threshold_cb 可设置为用以调用阈值筛选后的每个色块的函数，以便将其从将要合并的色块列表中过滤出来。 
        回调函数将收到一个参数：要被筛选的色块对象。然后回调函数需返回True以保留色块或返回False以过滤色块。
        merge_cb 可设置为用以调用两个即将合并的色块的函数，以禁止或准许合并。回调函数将收到两个参数—两个将被合并的色块对象。 
        回调函数须返回True以合并色块，或返回False以防止色块合并。
        不支持压缩图像和bayer图像。
        """
        ...
    
    def find_lines(self, roi: Optional[Tuple[int, int, int, int]] = None, x_stride: int = 2, y_stride: int = 1, 
                  threshold: int = 1000, theta_margin: int = 25, rho_margin: int = 25) -> List['line']:
        """
        使用霍夫变换查找图像中的所有直线。返回一个 image.line 对象的列表。
        roi 是感兴趣区域的矩形元组(x，y，w，h)。如果未指定，ROI即整个图像的图像矩形。操作范围仅限于 roi 区域内的像素。
        x_stride 是霍夫变换时需要跳过的x像素的数量。若已知直线较大，可增加 x_stride 。
        y_stride 是霍夫变换时需要跳过的y像素的数量。若已知直线较大，可增加 y_stride 。
        threshold 控制从霍夫变换中监测到的直线。只返回大于或等于 threshold 的直线。 
        应用程序的正确的 threshold 值取决于图像。注意：一条直线的大小(magnitude)是组成直线所有索贝尔滤波像素大小的总和。
        theta_margin 控制所监测的直线的合并。 
        直线角度为 theta_margin 的部分和直线p值为 rho_margin 的部分合并。
        rho_margin 控制所监测的直线的合并。 
        直线角度为 theta_margin 的部分和直线p值为 rho_margin 的部分合并。
        该方法通过在图像上运行索贝尔滤波器，并利用该滤波器的幅值和梯度响应来进行霍夫变换。 
        无需对图像进行任何预处理。但是，清理图像过滤器可得到更为稳定的结果。
        不支持压缩图像和bayer图像。
        此方法在OpenMV Cam M4 上不可用。
        """
        ...
    
    def find_qrcodes(self, roi: Optional[Tuple[int, int, int, int]] = None) -> List['qrcode']:
        """
        查找 roi 内的所有二维码并返回一个 image.qrcode 对象的列表。 
        请参考 image.qrcode 对象以获取更多信息。
        为使这一方法成功运行，图像上二维码需比较平展。通过使用 sensor.set_windowing 函数在镜头中心放大、 
        image.lens_corr 函数来消解镜头的桶形畸变或通过更换视野较为狭小的镜头， 
        您可得到一个不受镜头畸变影响的更为平展的二维码。有些机器视觉镜头不会造成桶形失真，但是其造价远比OpenMV提供的标准镜片高，这种镜头为无畸变镜头。
        roi 是一个用以复制的矩形的感兴趣区域(x, y, w, h)。如果未指定，ROI即整幅图像的图像矩形。 
        操作范围仅限于 roi 区域内的像素。
        不支持压缩图像和bayer图像。
        此方法在OpenMV Cam M4 上不可用。
        """
        ...
    
    def find_apriltags(self, roi: Optional[Tuple[int, int, int, int]] = None, 
                      families: int = 0x00000008,  # TAG36H11
                      fx: Optional[float] = None, fy: Optional[float] = None, 
                      cx: Optional[float] = None, cy: Optional[float] = None) -> List['apriltag']:
        """
        查找 roi 内的所有AprilTag, 并返回一个 image.apriltag 对象的列表。请参考 image.apriltag 对象以获取更多信息。
        与二维码相比，AprilTags可在更远距离、较差光线和更扭曲的图像环境下被检测到。 
        AprilTags可应对所有种类的图像失真问题，而二维码并不能。也就是说，AprilTags只能将数字ID编码作为其有效载荷。
        AprilTags也可用于本地化。每个 image.apriltag 对象都从摄像机返回其三维位置信息和旋转角度。 
        位置信息由 fx 、 fy 、 cx 和 cy 决定，分别为X和Y方向上图像的焦距和中心点。
        使用OpenMV IDE内置的标签生成器工具来创建AprilTags。标签生成器可创建可打印的8.5"x11"AprilTags。
        roi 是一个用以复制的矩形的感兴趣区域(x, y, w, h)。如果未指定，ROI即整幅图像的图像矩形。 
        操作范围仅限于 roi 区域内的像素。
        families 是要解码的标签家族的位掩码。是一个逻辑或：
        image.TAG16H5
        image.TAG25H7
        image.TAG25H9
        image.TAG36H10
        image.TAG36H11
        image.ARTOOLKIT
        默认设置为最好用的 image.TAG36H11 标签家族。注意：每启用一个标签家族， find_apriltags 的速度都会略有放慢。
        fx 是以像素为单位的相机x方向的焦距。标准OpenMV Cam的值为(2.8 / 3.984) * 656， 
        该值通过毫米计的焦距值除以X方向上感光元件的长度，再乘以X方向上感光元件的像素数量得来（对OV7725感光元件而言）。
        fy 是以像素为单位的相机y方向的焦距。标准OpenMV Cam的值为(2.8 / 2.952) * 488， 
        该值通过毫米计的焦距值除以Y方向上感光元件的长度，再乘以Y方向上感光元件的像素数量得来（对OV7725感光元件而言）。
        cx 是图像的中心，即 image.width()/2 ，而非 roi.w()/2 。
        cy 是图像的中心，即 image.height()/2，而非 roi.h()/2 。
        不支持压缩图像和bayer图像。
        此方法在OpenMV Cam M4 上不可用。
        """
        ...

# Constants
SEARCH_EX = 0  # "详尽的模板匹配搜索。"
SEARCH_DS = 1  # "更快的模板匹配搜索。"
EDGE_CANNY = 2  # "使用Canny边缘检测算法对图像进行边缘检测。"
EDGE_SIMPLE = 3  # "使用阈值高通滤波算法对图像进行边缘检测。"
CORNER_FAST = 4  # "用于ORB键点的高速低准确率角点检测算法"
CORNER_AGAST = 5  # "用于ORB键点的低速高准确率算法。"
TAG16H5 = 1  # "TAG1H5标签群的位掩码枚举。用于AprilTags。"
TAG25H7 = 2  # "TAG25H7标签群的位掩码枚举。用于AprilTags。"
TAG25H9 = 4  # "TAG25H9标签群的位掩码枚举。用于AprilTags。"
TAG36H10 = 8  # "TAG36H10标签群的位掩码枚举。用于AprilTags。"
TAG36H11 = 16  # "TAG36H11标签群的位掩码枚举。用于AprilTags。"
ARTOOLKIT = 32  # "ARTOOLKIT标签群的位掩码枚举。用于AprilTags。"
EAN2 = 1  # "EAN2条形码类型枚举。"
EAN5 = 2  # "EAN5条形码类型枚举。"
EAN8 = 3  # "EAN8条形码类型枚举。"
UPCE = 4  # "UPCE条形码类型枚举。"
ISBN10 = 5  # "ISBN10条形码类型枚举。"
UPCA = 6  # "UPCA条形码类型枚举。"
EAN13 = 7  # "EAN13条形码类型枚举。"
ISBN13 = 8  # "ISBN13条形码类型枚举。"
I25 = 9  # "I25条形码类型枚举。"
DATABAR = 10  # "DATABAR条形码类型枚举。"
DATABAR_EXP = 11  # "DATABAR_EXP条形码类型枚举。"
CODABAR = 12  # "CODABAR条形码类型枚举。"
CODE39 = 13  # "CODE39条形码类型枚举。"
PDF417 = 14  # "PDF417条形码类型枚举（目前尚不能运行）。"
CODE93 = 15  # "CODE93条形码类型枚举。"
CODE128 = 16  # "CODE128条形码类型枚举。"