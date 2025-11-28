"""
Camera sensor module | 摄像头传感器模块

Sensor module for camera control, configuration, and image capture. Used to control
the development board camera to complete camera tasks.
| 传感器模块(这里特指摄像头模块)，进行摄像头配置及图像抓取等，用于控制开发板摄像头完成摄像任务。
"""

from typing import Optional, Tuple, Union, Any
import image

# Frame size constants | 帧大小常量
B40x30: int = 0     # 40x30 resolution | 40x30分辨率
QQVGA: int = 1      # 160x120 resolution | 160x120分辨率
QCIF: int = 2       # 176x144 resolution | 176x144分辨率
HQVGA: int = 3      # 240x160 resolution | 240x160分辨率
QVGA: int = 4       # 320x240 resolution | 320x240分辨率
CIF: int = 5        # 400x300 resolution | 400x300分辨率
HVGA: int = 6       # 480x320 resolution | 480x320分辨率
VGA: int = 7        # 640x480 resolution | 640x480分辨率
SVGA: int = 8       # 800x600 resolution | 800x600分辨率
XGA: int = 9        # 1024x768 resolution | 1024x768分辨率
SXGA: int = 10      # 1280x1024 resolution | 1280x1024分辨率
UXGA: int = 11      # 1600x1200 resolution | 1600x1200分辨率
HD: int = 12        # 1280x720 resolution | 1280x720分辨率
FHD: int = 13       # 1920x1080 resolution | 1920x1080分辨率
QHD: int = 14       # 2560x1440 resolution | 2560x1440分辨率
QXGA: int = 15      # 2048x1536 resolution | 2048x1536分辨率
WQXGA: int = 16     # 2560x1600 resolution | 2560x1600分辨率
WQXGA_PLUS: int = 17 # 2560x1920 resolution | 2560x1920分辨率
QSXGA: int = 18     # 2560x2048 resolution | 2560x2048分辨率
QUXGA: int = 19     # 3200x2400 resolution | 3200x2400分辨率
WQUXGA: int = 20    # 3840x2400 resolution | 3840x2400分辨率

# Pixel format constants | 像素格式常量
GRAYSCALE: int = 1  # 8-bit grayscale format | 8位灰度格式
RGB565: int = 2     # 16-bit RGB565 format | 16位RGB565格式
YUV422: int = 3     # YUV422 format | YUV422格式

# Camera type constants | 摄像头类型常量
OV_CAM: int = 1     # OV series cameras (e.g., OV2640, OV7740) | OV系列摄像头
GC_CAM: int = 2     # GC series cameras | GC系列摄像头
MT_CAM: int = 3     # MT series cameras | MT系列摄像头

def reset(freq: int = 24000000, set_regs: bool = True, 
         dual_buff: bool = False, choice: Optional[int] = None) -> None:
    """Reset and initialize single camera | 重置并初始化单目摄像头
    
    Args:
        freq: Camera clock frequency in Hz. Higher frequency gives higher frame rate
              but may reduce image quality. Default 24MHz. For cameras with color
              spots (ov7740), consider lowering to 20MHz.
              | 设置摄像头时钟频率，频率越高帧率越高，但是画质可能更差。
              默认24MHz，如果摄像头有彩色斑点(ov7740)，可以适当调低比如20MHz
        set_regs: Allow program to write camera registers. Default True. Set to False
                  if you need custom reset sequence, then use sensor.__write_reg()
                  | 允许程序写摄像头寄存器，默认为True。如果需要自定义复位序列，
                  可以设置为False，然后使用sensor.__write_reg(addr, value)函数
        dual_buff: Enable double buffering. Default False. Increases frame rate but
                   uses more memory (~384KiB)
                   | 默认为False。允许使用双缓冲，会增高帧率，但是内存占用也会增加(大约为384KiB)
        choice: Specify camera type to search for. OV type (1), GC type (2), MT type (3).
                If not specified, search all camera types.
                | 指定需要搜索的摄像头类型，ov类型(1)，gc类型(2)，mt类型(3)，
                不传入该参数则搜索全部类型摄像头
    
    Note:
        - Must be called before any other camera operations | 必须在任何其他摄像头操作之前调用
        - K210 supports up to VGA (640x480) resolution | K210最大支持VGA格式
    
    Example:
        sensor.reset()  # Default initialization | 默认初始化
        sensor.reset(freq=20000000)  # Lower frequency for OV7740 | 为OV7740降低频率
    """
    ...

