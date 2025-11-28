"""
Maix module for K210 hardware control | K210硬件控制模块

Provides access to K210 specific hardware features including AI acceleration | 提供访问K210特定硬件功能，包括AI加速
"""

from typing import List, Tuple, Optional, Union, Callable, Dict, Any

class FPIOA:
    """Field Programmable Input and Output Array | 现场可编程IO阵列
    
    K210 supports mapping any peripheral to any pin using FPIOA functionality.
    | K210支持每个外设随意映射到任意引脚，使用FPIOA功能来实现。
    
    Note: The following GPIOHS pins are already used by default in MaixPy,
    avoid using them unless necessary:
    | 注意：以下GPIOHS默认已经被使用，程序中如非必要尽量不要使用：
    - GPIOHS5: LCD_DC (LCD read/write signal pin) | LCD读写信号引脚
    - GPIOHS4: LCD_RST (LCD reset pin) | LCD复位芯片脚  
    - GPIOHS29: SD_CS (SD card SPI chip select) | SD卡SPI片选
    - GPIOHS28: MIC_LED_CLK (SK9822_DAT) | SK9822_DAT
    - GPIOHS27: MIC_LED_DATA (SK9822_CLK) | SK9822_CLK
    """
    
    # FPIOA function constants | FPIOA功能常量
    
    # JTAG functions | JTAG功能
    JTAG_TCLK: int = 0   # JTAG Test Clock | JTAG测试时钟
    JTAG_TDI: int = 1    # JTAG Test Data In | JTAG测试数据输入
    JTAG_TMS: int = 2    # JTAG Test Mode Select | JTAG测试模式选择
    JTAG_TDO: int = 3    # JTAG Test Data Out | JTAG测试数据输出
    
    # SPI0 functions | SPI0功能
    SPI0_D0: int = 4     # SPI0 Data 0 | SPI0数据0
    SPI0_D1: int = 5     # SPI0 Data 1 | SPI0数据1
    SPI0_D2: int = 6     # SPI0 Data 2 | SPI0数据2
    SPI0_D3: int = 7     # SPI0 Data 3 | SPI0数据3
    SPI0_D4: int = 8     # SPI0 Data 4 | SPI0数据4
    SPI0_D5: int = 9     # SPI0 Data 5 | SPI0数据5
    SPI0_D6: int = 10    # SPI0 Data 6 | SPI0数据6
    SPI0_D7: int = 11    # SPI0 Data 7 | SPI0数据7
    SPI0_SS0: int = 12   # SPI0 Chip Select 0 | SPI0片选0
    SPI0_SS1: int = 13   # SPI0 Chip Select 1 | SPI0片选1
    SPI0_SS2: int = 14   # SPI0 Chip Select 2 | SPI0片选2
    SPI0_SS3: int = 15   # SPI0 Chip Select 3 | SPI0片选3
    SPI0_ARB: int = 16   # SPI0 Arbitration | SPI0仲裁
    SPI0_SCLK: int = 17  # SPI0 Serial Clock | SPI0串行时钟
    
    # UARTHS functions | UARTHS功能
    UARTHS_RX: int = 18  # UART High speed Receiver | UART高速接收器
    UARTHS_TX: int = 19  # UART High speed Transmitter | UART高速发射器
    
    # Reserved functions | 保留功能
    RESV6: int = 20      # Reserved function | 保留功能
    RESV7: int = 21      # Reserved function | 保留功能
    
    # Clock functions | 时钟功能
    CLK_SPI1: int = 22   # Clock SPI1 | SPI1时钟
    CLK_I2C1: int = 23   # Clock I2C1 | I2C1时钟
    
    # GPIOHS functions (0-31) | GPIOHS功能(0-31)
    GPIOHS0: int = 24    # GPIO High speed 0 | GPIO高速0
    GPIOHS1: int = 25    # GPIO High speed 1 | GPIO高速1
    GPIOHS2: int = 26    # GPIO High speed 2 | GPIO高速2
    GPIOHS3: int = 27    # GPIO High speed 3 | GPIO高速3
    GPIOHS4: int = 28    # GPIO High speed 4 | GPIO高速4 (LCD_RST - avoid using)
    GPIOHS5: int = 29    # GPIO High speed 5 | GPIO高速5 (LCD_DC - avoid using)
    GPIOHS6: int = 30    # GPIO High speed 6 | GPIO高速6
    GPIOHS7: int = 31    # GPIO High speed 7 | GPIO高速7
    GPIOHS8: int = 32    # GPIO High speed 8 | GPIO高速8
    GPIOHS9: int = 33    # GPIO High speed 9 | GPIO高速9
    GPIOHS10: int = 34   # GPIO High speed 10 | GPIO高速10
    GPIOHS11: int = 35   # GPIO High speed 11 | GPIO高速11
    GPIOHS12: int = 36   # GPIO High speed 12 | GPIO高速12
    GPIOHS13: int = 37   # GPIO High speed 13 | GPIO高速13
    GPIOHS14: int = 38   # GPIO High speed 14 | GPIO高速14
    GPIOHS15: int = 39   # GPIO High speed 15 | GPIO高速15
    GPIOHS16: int = 40   # GPIO High speed 16 | GPIO高速16
    GPIOHS17: int = 41   # GPIO High speed 17 | GPIO高速17
    GPIOHS18: int = 42   # GPIO High speed 18 | GPIO高速18
    GPIOHS19: int = 43   # GPIO High speed 19 | GPIO高速19
    GPIOHS20: int = 44   # GPIO High speed 20 | GPIO高速20
    GPIOHS21: int = 45   # GPIO High speed 21 | GPIO高速21
    GPIOHS22: int = 46   # GPIO High speed 22 | GPIO高速22
    GPIOHS23: int = 47   # GPIO High speed 23 | GPIO高速23
    GPIOHS24: int = 48   # GPIO High speed 24 | GPIO高速24
    GPIOHS25: int = 49   # GPIO High speed 25 | GPIO高速25
    GPIOHS26: int = 50   # GPIO High speed 26 | GPIO高速26
    GPIOHS27: int = 51   # GPIO High speed 27 | GPIO高速27 (MIC_LED_DATA - avoid using)
    GPIOHS28: int = 52   # GPIO High speed 28 | GPIO高速28 (MIC_LED_CLK - avoid using)
    GPIOHS29: int = 53   # GPIO High speed 29 | GPIO高速29 (SD_CS - avoid using)
    GPIOHS30: int = 54   # GPIO High speed 30 | GPIO高速30
    GPIOHS31: int = 55   # GPIO High speed 31 | GPIO高速31
    
    # GPIO functions (0-7) | GPIO功能(0-7)
    GPIO0: int = 56      # GPIO pin 0 | GPIO引脚0
    GPIO1: int = 57      # GPIO pin 1 | GPIO引脚1
    GPIO2: int = 58      # GPIO pin 2 | GPIO引脚2
    GPIO3: int = 59      # GPIO pin 3 | GPIO引脚3
    GPIO4: int = 60      # GPIO pin 4 | GPIO引脚4
    GPIO5: int = 61      # GPIO pin 5 | GPIO引脚5
    GPIO6: int = 62      # GPIO pin 6 | GPIO引脚6
    GPIO7: int = 63      # GPIO pin 7 | GPIO引脚7
    
    # UART functions | UART功能
    UART1_RX: int = 64   # UART1 Receiver | UART1接收器
    UART1_TX: int = 65   # UART1 Transmitter | UART1发射器
    UART2_RX: int = 66   # UART2 Receiver | UART2接收器
    UART2_TX: int = 67   # UART2 Transmitter | UART2发射器
    UART3_RX: int = 68   # UART3 Receiver | UART3接收器
    UART3_TX: int = 69   # UART3 Transmitter | UART3发射器
    
    # SPI1 functions | SPI1功能
    SPI1_D0: int = 70    # SPI1 Data 0 | SPI1数据0
    SPI1_D1: int = 71    # SPI1 Data 1 | SPI1数据1
    SPI1_D2: int = 72    # SPI1 Data 2 | SPI1数据2
    SPI1_D3: int = 73    # SPI1 Data 3 | SPI1数据3
    SPI1_D4: int = 74    # SPI1 Data 4 | SPI1数据4
    SPI1_D5: int = 75    # SPI1 Data 5 | SPI1数据5
    SPI1_D6: int = 76    # SPI1 Data 6 | SPI1数据6
    SPI1_D7: int = 77    # SPI1 Data 7 | SPI1数据7
    SPI1_SS0: int = 78   # SPI1 Chip Select 0 | SPI1片选0
    SPI1_SS1: int = 79   # SPI1 Chip Select 1 | SPI1片选1
    SPI1_SS2: int = 80   # SPI1 Chip Select 2 | SPI1片选2
    SPI1_SS3: int = 81   # SPI1 Chip Select 3 | SPI1片选3
    SPI1_ARB: int = 82   # SPI1 Arbitration | SPI1仲裁
    SPI1_SCLK: int = 83  # SPI1 Serial Clock | SPI1串行时钟
    
    # SPI Slave functions | SPI从机功能
    SPI_SLAVE_D0: int = 84    # SPI Slave Data 0 | SPI从机数据0
    SPI_SLAVE_SS: int = 85    # SPI Slave Select | SPI从机选择
    SPI_SLAVE_SCLK: int = 86  # SPI Slave Serial Clock | SPI从机串行时钟
    
    # I2S0 functions | I2S0功能
    I2S0_MCLK: int = 87       # I2S0 Master Clock | I2S0主时钟
    I2S0_SCLK: int = 88       # I2S0 Serial Clock(BCLK) | I2S0串行时钟(BCLK)
    I2S0_WS: int = 89         # I2S0 Word Select(LRCLK) | I2S0字选择(LRCLK)
    I2S0_IN_D0: int = 90      # I2S0 Serial Data Input 0 | I2S0串行数据输入0
    I2S0_IN_D1: int = 91      # I2S0 Serial Data Input 1 | I2S0串行数据输入1
    I2S0_IN_D2: int = 92      # I2S0 Serial Data Input 2 | I2S0串行数据输入2
    I2S0_IN_D3: int = 93      # I2S0 Serial Data Input 3 | I2S0串行数据输入3
    I2S0_OUT_D0: int = 94     # I2S0 Serial Data Output 0 | I2S0串行数据输出0
    I2S0_OUT_D1: int = 95     # I2S0 Serial Data Output 1 | I2S0串行数据输出1
    I2S0_OUT_D2: int = 96     # I2S0 Serial Data Output 2 | I2S0串行数据输出2
    I2S0_OUT_D3: int = 97     # I2S0 Serial Data Output 3 | I2S0串行数据输出3
    
    # I2S1 functions | I2S1功能
    I2S1_MCLK: int = 98       # I2S1 Master Clock | I2S1主时钟
    I2S1_SCLK: int = 99       # I2S1 Serial Clock(BCLK) | I2S1串行时钟(BCLK)
    I2S1_WS: int = 100        # I2S1 Word Select(LRCLK) | I2S1字选择(LRCLK)
    I2S1_IN_D0: int = 101     # I2S1 Serial Data Input 0 | I2S1串行数据输入0
    I2S1_IN_D1: int = 102     # I2S1 Serial Data Input 1 | I2S1串行数据输入1
    I2S1_IN_D2: int = 103     # I2S1 Serial Data Input 2 | I2S1串行数据输入2
    I2S1_IN_D3: int = 104     # I2S1 Serial Data Input 3 | I2S1串行数据输入3
    I2S1_OUT_D0: int = 105    # I2S1 Serial Data Output 0 | I2S1串行数据输出0
    I2S1_OUT_D1: int = 106    # I2S1 Serial Data Output 1 | I2S1串行数据输出1
    I2S1_OUT_D2: int = 107    # I2S1 Serial Data Output 2 | I2S1串行数据输出2
    I2S1_OUT_D3: int = 108    # I2S1 Serial Data Output 3 | I2S1串行数据输出3
    
    # I2S2 functions | I2S2功能
    I2S2_MCLK: int = 109      # I2S2 Master Clock | I2S2主时钟
    I2S2_SCLK: int = 110      # I2S2 Serial Clock(BCLK) | I2S2串行时钟(BCLK)
    I2S2_WS: int = 111        # I2S2 Word Select(LRCLK) | I2S2字选择(LRCLK)
    I2S2_IN_D0: int = 112     # I2S2 Serial Data Input 0 | I2S2串行数据输入0
    I2S2_IN_D1: int = 113     # I2S2 Serial Data Input 1 | I2S2串行数据输入1
    I2S2_IN_D2: int = 114     # I2S2 Serial Data Input 2 | I2S2串行数据输入2
    I2S2_IN_D3: int = 115     # I2S2 Serial Data Input 3 | I2S2串行数据输入3
    I2S2_OUT_D0: int = 116    # I2S2 Serial Data Output 0 | I2S2串行数据输出0
    I2S2_OUT_D1: int = 117    # I2S2 Serial Data Output 1 | I2S2串行数据输出1
    I2S2_OUT_D2: int = 118    # I2S2 Serial Data Output 2 | I2S2串行数据输出2
    I2S2_OUT_D3: int = 119    # I2S2 Serial Data Output 3 | I2S2串行数据输出3
    
    # Reserved functions | 保留功能
    RESV0: int = 120         # Reserved function | 保留功能
    RESV1: int = 121         # Reserved function | 保留功能
    RESV2: int = 122         # Reserved function | 保留功能
    RESV3: int = 123         # Reserved function | 保留功能
    RESV4: int = 124         # Reserved function | 保留功能
    RESV5: int = 125         # Reserved function | 保留功能
    
    # I2C functions | I2C功能
    I2C0_SCLK: int = 126     # I2C0 Serial Clock | I2C0串行时钟
    I2C0_SDA: int = 127      # I2C0 Serial Data | I2C0串行数据
    I2C1_SCLK: int = 128     # I2C1 Serial Clock | I2C1串行时钟
    I2C1_SDA: int = 129      # I2C1 Serial Data | I2C1串行数据
    I2C2_SCLK: int = 130     # I2C2 Serial Clock | I2C2串行时钟
    I2C2_SDA: int = 131      # I2C2 Serial Data | I2C2串行数据
    
    # CMOS/DVP camera functions | CMOS/DVP摄像头功能
    CMOS_XCLK: int = 132     # DVP System Clock | DVP系统时钟
    CMOS_RST: int = 133      # DVP System Reset | DVP系统复位
    CMOS_PWDN: int = 134     # DVP Power Down Mode | DVP掉电模式
    CMOS_VSYNC: int = 135    # DVP Vertical Sync | DVP垂直同步
    CMOS_HREF: int = 136     # DVP Horizontal Reference output | DVP水平参考输出
    CMOS_PCLK: int = 137     # Pixel Clock | 像素时钟
    CMOS_D0: int = 138       # Data Bit 0 | 数据位0
    CMOS_D1: int = 139       # Data Bit 1 | 数据位1
    CMOS_D2: int = 140       # Data Bit 2 | 数据位2
    CMOS_D3: int = 141       # Data Bit 3 | 数据位3
    CMOS_D4: int = 142       # Data Bit 4 | 数据位4
    CMOS_D5: int = 143       # Data Bit 5 | 数据位5
    CMOS_D6: int = 144       # Data Bit 6 | 数据位6
    CMOS_D7: int = 145       # Data Bit 7 | 数据位7
    
    # SCCB functions (for camera) | SCCB功能(用于摄像头)
    SCCB_SCLK: int = 146     # SCCB Serial Clock | SCCB串行时钟
    SCCB_SDA: int = 147      # SCCB Serial Data | SCCB串行数据
    
    # Additional UART and timer functions are defined in the full table...
    # (Complete list continues with all functions from the documentation)
    
    def __init__(self) -> None:
        """Initialize FPIOA controller | 初始化FPIOA控制器
        
        Example:
            from Maix import FPIOA
            fpioa = FPIOA()
        """
        ...
    
    def help(self, func: Optional[int] = None) -> str:
        """Display peripheral functions and their descriptions | 显示外设及其简要描述
        
        Args:
            func: Peripheral function number. If None, displays all functions in table format | 
                 外设功能编号。如果为None，则以表格形式显示所有功能
                - Example values: FPIOA.JTAG_TCLK, 0, fm.fpioa.GPIOHS0 | 示例值
        
        Returns:
            Function name and description as string | 外设名及其简要描述
        
        Example:
            # Display all functions | 显示所有功能
            fpioa.help()
            
            # Display specific function | 显示特定功能
            fpioa.help(FPIOA.JTAG_TCLK)
            fpioa.help(0)
        """
        ...
    
    def set_function(self, pin: int, func: int) -> None:
        """Set pin mapping to peripheral function | 设置引脚对应的外设功能
        
        Maps a physical pin to a specific peripheral function | 将物理引脚映射到特定的外设功能
        
        Args:
            pin: Pin number [0, 47] | 引脚编号 [0, 47]
                - Can use board_info.LED_G, board_info.BOOT_KEY, etc. | 可以使用board_info.LED_G, board_info.BOOT_KEY等
            func: Peripheral function constant | 外设功能常量
                - Example: FPIOA.GPIOHS0, FPIOA.UART1_TX, fm.fpioa.SPI0_SCLK | 示例
        
        Example:
            from Maix import FPIOA
            from board import board_info
            
            fpioa = FPIOA()
            # Map green LED pin to high-speed GPIO0 | 将绿色LED引脚映射到高速GPIO0
            fpioa.set_function(board_info.LED_G, FPIOA.GPIOHS0)
        """
        ...
    
    def get_Pin_num(self, func: int) -> int:
        """Get pin number mapped to peripheral function | 获取外设映射到哪个引脚上了
        
        Args:
            func: Peripheral function constant | 外设功能常量
                - Example: FPIOA.GPIOHS0, FPIOA.UART1_RX | 示例
        
        Returns:
            Pin number that the function is mapped to | 该功能映射到的引脚编号
        
        Raises:
            ValueError: If function is not mapped to any pin | 如果功能未映射到任何引脚
        
        Example:
            fpioa = FPIOA()
            fpioa.set_function(12, FPIOA.GPIOHS0)
            pin = fpioa.get_Pin_num(FPIOA.GPIOHS0)
            if pin == 12:
                print("Function mapped correctly")
        """
        ...


