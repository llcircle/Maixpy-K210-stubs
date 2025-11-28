"""
LCD display module | LCD显示模块

Provides functions to control and display content on LCD screens | 提供控制LCD屏幕和显示内容的函数
"""

from typing import Optional, Tuple, Union, Any
import image

# Color constants | 颜色常量
BLACK: int = 0x0000   # Black color in RGB565 format | 黑色(RGB565格式)
WHITE: int = 0xFFFF   # White color in RGB565 format | 白色(RGB565格式)
RED: int = 0xF800     # Red color in RGB565 format | 红色(RGB565格式)
GREEN: int = 0x07E0   # Green color in RGB565 format | 绿色(RGB565格式)
BLUE: int = 0x001F    # Blue color in RGB565 format | 蓝色(RGB565格式)

# LCD types | LCD类型
LCD_TYPE_NONE: int = 0          # No LCD | 无LCD
LCD_TYPE_SHIELD: int = 1        # LCD Shield | LCD扩展板
LCD_TYPE_MAIX_CUBE: int = 2     # Maix Cube | Maix Cube开发板
LCD_TYPE_RGB_ADAPTER: int = 5   # Sipeed RGB screen adapter board | Sipeed RGB屏转接板

# LCD direction constants (deprecated) | LCD方向常量(已弃用)
YX_LRUD: int = 0  # Normal direction | 正常方向
YX_RLDU: int = 1  # Mirror direction | 镜像方向

def init(type: int = 1, freq: int = 15000000, color: Union[int, Tuple[int, int, int]] = BLACK, 
         invert: int = 0, lcd_type: int = 0) -> None:
    """Initialize LCD screen display | 初始化LCD屏幕显示
    
    Args:
        type: Device type (reserved for future use) | 设备类型(保留给未来使用)
            - 0: None | 无
            - 1: lcd shield (default) | lcd扩展板(默认)
            - 2: Maix Cube | Maix Cube开发板
            - 5: sipeed rgb screen adapter board | sipeed rgb屏转接板
        freq: LCD (SPI communication) frequency in Hz | LCD(SPI通讯速率)频率(Hz)
            - Default: 15000000 (15MHz) | 默认: 15000000 (15MHz)
        color: LCD initialization color | LCD初始化颜色
            - Can be 16-bit RGB565 value (e.g., 0xFFFF) | 可以是16位RGB565颜色值(例如0xFFFF)
            - Or RGB888 tuple (e.g., (236, 36, 36)) | 或RGB888元组(例如(236, 36, 36))
            - Default: lcd.BLACK | 默认: lcd.BLACK
        invert: LCD color inversion (0 = normal, 1 = inverted) | LCD反色显示(0=正常,1=反色)
        lcd_type: LCD panel type | LCD面板类型
            - 0: Default type | 默认类型
            - 1: LCD_TYPE_ILI9486 | ILI9486屏幕
            - 2: LCD_TYPE_ILI9481 | ILI9481屏幕
            - 3: LCD_TYPE_5P0_7P0 (800*480 resolution) | 5寸或7寸(800*480分辨率)
            - 4: LCD_TYPE_5P0_IPS (854*489 resolution) | 5寸IPS(854*489分辨率)
            - 5: LCD_TYPE_480_272_4P3 (480*272 resolution) | 4.3寸(480*272分辨率)
    
    Note:
        - MaixCube and MaixAmigo automatically configure power IC | 
          MaixCube和MaixAmigo会自动配置电源芯片，无需手动操作
        - `type` is a keyword-only parameter, must be called with `type=` | 
          `type`是键值参数，必须在函数调用中通过写入`type=`来显式地调用
    
    Example:
        lcd.init()  # Initialize with default settings | 使用默认设置初始化
        lcd.init(type=1, freq=20000000, color=lcd.WHITE)  # Custom initialization | 自定义初始化
        lcd.init(type=2)  # Initialize for Maix Cube | 为Maix Cube初始化
    """
    ...

def deinit() -> None:
    """Deinitialize LCD driver and release I/O pins | 注销LCD驱动，释放I/O引脚
    
    Stops LCD operation and releases all hardware resources associated with the LCD.
    | 停止LCD操作并释放与LCD关联的所有硬件资源。
    
    Example:
        lcd.deinit()  # Cleanup LCD resources | 清理LCD资源
    """
    ...

def width() -> int:
    """Get LCD width (horizontal resolution) | 返回LCD的宽度(水平分辨率)
    
    Returns:
        LCD width in pixels | LCD宽度(像素)
    
    Example:
        w = lcd.width()
        print(f"LCD width: {w} pixels")
    """
    ...