def binocular_reset() -> None:
    """Reset and initialize binocular cameras | 重置并初始化双目摄像头
    
    K210 has only one DVP interface and can control only one sensor at a time.
    Use the shutdown() method to control the PWDN pin and select a specific sensor.
    After selecting a sensor, other operations remain unchanged.
    | K210只有一个DVP接口，同一时间只能控制一个Sensor。但是我们可以借助shutdown方法
    控制PWDN引脚以选择特定的Sensor。指定Sensor后其余操作不变。
    
    Note:
        - This is for dual-camera setups only | 仅适用于双摄像头设置
        - After reset, use shutdown() to select which camera to use | 复位后，使用shutdown()选择要使用的摄像头
    
    Example:
        sensor.binocular_reset()
        sensor.shutdown(0)  # Select camera 0 | 选择摄像头0
        sensor.set_pixformat(sensor.RGB565)
        sensor.set_framesize(sensor.QVGA)
    """
    ...

def set_framesize(framesize: int, set_regs: bool = True) -> bool:
    """Set camera frame size | 设置摄像头输出帧大小
    
    Sets the output frame size of the camera. K210 supports up to VGA format.
    MaixPy development boards have 320*240 resolution screens, QVGA format is recommended.
    | 用于设置摄像头输出帧大小，k210最大支持VGA格式，大于VGA将无法获取图像
    MaixPy开发板配置的屏幕是320*240分辨率，推荐设置为QVGA格式
    
    Args:
        framesize: Frame size constant | 帧大小
            - Common values: sensor.QVGA (320x240), sensor.VGA (640x480)
        set_regs: Allow program to write camera registers. Default True. Set to False
                  if you need custom frame size configuration sequence.
                  | 允许程序写摄像头寄存器，默认为True。如果需要自定义设置帧大小的序列，
                  可以设置为False，然后使用sensor.__write_reg(addr, value)函数
    
    Returns:
        True if successful, False if error | True: 设置成功, False: 设置错误
    
    Example:
        success = sensor.set_framesize(sensor.QVGA)  # 320x240
        if not success:
            print("Failed to set frame size")
    """
    ...

def set_pixformat(format: int, set_regs: bool = True) -> bool:
    """Set camera pixel format | 设置摄像头输出格式
    
    Sets the output pixel format of the camera. MaixPy development boards use RGB565
    format screens, so RGB565 format is recommended.
    | 用于设置摄像头输出格式
    MaixPy开发板配置的屏幕使用的是RGB565，推荐设置为RGB565格式
    
    Args:
        format: Pixel format constant | 帧格式
            - sensor.GRAYSCALE: 8-bit grayscale | 8位灰度
            - sensor.RGB565: 16-bit RGB565 (recommended) | 16位RGB565（推荐）
            - sensor.YUV422: YUV422 format | YUV422格式
        set_regs: Allow program to write camera registers. Default True. Set to False
                  if you need custom pixel format configuration sequence.
                  | 允许程序写摄像头寄存器，默认为True。如果需要自定义设置像素格式的序列，
                  可以设置为False，然后使用sensor.__write_reg(addr, value)函数
    
    Returns:
        True if successful, False if error | True: 设置成功, False: 设置错误
    
    Example:
        success = sensor.set_pixformat(sensor.RGB565)
        if not success:
            print("Failed to set pixel format")
    """
    ...

def run(enable: int) -> bool:
    """Control image capture | 图像捕捉功能控制
    
    Controls whether the camera captures images.
    | 图像捕捉功能控制
    
    Args:
        enable: 1 to start capturing images, 0 to stop capturing images
                | 1表示开始抓取图像，0表示停止抓取图像
    
    Returns:
        True if successful, False if error | True: 设置成功, False: 设置错误
    
    Example:
        sensor.run(1)  # Start capturing images | 开始抓取图像
        # ... do something ...
        sensor.run(0)  # Stop capturing images | 停止抓取图像
    """
    ...

def snapshot() -> image.Image:
    """Capture an image | 使用摄像头拍摄一张照片
    
    Captures a single image from the camera and returns it as an image object.
    | 使用摄像头拍摄一张照片
    
    Returns:
        Image object containing the captured frame | 返回的图像对象
    
    Note:
        - Must call sensor.run(1) before capturing images | 必须在捕获图像前调用sensor.run(1)
        - Blocks until frame is captured | 阻塞直到帧被捕获
    
    Example:
        img = sensor.snapshot()
        lcd.display(img)  # Display on LCD | 在LCD上显示
    """
    ...