class GPIO:
    """General Purpose Input Output | 通用输入/输出
    
    K210 has two types of GPIO:
    - High-speed GPIO (GPIOHS): 32 channels with independent interrupt sources
    - General GPIO: 8 channels sharing one interrupt source
    | K210上有两种GPIO：
    - 高速GPIO(GPIOHS)：32个通道，每个都有独立中断源
    - 通用GPIO：8个通道，共享一个中断源
    
    Features:
    - Each IO can be assigned to any of the 48 FPIOA pins | 每个IO可以分配到FPIOA上48个管脚之一
    - Configurable input/output signals | 可配置输入输出信号
    - Interrupt support (edge/level triggered) | 中断支持（边沿/电平触发）
    - Configurable pull-up/pull-down/high-impedance | 可配置上下拉，或者高阻
    
    Note: The following GPIOHS pins are already used by default in MaixPy,
    avoid using them unless necessary:
    | 注意：以下GPIOHS默认已经被使用，程序中如非必要尽量不要使用：
    - GPIOHS31: LCD_DC | LCD读写信号引脚
    - GPIOHS30: LCD_RST | LCD复位芯片脚
    - GPIOHS29: SD_CS | SD卡SPI片选
    - GPIOHS28: MIC_LED_CLK | SK9822_DAT
    - GPIOHS27: MIC_LED_DATA | SK9822_CLK
    """
    
    # General GPIO constants (8 channels) | 通用GPIO常量(8个通道)
    GPIO0: int = 0   # GPIO pin 0 | GPIO引脚0
    GPIO1: int = 1   # GPIO pin 1 | GPIO引脚1
    GPIO2: int = 2   # GPIO pin 2 | GPIO引脚2
    GPIO3: int = 3   # GPIO pin 3 | GPIO引脚3
    GPIO4: int = 4   # GPIO pin 4 | GPIO引脚4
    GPIO5: int = 5   # GPIO pin 5 | GPIO引脚5
    GPIO6: int = 6   # GPIO pin 6 | GPIO引脚6
    GPIO7: int = 7   # GPIO pin 7 | GPIO引脚7
    
    # High-speed GPIO constants (32 channels) | 高速GPIO常量(32个通道)
    GPIOHS0: int = 8    # GPIO High speed 0 | GPIO高速0
    GPIOHS1: int = 9    # GPIO High speed 1 | GPIO高速1
    GPIOHS2: int = 10   # GPIO High speed 2 | GPIO高速2
    GPIOHS3: int = 11   # GPIO High speed 3 | GPIO高速3
    GPIOHS4: int = 12   # GPIO High speed 4 | GPIO高速4
    GPIOHS5: int = 13   # GPIO High speed 5 | GPIO高速5 (LCD_DC - avoid using)
    GPIOHS6: int = 14   # GPIO High speed 6 | GPIO高速6
    GPIOHS7: int = 15   # GPIO High speed 7 | GPIO高速7
    GPIOHS8: int = 16   # GPIO High speed 8 | GPIO高速8
    GPIOHS9: int = 17   # GPIO High speed 9 | GPIO高速9
    GPIOHS10: int = 18  # GPIO High speed 10 | GPIO高速10
    GPIOHS11: int = 19  # GPIO High speed 11 | GPIO高速11
    GPIOHS12: int = 20  # GPIO High speed 12 | GPIO高速12
    GPIOHS13: int = 21  # GPIO High speed 13 | GPIO高速13
    GPIOHS14: int = 22  # GPIO High speed 14 | GPIO高速14
    GPIOHS15: int = 23  # GPIO High speed 15 | GPIO高速15
    GPIOHS16: int = 24  # GPIO High speed 16 | GPIO高速16
    GPIOHS17: int = 25  # GPIO High speed 17 | GPIO高速17
    GPIOHS18: int = 26  # GPIO High speed 18 | GPIO高速18
    GPIOHS19: int = 27  # GPIO High speed 19 | GPIO高速19
    GPIOHS20: int = 28  # GPIO High speed 20 | GPIO高速20
    GPIOHS21: int = 29  # GPIO High speed 21 | GPIO高速21
    GPIOHS22: int = 30  # GPIO High speed 22 | GPIO高速22
    GPIOHS23: int = 31  # GPIO High speed 23 | GPIO高速23
    GPIOHS24: int = 32  # GPIO High speed 24 | GPIO高速24
    GPIOHS25: int = 33  # GPIO High speed 25 | GPIO高速25
    GPIOHS26: int = 34  # GPIO High speed 26 | GPIO高速26
    GPIOHS27: int = 35  # GPIO High speed 27 | GPIO高速27 (MIC_LED_DATA - avoid using)
    GPIOHS28: int = 36  # GPIO High speed 28 | GPIO高速28 (MIC_LED_CLK - avoid using)
    GPIOHS29: int = 37  # GPIO High speed 29 | GPIO高速29 (SD_CS - avoid using)
    GPIOHS30: int = 38  # GPIO High speed 30 | GPIO高速30 (LCD_RST - avoid using)
    GPIOHS31: int = 39  # GPIO High speed 31 | GPIO高速31 (LCD_DC - avoid using)
    
    # GPIO modes | GPIO模式
    IN: int = 0        # Input mode | 输入模式
    OUT: int = 1       # Output mode | 输出模式
    
    # Pull modes | 上下拉模式
    PULL_UP: int = 2   # Pull-up resistor enabled | 上拉电阻启用
    PULL_DOWN: int = 3 # Pull-down resistor enabled | 下拉电阻启用
    PULL_NONE: int = 4 # No pull-up/pull-down (high impedance) | 无上下拉（高阻态）
    
    # Interrupt trigger conditions | 中断触发条件
    IRQ_RISING: int = 0    # Rising edge triggered | 上升沿触发
    IRQ_FALLING: int = 1   # Falling edge triggered | 下降沿触发
    IRQ_BOTH: int = 2      # Both edges triggered | 上升沿和下降沿都触发
    
    # Wakeup support constants | 唤醒支持常量
    WAKEUP_NOT_SUPPORT: int = 0  # Wakeup not supported | 不支持唤醒
    
    def __init__(self, id: int, mode: int, pull: Optional[int] = None, value: Optional[int] = None) -> None:
        """Initialize GPIO pin | 初始化GPIO引脚
        
        Args:
            id: GPIO pin identifier using GPIO constants | GPIO引脚标识符，使用GPIO类中的常量
                - General GPIO: GPIO.GPIO0 to GPIO.GPIO7 | 通用GPIO: GPIO.GPIO0到GPIO.GPIO7
                - High-speed GPIO: GPIO.GPIOHS0 to GPIO.GPIOHS31 | 高速GPIO: GPIO.GPIOHS0到GPIO.GPIOHS31
            mode: GPIO mode (GPIO.IN or GPIO.OUT) | GPIO模式(GPIO.IN或GPIO.OUT)
            pull: Pull mode (GPIO.PULL_UP, GPIO.PULL_DOWN, GPIO.PULL_NONE) | 上下拉模式
                - Only applicable for input mode | 仅适用于输入模式
                - Default: GPIO.PULL_NONE | 默认: GPIO.PULL_NONE
            value: Initial value for output mode (0 or 1) | 输出模式的初始值(0或1)
                - Only applicable for output mode | 仅适用于输出模式
                - Default: 0 (low) | 默认: 0 (低电平)
        
        Note:
            - Must use FPIOA to map GPIO to physical pins first | 必须先使用FPIOA将GPIO映射到物理引脚
            - Only GPIOHS supports interrupts | 只有GPIOHS支持中断
            - Avoid using reserved GPIOHS pins unless necessary | 避免使用保留的GPIOHS引脚，除非必要
        
        Example:
            from Maix import GPIO
            from fpioa_manager import fm
            from board import board_info
            
            # Map LED pin to GPIO0 | 将LED引脚映射到GPIO0
            fm.register(board_info.LED_R, fm.fpioa.GPIO0)
            led = GPIO(GPIO.GPIO0, GPIO.OUT)
            
            # Map button pin to GPIOHS0 | 将按键引脚映射到GPIOHS0
            fm.register(board_info.BOOT_KEY, fm.fpioa.GPIOHS0)
            key = GPIO(GPIO.GPIOHS0, GPIO.IN, GPIO.PULL_NONE)
        """
        ...
    
    def value(self, value: Optional[int] = None) -> int:
        """Get or set GPIO pin state | 读取/设置GPIO引脚状态
        
        Args:
            value: Value to set (0 or 1), if None then only read current state | 
                 要设置的值(0或1)，如果为None则只读取当前状态
        
        Returns:
            Current GPIO pin state (0 or 1) | 当前GPIO引脚状态(0或1)
        
        Example:
            # Read GPIO state | 读取GPIO状态
            state = gpio.value()
            print(f"GPIO state: {state}")
            
            # Set GPIO high | 设置GPIO高电平
            gpio.value(1)
            
            # Set GPIO low | 设置GPIO低电平
            gpio.value(0)
        """
        ...
    
    def irq(self, callback: Callable[[int], None], trigger: int, 
           wakeup: int = WAKEUP_NOT_SUPPORT, priority: int = 7) -> None:
        """Configure interrupt handler | 配置中断处理程序
        
        Sets up an interrupt handler that will be called when the trigger condition is met.
        Only GPIOHS pins support interrupts.
        | 配置中断处理程序，当触发条件满足时调用。只有GPIOHS引脚支持中断。
        
        Args:
            callback: Interrupt callback function | 中断回调函数
                - Signature: def callback(pin_num: int) -> None | 签名
                - pin_num: GPIOHS pin number that triggered the interrupt | 触发中断的GPIOHS引脚号
            trigger: Interrupt trigger condition | 中断触发条件
                - GPIO.IRQ_RISING: Rising edge triggered | 上升沿触发
                - GPIO.IRQ_FALLING: Falling edge triggered | 下降沿触发
                - GPIO.IRQ_BOTH: Both edges triggered | 上升沿和下降沿都触发
            wakeup: Wakeup support (currently not supported) | 唤醒支持（当前不支持）
                - Default: GPIO.WAKEUP_NOT_SUPPORT | 默认: GPIO.WAKEUP_NOT_SUPPORT
            priority: Interrupt priority (1-7, 1=highest, 7=lowest) | 中断优先级(1-7, 1=最高, 7=最低)
                - Default: 7 (lowest priority) | 默认: 7 (最低优先级)
        
        Note:
            - Only GPIOHS pins support interrupts | 只有GPIOHS引脚支持中断
            - Callback function is called in interrupt context | 回调函数在中断上下文中调用
            - Avoid long operations in callback function | 避免在回调函数中执行长时间操作
        
        Example:
            def button_callback(pin_num):
                print(f"Button pressed on pin {pin_num}")
            
            # Configure interrupt for button press | 为按键按下配置中断
            key.irq(button_callback, GPIO.IRQ_FALLING, GPIO.WAKEUP_NOT_SUPPORT, 7)
        """
        ...
    
    def disirq(self) -> None:
        """Disable interrupt | 关闭中断
        
        Disables the interrupt handler for this GPIO pin.
        | 禁用此GPIO引脚的中断处理程序。
        
        Example:
            key.disirq()  # Disable button interrupt | 禁用按键中断
        """
        ...
    
    def mode(self, mode: int) -> None:
        """Set GPIO input/output mode | 设置GPIO输入输出模式
        
        Args:
            mode: GPIO mode | GPIO模式
                - GPIO.IN: Input mode | 输入模式
                - GPIO.PULL_UP: Pull-up input mode | 上拉输入模式
                - GPIO.PULL_DOWN: Pull-down input mode | 下拉输入模式
                - GPIO.OUT: Output mode | 输出模式
        
        Note:
            - This changes the GPIO mode dynamically | 这会动态改变GPIO模式
            - For input modes with pull-up/down, use PULL_UP/PULL_DOWN constants | 
              对于带上下拉的输入模式，使用PULL_UP/PULL_DOWN常量
        
        Example:
            # Change to input mode with pull-up | 切换到带上拉的输入模式
            gpio.mode(GPIO.PULL_UP)
            
            # Change to output mode | 切换到输出模式
            gpio.mode(GPIO.OUT)
        """
        ...
        