def height() -> int:
    """Get LCD height (vertical resolution) | 返回LCD的高度(垂直分辨率)
    
    Returns:
        LCD height in pixels | LCD高度(像素)
    
    Example:
        h = lcd.height()
        print(f"LCD height: {h} pixels")
    """
    ...

def type() -> int:
    """Get LCD type | 返回LCD的类型
    
    Returns:
        LCD type identifier | LCD类型标识符
            - 0: None | 无
            - 1: lcd Shield | LCD扩展板
    
    Note:
        This function is reserved for future use | 此函数保留给未来使用
    """
    ...

def freq(freq: Optional[int] = None) -> int:
    """Set or get LCD (SPI) frequency | 设置或者获取LCD(SPI)的频率
    
    Args:
        freq: LCD (SPI) frequency in Hz. If None, only get current frequency | 
             LCD(SPI)频率(Hz)。如果为None，仅获取当前频率
    
    Returns:
        Current LCD frequency in Hz | 当前LCD频率(Hz)
    
    Example:
        # Get current frequency | 获取当前频率
        current_freq = lcd.freq()
        print(f"Current LCD frequency: {current_freq} Hz")
        
        # Set new frequency to 20MHz | 设置新频率为20MHz
        lcd.freq(20000000)
        print(f"New LCD frequency: {lcd.freq()} Hz")
    """
    ...

def set_backlight(state: int) -> None:
    """Set LCD backlight state | 设置LCD的背光状态
    
    Controls the backlight brightness of the LCD screen. Turning off backlight can
    significantly reduce power consumption of the LCD expansion board.
    | 控制LCD屏幕的背光亮度。关闭背光会大大降低lcd扩展板的能耗。
    
    Args:
        state: Backlight brightness, range [0, 100] | 背光亮度，取值[0,100]
            - 0: Completely off | 完全关闭
            - 100: Maximum brightness | 最大亮度
    
    Note:
        This function is not implemented in current firmware | 此函数在当前固件中未实现
    
    Example:
        lcd.set_backlight(50)  # Set to 50% brightness | 设置为50%亮度
        lcd.set_backlight(0)   # Turn off backlight | 关闭背光
        lcd.set_backlight(100) # Maximum brightness | 最大亮度
    """
    ...

def get_backlight() -> int:
    """Get current backlight state | 返回背光状态
    
    Returns:
        Current backlight brightness, range [0, 100] | 当前背光亮度，取值[0,100]
    
    Example:
        brightness = lcd.get_backlight()
        print(f"Current backlight brightness: {brightness}%")
    """
    ...

def display(img: image.Image, roi: Optional[Tuple[int, int, int, int]] = None, 
            oft: Optional[Tuple[int, int]] = None) -> None:
    """Display an image on LCD screen | 在液晶屏上显示一张图像
    
    Displays an image (GRAYSCALE or RGB565 format) on the LCD screen with optional
    region of interest (ROI) and offset parameters.
    | 在LCD屏幕上显示图像(GRAYSCALE或RGB565格式)，可选感兴趣区域(ROI)和偏移参数。
    
    Args:
        img: Image object to display | 要显示的图像对象
        roi: Region of interest as (x, y, w, h) tuple. If None, uses full image | 
            感兴趣区域，格式为(x, y, w, h)元组。如果为None，使用完整图像
            - If roi width < LCD width: Centers roi with black borders | 
              如果roi宽度 < LCD宽度：居中roi，用黑色边框填充
            - If roi width > LCD width: Centers roi, crops excess pixels | 
              如果roi宽度 > LCD宽度：居中roi，裁剪多余像素
            - If roi height < LCD height: Centers roi with black borders | 
              如果roi高度 < LCD高度：居中roi，用黑色边框填充
            - If roi height > LCD height: Centers roi, crops excess pixels | 
              如果roi高度 > LCD高度：居中roi，裁剪多余像素
        oft: Offset coordinates as (x, y) tuple. If set, disables automatic centering | 
            偏移坐标，格式为(x, y)元组。如果设置，禁用自动居中
    
    Note:
        - `roi` is a keyword-only parameter, must be called with `roi=` | 
          `roi`是键值参数，必须在函数调用中通过写入`roi=`来显式地调用
    
    Example:
        # Display full image | 显示完整图像
        lcd.display(img)
        
        # Display specific region | 显示特定区域
        lcd.display(img, roi=(10, 20, 100, 150))
        
        # Display with offset | 带偏移显示
        lcd.display(img, oft=(50, 60))
    """
    ...