def shutdown(enable_select: Union[bool, int]) -> None:
    """Control camera power/shutdown or switch between cameras | 关闭摄像头/切换摄像头
    
    For single camera: Controls camera power/shutdown state
    For dual cameras: Switches between camera sensors
    | 单目摄像头：控制摄像头开关
    双目摄像头：切换摄像头
    
    Args:
        enable_select: For single camera: True to enable camera, False to disable
                       For dual cameras: 0 to select camera 0, 1 to select camera 1
                       | 单目摄像头：True表示开启摄像头，False表示关闭摄像头
                       双目摄像头：通过写入0或1来切换摄像头
    
    Example:
        # Single camera | 单目摄像头
        sensor.shutdown(False)  # Turn off camera | 关闭摄像头
        sensor.shutdown(True)   # Turn on camera | 开启摄像头
        
        # Dual cameras | 双目摄像头
        sensor.shutdown(0)  # Select camera 0 | 选择摄像头0
        img0 = sensor.snapshot()
        sensor.shutdown(1)  # Select camera 1 | 选择摄像头1
        img1 = sensor.snapshot()
    """
    ...

def skip_frames(n: Optional[int] = None, time: Optional[int] = None) -> None:
    """Skip frames to stabilize camera | 跳过指定帧数或者跳过指定时间内的图像
    
    Skips specified number of frames or time duration to allow camera image to stabilize
    after changing camera settings.
    | 跳过指定帧数或者跳过指定时间内的图像，让相机图像在改变相机设置后稳定下来
    
    Args:
        n: Number of frames to skip | 跳过n帧图像
        time: Time duration to skip in milliseconds | 跳过指定时间，单位为ms
    
    Note:
        - If neither n nor time is specified, skips frames for 300ms | 
          若n和time皆未指定，该方法跳过300毫秒的帧
        - If both n and time are specified, skips n frames but returns after time ms | 
          若二者皆指定，该方法会跳过n数量的帧，但将在time毫秒后返回
    
    Example:
        sensor.skip_frames()  # Skip frames for 300ms (default) | 跳过300ms的帧(默认)
        sensor.skip_frames(n=10)  # Skip 10 frames | 跳过10帧
        sensor.skip_frames(time=500)  # Skip frames for 500ms | 跳过500ms的帧
        sensor.skip_frames(n=30, time=1000)  # Skip 30 frames but return after 1000ms | 跳过30帧但在1000ms后返回
    """
    ...

def width() -> int:
    """Get camera resolution width | 获取摄像头分辨率宽度
    
    Returns:
        Camera resolution width in pixels | 摄像头分辨率宽度
    
    Example:
        w = sensor.width()
        print(f"Camera width: {w} pixels")
    """
    ...

def height() -> int:
    """Get camera resolution height | 获取摄像头分辨率高度
    
    Returns:
        Camera resolution height in pixels | 摄像头分辨率高度
    
    Example:
        h = sensor.height()
        print(f"Camera height: {h} pixels")
    """
    ...

def get_fb() -> image.Image:
    """Get current frame buffer | 获取当前帧缓冲区
    
    Returns:
        Image object containing current frame buffer | image类型的对象
    
    Note:
        - This returns the same image as snapshot() but doesn't capture a new frame | 
          这返回与snapshot()相同的图像，但不捕获新帧
    
    Example:
        img = sensor.get_fb()
        lcd.display(img)
    """
    ...

def get_id() -> int:
    """Get camera ID | 获取当前摄像头ID
    
    Returns:
        Camera ID as integer | int类型的ID
    
    Note:
        - Must call after sensor.reset() to get valid ID | 需要在摄像头reset之后才能读取到id号
    
    Example:
        sensor.reset()
        cam_id = sensor.get_id()
        print(f"Camera ID: {cam_id}")
    """
    ...

def set_colorbar(enable: int) -> None:
    """Set camera color bar test mode | 将摄像头设置为彩条测试模式
    
    Enables color bar test pattern output. Used to check if camera bus is connected correctly.
    | 开启彩条测试模式后，摄像头会输出一彩条图像，常用来检测摄像机总线是否连接正确。
    
    Args:
        enable: 1 to enable color bar test mode, 0 to disable | 1表示开启彩条测试模式，0表示关闭彩条测试模式
    
    Example:
        sensor.set_colorbar(1)  # Enable color bar test | 开启彩条测试
        img = sensor.snapshot()
        lcd.display(img)  # Should show color bars | 应该显示彩条
        sensor.set_colorbar(0)  # Disable color bar test | 关闭彩条测试
    """
    ...

def set_contrast(contrast: int) -> bool:
    """Set camera contrast | 设置摄像头对比度
    
    Args:
        contrast: Camera contrast value, range [-2, +2] | 摄像头对比度，范围为[-2,+2]
            -2 = lowest contrast, +2 = highest contrast
    
    Returns:
        True if successful, False if error | True: 设置成功, False: 设置错误
    
    Example:
        success = sensor.set_contrast(1)  # Increase contrast | 增加对比度
    """
    ...