class freq:
    """System frequency control module | 系统频率控制模块
    
    Supports programmatic modification of CPU and KPU frequencies.
    Settings are persisted to /flash/freq.conf and applied after reboot.
    | 支持程序修改 cpu 和 kpu 频率。
    配置保存在文件系统的/flash/freq.conf文件下，设置后会自动重启生效。
    """
    
    @staticmethod
    def set(cpu: Optional[int] = None, pll1: Optional[int] = None, kpu_div: Optional[int] = None) -> None:
        """Set CPU and/or KPU frequencies | 设置CPU和/或KPU频率
        
        Parameters that are not set will retain their previous values.
        After frequency changes, the system will automatically reboot.
        | 不设置的参数会保持之前的值。
        设置完后会自动重启生效。
        
        Args:
            cpu: CPU frequency in MHz, range [26, 600] | CPU频率(MHz), 范围[26, 600]
                - Default: 400 MHz | 默认值: 400 MHz
                - Note: If cpu < 60MHz, REPL baud rate will be set to 9600 | 注意: 如果cpu < 60MHz, REPL串口波特率会设置为9600
                - Warning: For stability, not recommended to set too high on some boards | 警告: 为了稳定性，不建议在某些板子上设置过高
            pll1: PLL1 output frequency in MHz, range [26, 1200] | PLL1输出频率(MHz), 范围[26, 1200]
                - Default: 400 MHz | 默认值: 400 MHz
                - Note: Chip maximum is 1800MHz, but MaixPy limits to 1200MHz | 注意: 芯片最高1800MHz, 但MaixPy限制到1200MHz
            kpu_div: KPU clock divider, range [1, 16] | KPU时钟分频器, 范围[1, 16]
                - Default: 1 | 默认值: 1
                - KPU frequency = pll1 / kpu_div, range [26, 600] | KPU频率 = pll1 / kpu_div, 范围[26, 600]
        
        Note:
            - Configuration is saved to /flash/freq.conf | 配置文件将会保存在/flash/freq.conf
            - System will automatically reboot if frequencies change | 如果频率有变化，将会自动重启机器
            - Frequency changes may affect peripheral performance | 频率设置完毕后可能会导致某些外设性能改变
            - Verify system stability after frequency changes | 频率更改后验证系统稳定性
        
        Example:
            from Maix import freq
            # Set CPU and KPU to 400MHz
            freq.set(cpu=400, pll1=400, kpu_div=1)
            
            # Only change CPU frequency to 300MHz, keep other settings
            freq.set(cpu=300)
        
        Raises:
            ValueError: If parameters are out of valid ranges | 如果参数超出有效范围
        """
        ...
    
    @staticmethod
    def get() -> Tuple[int, int]:
        """Get current CPU and KPU frequencies | 获取当前设置的频率参数
        
        Returns:
            Tuple containing (cpu_frequency, kpu_frequency) in MHz | 
            元组形式返回cpu频率和kpu的频率，单位MHz
        
        Example:
            cpu_freq, kpu_freq = freq.get()
            print(f"Current frequencies - CPU: {cpu_freq}MHz, KPU: {kpu_freq}MHz")
            # Output: Current frequencies - CPU: 400MHz, KPU: 400MHz
        """
        ...
    
    @staticmethod
    def get_cpu() -> int:
        """Get current CPU frequency | 获取当前cpu的频率
        
        Returns:
            Current CPU frequency in MHz | 当前CPU频率(MHz)
        
        Example:
            cpu_freq = freq.get_cpu()
            print(f"CPU frequency: {cpu_freq} MHz")
        """
        ...
    
    @staticmethod
    def get_kpu() -> int:
        """Get current KPU frequency | 获取当前设置的kpu频率
        
        Returns:
            Current KPU frequency in MHz | 当前KPU频率(MHz)
        
        Example:
            kpu_freq = freq.get_kpu()
            print(f"KPU frequency: {kpu_freq} MHz")
        """
        ...
        
        