def clear(color: Union[int, Tuple[int, int, int]] = BLACK) -> None:
    """Clear LCD screen to black or specified color | 将液晶屏清空为黑色或者指定的颜色
    
    Args:
        color: Color to clear screen with | 用于清屏的颜色
            - Can be 16-bit RGB565 value (e.g., 0xFFFF) | 可以是16位RGB565颜色值(例如0xFFFF)
            - Or RGB888 tuple (e.g., (236, 36, 36)) | 或RGB888元组(例如(236, 36, 36))
            - Default: lcd.BLACK | 默认: lcd.BLACK
    
    Example:
        lcd.clear()  # Clear to black | 清空为黑色
        lcd.clear(lcd.WHITE)  # Clear to white | 清空为白色
        lcd.clear(0xF800)  # Clear to red (RGB565) | 清空为红色(RGB565)
        lcd.clear((255, 0, 0))  # Clear to red (RGB888) | 清空为红色(RGB888)
    """
    ...

def direction(dir: int) -> None:
    """Set screen direction and mirroring (deprecated) | 设置屏幕方向，以及是否镜像等(已弃用)
    
    Args:
        dir: Screen direction constant | 屏幕方向常量
            - Recommended: lcd.YX_LRUD or lcd.YX_RLDU | 推荐: lcd.YX_LRUD或lcd.YX_RLDU
            - Other values: Swap XY, LR, or DU | 其他值: 交换XY, LR, 或DU
    
    Note:
        - This function is deprecated since v0.3.1 | 此函数自v0.3.1后已被弃用
        - Use lcd.rotation() and lcd.mirror() instead | 请使用lcd.rotation()和lcd.mirror()代替
        - Interface is retained for debugging purposes | 接口仍会被保留用于调试使用
    
    Example:
        lcd.direction(lcd.YX_LRUD)  # Normal direction | 正常方向
        lcd.direction(lcd.YX_RLDU)  # Mirror direction | 镜像方向
    """
    ...

def rotation(dir: int) -> int:
    """Set LCD screen rotation direction | 设置LCD屏幕方向
    
    Rotates the screen display in 90-degree increments.
    | 以90度增量旋转屏幕显示。
    
    Args:
        dir: Rotation direction, range [0, 3] | 旋转方向，取值范围[0,3]
            - 0: 0 degrees (normal) | 0度(正常)
            - 1: 90 degrees clockwise | 90度顺时针
            - 2: 180 degrees | 180度
            - 3: 270 degrees clockwise | 270度顺时针
    
    Returns:
        Current rotation direction, range [0, 3] | 当前方向，取值[0,3]
    
    Example:
        current_dir = lcd.rotation(1)  # Rotate 90 degrees | 旋转90度
        print(f"Current rotation: {current_dir}")
    """
    ...

def mirror(invert: bool) -> bool:
    """Set LCD mirror display mode | 设置LCD是否镜面显示
    
    Args:
        invert: Whether to mirror display (True = mirror, False = normal) | 
               是否镜面显示(True=镜像, False=正常)
    
    Returns:
        Current mirror setting (True = mirror, False = normal) | 
        当前设置，是否镜面显示，返回True或者False
    
    Example:
        current_setting = lcd.mirror(True)  # Enable mirror mode | 启用镜像模式
        print(f"Mirror mode: {current_setting}")
        
        lcd.mirror(False)  # Disable mirror mode | 禁用镜像模式
    """
    ...

def bgr_to_rgb(enable: bool) -> None:
    """Enable or disable BGR color display | 设置是否启动bgr色彩显示
    
    Args:
        enable: Whether to enable BGR color format (True = BGR, False = RGB) | 
               是否启用BGR颜色格式(True=BGR, False=RGB)
    
    Example:
        lcd.bgr_to_rgb(True)  # Enable BGR format | 启用BGR格式
        lcd.bgr_to_rgb(False) # Disable BGR format (use RGB) | 禁用BGR格式(使用RGB)
    """
    ...

def fill_rectangle(x: int, y: int, w: int, h: int, color: Union[int, Tuple[int, int, int]]) -> None:
    """Fill a rectangular area on LCD | 填充LCD指定区域
    
    Args:
        x: Starting X coordinate | 起始坐标x
        y: Starting Y coordinate | 起始坐标y
        w: Rectangle width in pixels | 填充宽度
        h: Rectangle height in pixels | 填充高度
        color: Fill color | 填充颜色
            - Can be RGB888 tuple (e.g., (255, 255, 255)) | 可以是元组(例如(255, 255, 255))
            - Or RGB565 uint16 value (e.g., 0x00F8 for red) | 或RGB565 uint16值(例如红色0x00F8)
    
    Example:
        # Fill a red rectangle at position (10,20) with size 100x50 | 
        # 在位置(10,20)填充100x50大小的红色矩形
        lcd.fill_rectangle(10, 20, 100, 50, lcd.RED)
        
        # Fill a white rectangle using RGB888 format | 使用RGB888格式填充白色矩形
        lcd.fill_rectangle(30, 40, 80, 60, (255, 255, 255))
    """
    ...