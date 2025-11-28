"""
FPIOA Manager module | FPIOA管理模块

This module (imported as fm) is used to register internal chip functions and pins,
helping users manage the mapping relationship between internal functions and pins.
| 该模块（导入为fm）用于注册芯片内部功能和引脚，帮助用户管理内部功能和引脚映射关系。

Key concept: On K210 chip, external pins and internal functions are independent.
Any internal function (GPIO/I2C/UART/I2S/SPI) can be mapped to any pin (0-47).
| 核心概念：在K210芯片上，外部引脚和内部功能是独立的。
任何内部功能(GPIO/I2C/UART/I2S/SPI)都可以映射到任何引脚(0-47)。
"""

from typing import List, Tuple, Optional, Union, Any, Dict

class _FPIOA_Functions:
    """FPIOA function constants | FPIOA功能常量
    
    All available internal hardware functions that can be mapped to pins.
    | 所有可用的内部硬件功能，可以映射到引脚。
    """
    
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
    
    # Clock functions | 时钟功能
    CLK_SPI2: int = 148      # Clock SPI2 | SPI2时钟
    CLK_I2C2: int = 149      # Clock I2C2 | I2C2时钟
    
    # Timer functions | 定时器功能
    TIMER0_TOGGLE1: int = 150  # TIMER0 Toggle Output 1 | TIMER0切换输出1
    TIMER0_TOGGLE2: int = 151  # TIMER0 Toggle Output 2 | TIMER0切换输出2
    TIMER0_TOGGLE3: int = 152  # TIMER0 Toggle Output 3 | TIMER0切换输出3
    TIMER0_TOGGLE4: int = 153  # TIMER0 Toggle Output 4 | TIMER0切换输出4
    TIMER1_TOGGLE1: int = 154  # TIMER1 Toggle Output 1 | TIMER1切换输出1
    TIMER1_TOGGLE2: int = 155  # TIMER1 Toggle Output 2 | TIMER1切换输出2
    TIMER1_TOGGLE3: int = 156  # TIMER1 Toggle Output 3 | TIMER1切换输出3
    TIMER1_TOGGLE4: int = 157  # TIMER1 Toggle Output 4 | TIMER1切换输出4
    TIMER2_TOGGLE1: int = 158  # TIMER2 Toggle Output 1 | TIMER2切换输出1
    TIMER2_TOGGLE2: int = 159  # TIMER2 Toggle Output 2 | TIMER2切换输出2
    TIMER2_TOGGLE3: int = 160  # TIMER2 Toggle Output 3 | TIMER2切换输出3
    TIMER2_TOGGLE4: int = 161  # TIMER2 Toggle Output 4 | TIMER2切换输出4