class utils:
    """System utilities module | 系统工具模块
    
    Provides various system-level utility functions for memory management,
    flash operations, and system information.
    | 提供各种系统级工具函数，用于内存管理、flash操作和系统信息。
    """
    
    @staticmethod
    def gc_heap_size(size: Optional[int] = None) -> int:
        """Get or set GC heap size | 获取或者设置GC堆大小
        
        Retrieves current GC heap size or sets a new size. When setting a new size,
        the system will automatically reboot to apply the changes.
        | 获取当前GC堆大小或设置新大小。设置新大小时，系统会自动重启以应用更改。
        
        Args:
            size: New heap size in bytes, or None to only get current size | 
                 新的堆大小(字节)，或None仅获取当前大小
                - If None: Only returns current heap size | 如果为None：仅返回当前堆大小
                - If provided: Sets new heap size and triggers system reboot | 如果提供：设置新堆大小并触发系统重启
        
        Returns:
            Current GC heap size in bytes | 当前GC堆大小(字节)
        
        Note:
            - Default firmware configuration is 500KB (0x80000) | 固件默认配置为500KB(0x80000)
            - Increasing heap size may help with "out of memory" errors | 增加堆大小可能有助于解决"内存不足"错误
            - Setting heap size requires system reboot | 设置堆大小需要系统重启
            - Configuration is persistent across reboots | 配置在重启后保持持久
        
        Example:
            import Maix
            
            # Get current heap size | 获取当前堆大小
            current_size = Maix.utils.gc_heap_size()
            print(f"Current heap size: {current_size} bytes")
            
            # Set new heap size to 600KB (0x96000) | 设置新堆大小为600KB(0x96000)
            # Note: This will cause system to reboot | 注意：这将导致系统重启
            Maix.utils.gc_heap_size(0x96000)
        """
        ...
    
    @staticmethod
    def flash_read(flash_offset: int, size: int) -> bytes:
        """Read data from internal flash memory | 从内部flash读取数据
        
        Reads specified number of bytes from internal flash memory starting at given offset.
        | 从内部flash读取指定大小(字节数)数据，从给定偏移量开始。
        
        Args:
            flash_offset: Flash memory address offset in bytes | flash地址偏移(字节)
                - Must be within valid flash memory range | 必须在有效的flash内存范围内
            size: Number of bytes to read | 要读取的字节数
                - Must be positive and within flash bounds | 必须为正数且在flash边界内
        
        Returns:
            Read data as bytes object | 读取的数据(bytes对象)
        
        Note:
            - Be careful with flash addresses to avoid reading invalid areas | 小心使用flash地址以避免读取无效区域
            - Flash memory is organized in sectors (typically 4KB per sector) | flash内存按扇区组织(通常每扇区4KB)
            - Reading from protected areas may cause errors | 从受保护区域读取可能导致错误
        
        Example:
            # Read 16 bytes from flash offset 0x10000 | 从flash偏移0x10000读取16字节
            data = Maix.utils.flash_read(0x10000, 16)
            print(f"Read {len(data)} bytes from flash")
            print(f"Data: {data.hex()}")
        """
        ...
    
    @staticmethod
    def heap_free() -> int:
        """Get free heap memory | 获取空闲堆内存
        
        Returns the amount of free memory available in the heap.
        | 返回堆中可用的空闲内存量。
        
        Returns:
            Amount of free heap memory in bytes | 空闲堆内存量(字节)
        
        Note:
            - This shows current free memory, not the total heap size | 这显示当前空闲内存，不是总堆大小
            - Free memory fluctuates based on program execution | 空闲内存根据程序执行而波动
            - Useful for debugging memory issues and optimizing memory usage | 对调试内存问题和优化内存使用很有用
        
        Example:
            # Check current heap size and free memory | 检查当前堆大小和空闲内存
            heap_size = Maix.utils.gc_heap_size()
            free_mem = Maix.utils.heap_free()
            used_mem = heap_size - free_mem
            
            print(f"Heap size: {heap_size} bytes")
            print(f"Free memory: {free_mem} bytes")
            print(f"Used memory: {used_mem} bytes")
            print(f"Memory usage: {(used_mem/heap_size)*100:.1f}%")
        
        Typical output (MaixDock, MaixPy v0.5.0_246):
            Heap size: 524288 bytes
            Free memory: 4374528 bytes
        """
        ...
    
    @staticmethod
    def get_firmware_version() -> str:
        """Get MaixPy firmware version | 获取MaixPy固件版本
        
        Returns the current firmware version string.
        | 返回当前固件版本字符串。
        
        Returns:
            Firmware version string | 固件版本字符串
        
        Example:
            version = Maix.utils.get_firmware_version()
            print(f"MaixPy firmware version: {version}")
            # Output: MaixPy firmware version: 0.5.0_246
        """
        ...
    
    @staticmethod
    def reset() -> None:
        """Reset the system | 重置系统
        
        Performs a soft reset of the K210 system.
        | 执行K210系统的软重置。
        
        Note:
            - This will restart the entire system | 这将重启整个系统
            - All program state will be lost | 所有程序状态将丢失
            - Similar to pressing the reset button | 类似于按下复位按钮
        
        Example:
            print("System will reset in 2 seconds...")
            import time
            time.sleep(2)
            Maix.utils.reset()
        """
        ...
    
    @staticmethod
    def get_chip_id() -> int:
        """Get K210 chip ID | 获取K210芯片ID
        
        Returns the unique identifier of the K210 chip.
        | 返回K210芯片的唯一标识符。
        
        Returns:
            Unique chip identifier as integer | 唯一芯片标识符(整数)
        
        Example:
            chip_id = Maix.utils.get_chip_id()
            print(f"K210 Chip ID: {chip_id:08X}")
            # Output: K210 Chip ID: 12345678
        """
        ...