def set_brightness(brightness: int) -> bool:
    """Set camera brightness | 设置摄像头亮度
    
    Args:
        brightness: Camera brightness value, range [-2, +2] | 摄像头亮度，范围为[-2,+2]
            -2 = lowest brightness, +2 = highest brightness
    
    Returns:
        True if successful, False if error | True: 设置成功, False: 设置错误
    
    Example:
        success = sensor.set_brightness(0)  # Normal brightness | 正常亮度
    """
    ...

def set_saturation(saturation: int) -> bool:
    """Set camera saturation | 设置摄像头饱和度
    
    Args:
        saturation: Camera saturation value, range [-2, +2] | 摄像头饱和度，范围为[-2,+2]
            -2 = lowest saturation, +2 = highest saturation
    
    Returns:
        True if successful, False if error | True: 设置成功, False: 设置错误
    
    Example:
        success = sensor.set_saturation(1)  # Increase saturation | 增加饱和度
    """
    ...

def set_auto_gain(enable: int, gain_db: Optional[float] = None) -> None:
    """Set camera auto gain mode | 设置摄像自动增益模式
    
    Args:
        enable: 1 to enable auto gain, 0 to disable auto gain | 1表示开启自动增益，0表示关闭自动增益
        gain_db: Fixed gain value in dB when auto gain is disabled | 
                关闭自动增益时，设置的摄像头固定增益值，单位为dB
    
    Note:
        - For color tracking applications, disable auto gain | 如果需要追踪颜色，需要关闭自动增益
    
    Example:
        # Enable auto gain | 开启自动增益
        sensor.set_auto_gain(1)
        
        # Disable auto gain and set fixed gain to 10dB | 关闭自动增益并设置固定增益为10dB
        sensor.set_auto_gain(0, 10.0)
    """
    ...

def get_gain_db() -> float:
    """Get camera gain value | 获取摄像头增益值
    
    Returns:
        Camera gain value in dB | float类型的增益值
    
    Example:
        gain = sensor.get_gain_db()
        print(f"Current gain: {gain} dB")
    """
    ...

def set_hmirror(enable: int) -> None:
    """Set camera horizontal mirror | 设置摄像头水平镜像
    
    Args:
        enable: 1 to enable horizontal mirror, 0 to disable | 1表示开启水平镜像，0表示关闭水平镜像
    
    Example:
        sensor.set_hmirror(1)  # Enable horizontal mirror | 开启水平镜像
    """
    ...

def set_vflip(enable: int) -> None:
    """Set camera vertical flip | 设置摄像头垂直翻转
    
    Args:
        enable: 1 to enable vertical flip, 0 to disable | 1表示开启垂直翻转，0表示关闭垂直翻转
    
    Example:
        sensor.set_vflip(1)  # Enable vertical flip | 开启垂直翻转
    """
    ...

def __write_reg(address: int, value: int) -> None:
    """Write to camera register | 往摄像头寄存器写入指定值
    
    Args:
        address: Register address | 寄存器地址
        value: Value to write | 写入值
    
    Note:
        - Consult camera datasheet for register details | 请参阅摄像头数据手册以获取详细信息
        - Use with caution - incorrect values can damage camera | 谨慎使用 - 错误值可能损坏摄像头
    
    Example:
        # Example for OV2640 camera | OV2640摄像头示例
        sensor.__write_reg(0xFF, 0x01)  # Bank select | 银行选择
    """
    ...

def __read_reg(address: int) -> int:
    """Read from camera register | 读取摄像头寄存器值
    
    Args:
        address: Register address | 寄存器地址
    
    Returns:
        Register value as integer | int类型的寄存器值
    
    Note:
        - Consult camera datasheet for register details | 请参阅摄像头数据手册以获取详细信息
    
    Example:
        # Example for OV2640 camera | OV2640摄像头示例
        value = sensor.__read_reg(0x0A)  # Read product ID MSB | 读取产品ID MSB
        print(f"Register 0x0A value: {value:02X}")
    """
    ...

def set_jb_quality(quality: int) -> None:
    """Set image quality for IDE transfer | 设置传送给IDE图像的质量
    
    Args:
        quality: Image quality percentage (0-100), higher number = better quality | 
                int类型，图像质量百分比（0~100），数字越大质量越好
    
    Example:
        sensor.set_jb_quality(80)  # Set 80% quality for IDE transfer | 为IDE传输设置80%质量
    """
    ...