class _FPIOA_Manager:
    """FPIOA Manager class | FPIOA管理类
    
    Manages pin function mapping for K210 chip, allowing any internal function
    to be mapped to any physical pin (0-47).
    | 管理K210芯片的引脚功能映射，允许任何内部功能映射到任何物理引脚(0-47)。
    """
    
    fpioa: _FPIOA_Functions = _FPIOA_Functions()
    
    def register(self, pin: int, func: int, force: bool = True) -> None:
        """Register pin function mapping | 注册引脚功能映射
        
        Maps a physical pin to an internal hardware function. If force=True, it will
        override any existing mapping for that pin. If force=False, it will raise an
        exception if the function is already used by another pin.
        | 将物理引脚映射到内部硬件功能。如果force=True，它将覆盖该引脚的任何现有映射。
        如果force=False，如果该功能已被另一个引脚使用，它将引发异常。
        
        Args:
            pin: Physical pin number [0, 47] | 物理引脚编号[0, 47]
            func: Internal hardware function constant | 内部硬件功能常量
                - Example: fm.fpioa.GPIOHS0, fm.fpioa.UART1_TX | 示例
            force: Force mapping even if function is already used | 即使功能已被使用，也强制映射
                - True: Override existing mappings (default, useful for IDE) | True: 覆盖现有映射(默认，对IDE有用)
                - False: Raise exception if function is already used | False: 如果功能已被使用，引发异常
        
        Note:
            - Default force=True is for IDE convenience, allowing multiple runs | 
              默认force=True是为了IDE方便，允许多次运行
            - For production code, set force=False to avoid accidental remapping | 
              对于生产代码，设置force=False以避免意外重新映射
            - The following GPIOHS pins are reserved by default - avoid using them: | 
              以下GPIOHS引脚默认保留 - 避免使用它们:
                - GPIOHS31: LCD_DC | LCD控制信号引脚
                - GPIOHS30: LCD_RST | LCD复位芯片脚
                - GPIOHS29: SD_CS | SD卡SPI片选
                - GPIOHS28: MIC_LED_CLK | SK9822_DAT
                - GPIOHS27: MIC_LED_DATA | SK9822_CLK
        
        Examples:
            # Basic mapping | 基本映射
            fm.register(11, fm.fpioa.GPIO0)
            
            # Map green LED to high-speed GPIO0 | 将绿色LED映射到高速GPIO0
            from board import board_info
            fm.register(board_info.LED_G, fm.fpioa.GPIOHS0)
            
            # Safe mapping (will raise exception if function is already used) | 安全映射(如果功能已被使用将引发异常)
            fm.register(12, fm.fpioa.GPIO2, force=False)
        
        Raises:
            Exception: If force=False and the function is already used by another pin | 
                     如果force=False且该功能已被另一个引脚使用
        """
        ...
    
    def unregister(self, pin: int) -> None:
        """Unregister pin function mapping | 注销引脚功能映射
        
        Releases the hardware function bound to the specified pin, making it available
        for other mappings.
        | 释放绑定到指定引脚的硬件功能，使其可用于其他映射。
        
        Args:
            pin: Physical pin number to release [0, 47] | 要释放的物理引脚编号[0, 47]
        
        Note:
            - Always unregister pins when they are no longer needed | 
              当引脚不再需要时，始终注销它们
            - This is good practice to avoid resource leaks | 
              这是避免资源泄漏的良好做法
        
        Example:
            fm.unregister(11)  # Release pin 11 | 释放引脚11
            fm.unregister(board_info.LED_G)  # Release LED pin | 释放LED引脚
        """
        ...
    
    def get_pin_by_function(self, func: int) -> Optional[int]:
        """Get pin number by function | 通过功能获取引脚编号
        
        Returns the pin number that is currently mapped to the specified internal function.
        | 返回当前映射到指定内部功能的引脚编号。
        
        Args:
            func: Internal hardware function constant | 内部硬件功能常量
                - Example: fm.fpioa.GPIOHS0, fm.fpioa.UART1_RX | 示例
        
        Returns:
            Pin number if the function is mapped, None if not mapped | 
            如果功能已映射则返回引脚编号，未映射则返回None
        
        Example:
            pin = fm.get_pin_by_function(fm.fpioa.GPIOHS0)
            if pin is not None:
                print(f"GPIOHS0 is mapped to pin {pin}")
            else:
                print("GPIOHS0 is not mapped to any pin")
        """
        ...
    
    def get_gpio_used(self) -> List[Tuple[str, Optional[int]]]:
        """Get GPIO usage status | 获取GPIO使用状态
        
        Returns a list of tuples showing all GPIOHS and GPIO functions and their current
        pin assignments. None indicates the function is not used.
        | 返回元组列表，显示所有GPIOHS和GPIO功能及其当前引脚分配。None表示该功能未使用。
        
        Returns:
            List of (function_name, pin_number) tuples | (function_name, pin_number)元组列表
                - function_name: String representation of the function | 功能的字符串表示
                - pin_number: Pin number or None if not used | 引脚编号或None(如果未使用)
        
        Note:
            - This only shows GPIOHS and GPIO functions, not other peripherals | 
              这仅显示GPIOHS和GPIO功能，不显示其他外设
            - Every function has a default state | 每个功能都有默认状态
        
        Example:
            for func_name, pin in fm.get_gpio_used():
                status = f"pin {pin}" if pin is not None else "not used"
                print(f"{func_name}: {status}")
        """
        ...
    
    def help(self, func: Optional[Union[int, str]] = None) -> str:
        """Display help information | 显示帮助信息
        
        Displays help information about internal hardware functions and their descriptions.
        If no parameter is provided, displays all functions in table format. If a function
        number or name is provided, displays information about that specific function.
        | 显示有关内部硬件功能及其描述的帮助信息。
        如果未提供参数，以表格格式显示所有功能。如果提供了功能编号或名称，显示该特定功能的信息。
        
        Args:
            func: Function identifier (optional) | 功能标识符(可选)
                - None: Display all functions (default) | None: 显示所有功能(默认)
                - int: Function number (e.g., fm.fpioa.GPIOHS0) | int: 功能编号
                - str: Function name string | str: 功能名称字符串
        
        Returns:
            Function name and description | 功能名称和描述
        
        Examples:
            # Display all functions | 显示所有功能
            fm.help()
            
            # Display specific function by number | 通过编号显示特定功能
            fm.help(fm.fpioa.GPIOHS0)
            fm.help(24)  # GPIOHS0 function number | GPIOHS0功能编号
            
            # Display specific function by name | 通过名称显示特定功能
            fm.help("GPIOHS0")
        """
        ...