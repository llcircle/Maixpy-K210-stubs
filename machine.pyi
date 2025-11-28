"""
Machine module for hardware control | 硬件控制模块

Provides low-level hardware access and control | 提供底层硬件访问和控制
"""

from typing import Callable, Optional, Union, Any, List,Dict

class I2C:
    """I2C bus controller | I2C总线控制器
    
    I2C bus protocol that uses two lines (SCL, SDA) to control multiple slave devices in master mode.
    | I2C总线协议，简单地使用两条线（SCL，SDA）可以控制多个从机（主机模式）。
    
    Features:
    - Supports master and slave modes | 支持主机模式和从机模式
    - 7-bit/10-bit addressing modes | 7位/10位寻址模式  
    - Standard mode <=100Kb/s | 标准模式 <=100Kb/s
    - Fast mode <=400Kb/s | 快速模式 <=400Kb/s
    - Fast-plus mode <=1000Kb/s | 超快速模式 <=1000Kb/s
    - High-speed mode 3.4Mb/s | 高速模式 3.4Mb/s
    """
    
    # I2C IDs | I2C ID
    I2C0: int = 0  # I2C bus 0 | I2C总线0
    I2C1: int = 1  # I2C bus 1 | I2C总线1
    I2C2: int = 2  # I2C bus 2 | I2C总线2
    I2C3: int = 3  # I2C bus 3 (software) | I2C总线3（软件模拟）
    I2C4: int = 4  # I2C bus 4 (software) | I2C总线4（软件模拟）
    I2C5: int = 5  # I2C bus 5 (software) | I2C总线5（软件模拟）
    
    # Operation modes | 操作模式
    MODE_MASTER: int = 0  # Master mode | 主机模式
    MODE_SLAVE: int = 1   # Slave mode | 从机模式
    
    # Event types for slave mode | 从机模式事件类型
    I2C_EV_START: int = 0    # Start condition event | 开始信号事件
    I2C_EV_RESTART: int = 1  # Restart condition event | 重新开始信号事件  
    I2C_EV_STOP: int = 2     # Stop condition event | 结束信号事件
    
    def __init__(self, id: int, mode: int = MODE_MASTER, 
                scl: Optional[int] = None, sda: Optional[int] = None,
                gscl: Optional[int] = None, gsda: Optional[int] = None,
                freq: int = 400000, timeout: int = 1000, 
                addr: int = 0, addr_size: int = 7,
                on_receive: Optional[Callable[[bytes], None]] = None,
                on_transmit: Optional[Callable[[], bytes]] = None, 
                on_event: Optional[Callable[[int], None]] = None) -> None:
        """Initialize I2C bus | 初始化I2C总线
        
        Args:
            id: I2C ID [0~2] for hardware I2C, [3~5] for software I2C (I2C_SOFT) | 
                I2C ID [0~2] 为硬件I2C, [3~5] 为软件I2C (I2C_SOFT)
            mode: Operation mode (MODE_MASTER or MODE_SLAVE) | 操作模式 (MODE_MASTER 或 MODE_SLAVE)
            scl: SCL pin number [0,47], can be None to use fm for pin mapping | 
                SCL引脚编号 [0,47], 可以为None以使用fm进行引脚映射
            sda: SDA pin number [0,47], can be None to use fm for pin mapping | 
                SDA引脚编号 [0,47], 可以为None以使用fm进行引脚映射
            gscl: GPIOHS for SCL, only needed for software I2C, defaults to scl | 
                SCL对应的GPIOHS, 仅软件模拟I2C需要, 默认与scl相同
            gsda: GPIOHS for SDA, only needed for software I2C, defaults to sda | 
                SDA对应的GPIOHS, 仅软件模拟I2C需要, 默认与sda相同
            freq: I2C communication frequency in Hz | I2C通信频率(Hz)
                - Standard mode: <=100000 (100Kb/s) | 标准模式: <=100000 (100Kb/s)
                - Fast mode: <=400000 (400Kb/s) | 快速模式: <=400000 (400Kb/s)
                - Fast-plus mode: <=1000000 (1000Kb/s) | 超快速模式: <=1000000 (1000Kb/s)
                - High-speed mode: 3400000 (3.4Mb/s) | 高速模式: 3400000 (3.4Mb/s)
            timeout: Timeout in milliseconds (currently reserved, has no effect) | 
                超时时间(毫秒)（目前保留，设置无效）
            addr: Slave address (only used in MODE_SLAVE) | 从机地址（仅在MODE_SLAVE模式下使用）
            addr_size: Address size, 7 for 7-bit addressing, 10 for 10-bit addressing | 
                地址长度, 7为7位寻址, 10为10位寻址
            on_receive: Callback function for slave mode when data is received | 
                从机模式下接收数据时的回调函数
            on_transmit: Callback function for slave mode when data is requested | 
                从机模式下数据被请求时的回调函数
            on_event: Callback function for slave mode events (start/restart/stop) | 
                从机模式下事件（开始/重新开始/结束）的回调函数
        
        Note:
            - For hardware I2C (id 0-2), use scl/sda parameters or fm for pin mapping | 
              对于硬件I2C (id 0-2), 使用scl/sda参数或fm进行引脚映射
            - For software I2C (id 3-5), gscl/gsda must be specified | 
              对于软件I2C (id 3-5), 必须指定gscl/gsda
            - In master mode, addr, on_receive, on_transmit, on_event are ignored | 
              在主机模式下, addr, on_receive, on_transmit, on_event 参数被忽略
        
        Example:
            # Hardware I2C master mode | 硬件I2C主机模式
            i2c = I2C(I2C.I2C0, freq=100000, scl=28, sda=29)
            
            # Software I2C master mode | 软件I2C主机模式
            i2c = I2C(I2C.I2C3, freq=100000, scl=10, sda=11, gscl=2, gsda=3)
            
            # I2C slave mode | I2C从机模式
            def on_receive(data):
                print("Received:", data)
            def on_transmit():
                return b"response"
            def on_event(event):
                print("Event:", event)
            i2c = I2C(I2C.I2C0, mode=I2C.MODE_SLAVE, addr=0x24, addr_size=7,
                     on_receive=on_receive, on_transmit=on_transmit, on_event=on_event)
        """
        ...
    
    def init(self, id: int, mode: int = MODE_MASTER, 
            scl: Optional[int] = None, sda: Optional[int] = None,
            gscl: Optional[int] = None, gsda: Optional[int] = None,
            freq: int = 400000, timeout: int = 1000, 
            addr: int = 0, addr_size: int = 7,
            on_receive: Optional[Callable[[bytes], None]] = None,
            on_transmit: Optional[Callable[[], bytes]] = None, 
            on_event: Optional[Callable[[int], None]] = None) -> None:
        """Initialize I2C bus (alternative to constructor) | 初始化I2C总线（构造函数的替代方法）
        
        Same parameters as constructor | 参数与构造函数相同
        
        Example:
            i2c = I2C(I2C.I2C0)
            i2c.init(id=I2C.I2C0, freq=400000, scl=28, sda=29)
        """
        ...
    
    def scan(self) -> List[int]:
        """Scan I2C bus for slave devices | 扫描I2C总线上的从机设备
        
        Returns:
            List of detected slave device addresses | 检测到的从机设备地址列表
        
        Example:
            devices = i2c.scan()
            print("I2C devices found:", [hex(addr) for addr in devices])
            # Output: I2C devices found: ['0x3c', '0x50']
        """
        ...
    
    def readfrom(self, addr: int, nbytes: int, stop: bool = True) -> bytes:
        """Read data from I2C slave device | 从I2C从机设备读取数据
        
        Args:
            addr: Slave device address | 从机设备地址
            nbytes: Number of bytes to read | 要读取的字节数
            stop: Whether to generate stop condition (currently must be True) | 
                 是否产生停止信号（目前必须为True）
        
        Returns:
            Read data as bytes | 读取的数据(bytes类型)
        
        Example:
            data = i2c.readfrom(0x3c, 16)  # Read 16 bytes from device 0x3c | 从设备0x3c读取16字节
        """
        ...
    
    def readfrom_into(self, addr: int, buf: bytearray, stop: bool = True) -> None:
        """Read data from I2C slave device into buffer | 从I2C从机设备读取数据到缓冲区
        
        Args:
            addr: Slave device address | 从机设备地址
            buf: bytearray buffer to store read data | 用于存储读取数据的bytearray缓冲区
            stop: Whether to generate stop condition (currently must be True) | 
                 是否产生停止信号（目前必须为True）
        
        Example:
            buffer = bytearray(16)
            i2c.readfrom_into(0x3c, buffer)  # Read into buffer | 读取到缓冲区
            print(buffer)
        """
        ...
    
    def writeto(self, addr: int, buf: bytes, stop: bool = True) -> int:
        """Write data to I2C slave device | 向I2C从机设备写入数据
        
        Args:
            addr: Slave device address | 从机设备地址
            buf: Data to write | 要写入的数据
            stop: Whether to generate stop condition (currently must be True) | 
                 是否产生停止信号（目前必须为True）
        
        Returns:
            Number of bytes successfully written | 成功写入的字节数
        
        Example:
            bytes_written = i2c.writeto(0x3c, b'hello')  # Write string | 写入字符串
            print(f"Written {bytes_written} bytes")
        """
        ...
    
    def readfrom_mem(self, addr: int, memaddr: int, nbytes: int, mem_size: int = 8) -> bytes:
        """Read data from I2C slave device register | 从I2C从机设备寄存器读取数据
        
        Args:
            addr: Slave device address | 从机设备地址
            memaddr: Register address to read from | 要读取的寄存器地址
            nbytes: Number of bytes to read | 要读取的字节数
            mem_size: Register width in bits (default 8) | 寄存器宽度(位)(默认8)
        
        Returns:
            Read data as bytes | 读取的数据(bytes类型)
        
        Example:
            # Read 2 bytes from register 0x00 of device 0x50 | 从设备0x50的寄存器0x00读取2字节
            data = i2c.readfrom_mem(0x50, 0x00, 2)
        """
        ...
    
    def readfrom_mem_into(self, addr: int, memaddr: int, buf: bytearray, mem_size: int = 8) -> None:
        """Read data from I2C slave device register into buffer | 从I2C从机设备寄存器读取数据到缓冲区
        
        Args:
            addr: Slave device address | 从机设备地址
            memaddr: Register address to read from | 要读取的寄存器地址
            buf: bytearray buffer to store read data | 用于存储读取数据的bytearray缓冲区
            mem_size: Register width in bits (default 8) | 寄存器宽度(位)(默认8)
        
        Example:
            buffer = bytearray(2)
            i2c.readfrom_mem_into(0x50, 0x00, buffer)  # Read register into buffer | 读取寄存器到缓冲区
        """
        ...
    
    def writeto_mem(self, addr: int, memaddr: int, buf: bytes, mem_size: int = 8) -> None:
        """Write data to I2C slave device register | 向I2C从机设备寄存器写入数据
        
        Args:
            addr: Slave device address | 从机设备地址
            memaddr: Register address to write to | 要写入的寄存器地址
            buf: Data to write | 要写入的数据
            mem_size: Register width in bits (default 8) | 寄存器宽度(位)(默认8)
        
        Example:
            # Write 0x01 to register 0x00 of device 0x50 | 向设备0x50的寄存器0x00写入0x01
            i2c.writeto_mem(0x50, 0x00, b'\x01')
        """
        ...
    
    def deinit(self) -> None:
        """Deinitialize I2C hardware and release resources | 反初始化I2C硬件并释放资源
        
        Stops I2C operation, releases hardware resources, and closes I2C clock | 
        停止I2C操作，释放硬件资源，并关闭I2C时钟
        
        Example:
            i2c.deinit()  # Properly cleanup I2C resources | 正确清理I2C资源
        """
        ...
    
    def __del__(self) -> None:
        """Destructor, same as deinit() | 析构函数，与deinit()相同
        
        Automatically called when I2C object is destroyed | I2C对象销毁时自动调用
        """
        ...

class PWM:
    """PWM (Pulse Width Modulation) controller | PWM（脉宽调制）控制器
    
    Hardware-supported PWM module that can be assigned to any pin (0-47).
    | 硬件支持的PWM模块，可以指定任意引脚（0到47引脚）。
    
    Note: Each PWM depends on a timer. When a timer is bound to PWM function,
    it cannot be used as a regular timer anymore. With 3 timers and 4 channels
    each, maximum 12 PWM waveforms can be generated simultaneously.
    | 每个 PWM 依赖于一个定时器，即当定时器与 PWM 功能绑定后，不能作为普通定时器使用了。
    因为有 3 个定时器，每个定时器有 4 个通道，即最大可以同时产生 12 路 PWM 波形。
    """
    
    def __init__(self, tim: Timer, freq: int = 500000, duty: int = 50, 
                pin: Optional[int] = None, enable: bool = True) -> None:
        """Initialize PWM controller | 初始化PWM控制器
        
        Args:
            tim: Timer object that PWM depends on. Must be initialized with 
                 Timer ID and channel number in MODE_PWM mode | 
                 PWM依赖的定时器对象。必须在MODE_PWM模式下初始化，指定定时器ID和通道号
            freq: PWM waveform frequency in Hz | PWM波形频率(Hz)
                - Default: 500000 (500kHz) | 默认: 500000 (500kHz)
                - Typical range: 1Hz to several MHz | 典型范围: 1Hz到几MHz
            duty: PWM duty cycle percentage [0,100], where 0 = always low, 
                  100 = always high | PWM占空比百分比[0,100]，其中0=始终低电平，100=始终高电平
                - Default: 50 (50% duty cycle) | 默认: 50 (50%占空比)
            pin: PWM output pin number [0,47]. Can be None to use fm for 
                 pin mapping management | PWM输出引脚编号[0,47]。可以为None以使用fm进行引脚映射管理
            enable: Whether to start generating waveform immediately after 
                    initialization (default True) | 是否在初始化后立即开始产生波形（默认True）
        
        Note:
            - The timer must be initialized in Timer.MODE_PWM mode | 
              定时器必须在Timer.MODE_PWM模式下初始化
            - If pin is not specified, use fm.register() to map pin to PWM function | 
              如果未指定引脚，使用fm.register()将引脚映射到PWM功能
            - PWM frequency and duty cycle may have hardware limitations | 
              PWM频率和占空比可能有硬件限制
        
        Example:
            from machine import Timer, PWM
            from board import board_info
            
            # Initialize timer in PWM mode | 在PWM模式下初始化定时器
            tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
            
            # Initialize PWM on LED pin | 在LED引脚上初始化PWM
            pwm = PWM(tim, freq=500000, duty=50, pin=board_info.LED_G)
        """
        ...
    
    def init(self, tim: Timer, freq: int = 500000, duty: int = 50, 
            pin: Optional[int] = None, enable: bool = True) -> None:
        """Initialize PWM controller (alternative to constructor) | 初始化PWM控制器（构造函数的替代方法）
        
        Same parameters as constructor | 参数与构造函数相同
        
        Example:
            pwm = PWM(None)  # Create empty PWM object | 创建空的PWM对象
            tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
            pwm.init(tim, freq=1000, duty=30, pin=12)  # Initialize later | 稍后初始化
        """
        ...
    
    def freq(self, freq: Optional[int] = None) -> int:
        """Get or set PWM frequency | 获取或设置PWM频率
        
        Args:
            freq: New PWM frequency in Hz, if None then only get current frequency | 
                 新的PWM频率(Hz)，如果为None则只获取当前频率
        
        Returns:
            Current PWM frequency in Hz | 当前PWM频率(Hz)
        
        Example:
            # Get current frequency | 获取当前频率
            current_freq = pwm.freq()
            print(f"Current PWM frequency: {current_freq} Hz")
            
            # Set new frequency to 1kHz | 设置新频率为1kHz
            pwm.freq(1000)
            print(f"New PWM frequency: {pwm.freq()} Hz")
        """
        ...
    
    def duty(self, duty: Optional[int] = None) -> int:
        """Get or set PWM duty cycle | 获取或设置PWM占空比
        
        Args:
            duty: New duty cycle percentage [0,100], if None then only get current duty | 
                 新的占空比百分比[0,100]，如果为None则只获取当前占空比
        
        Returns:
            Current PWM duty cycle percentage | 当前PWM占空比百分比
        
        Example:
            # Get current duty cycle | 获取当前占空比
            current_duty = pwm.duty()
            print(f"Current duty cycle: {current_duty}%")
            
            # Set new duty cycle to 75% | 设置新占空比为75%
            pwm.duty(75)
            print(f"New duty cycle: {pwm.duty()}%")
        """
        ...
    
    def enable(self) -> None:
        """Enable PWM output | 使能PWM输出
        
        Starts generating PWM waveform on the specified pin immediately | 
        使指定的引脚上立即产生PWM波形
        
        Example:
            pwm.enable()  # Start PWM output | 开始PWM输出
        """
        ...
    
    def disable(self) -> None:
        """Disable PWM output | 失能PWM输出
        
        Stops PWM waveform generation on the specified pin | 
        指定的引脚不再产生波形
        
        Example:
            pwm.disable()  # Stop PWM output | 停止PWM输出
        """
        ...
    
    def deinit(self) -> None:
        """Deinitialize PWM hardware and release resources | 反初始化PWM硬件并释放资源
        
        Stops PWM operation, releases hardware resources, and closes PWM clock | 
        停止PWM操作，释放硬件资源，并关闭PWM时钟
        
        Example:
            pwm.deinit()  # Properly cleanup PWM resources | 正确清理PWM资源
        
        Note:
            Same as __del__ method, can be called explicitly or automatically when object is destroyed | 
            与__del__方法相同，可以显式调用或在对象销毁时自动调用
        """
        ...
    
    def __del__(self) -> None:
        """Destructor, same as deinit() | 析构函数，与deinit()相同
        
        Automatically called when PWM object is destroyed | PWM对象销毁时自动调用
        """
        ...

class Timer:
    """Hardware timer | 硬件定时器
    
    Hardware timer that can be used to trigger tasks periodically or after a delay.
    Can trigger interrupts (callback functions) with higher precision than software timers.
    | 硬件定时器，可用于定期触发任务或在延迟后触发任务。
    可以触发中断（回调函数），精度比软件定时器高。
    
    Note: There are 3 timers available (TIMER0-TIMER2), each with 4 channels (CHANNEL0-CHANNEL3).
    | 注意：共有3个定时器可用(TIMER0-TIMER2)，每个定时器有4个通道(CHANNEL0-CHANNEL3)。
    """
    
    # Timer IDs | 定时器ID
    TIMER0: int = 0  # Timer 0 | 定时器0
    TIMER1: int = 1  # Timer 1 | 定时器1  
    TIMER2: int = 2  # Timer 2 | 定时器2
    
    # Timer channels | 定时器通道
    CHANNEL0: int = 0  # Channel 0 | 通道0
    CHANNEL1: int = 1  # Channel 1 | 通道1
    CHANNEL2: int = 2  # Channel 2 | 通道2
    CHANNEL3: int = 3  # Channel 3 | 通道3
    
    # Timer modes | 定时器模式
    MODE_ONE_SHOT: int = 0   # One-shot mode, triggers callback once | 单次模式，只触发回调一次
    MODE_PERIODIC: int = 1   # Periodic mode, triggers callback continuously | 周期模式，连续触发回调
    MODE_PWM: int = 2        # PWM mode, used for generating PWM signals | PWM模式，用于生成PWM信号
    
    # Time units | 时间单位
    UNIT_S: int = 0    # Seconds | 秒
    UNIT_MS: int = 1   # Milliseconds | 毫秒  
    UNIT_US: int = 2   # Microseconds | 微秒
    UNIT_NS: int = 3   # Nanoseconds | 纳秒
    
    def __init__(self, id: int, channel: int, mode: int = MODE_ONE_SHOT, 
                period: int = 1000, unit: int = UNIT_MS, 
                callback: Optional[Callable[['Timer', Any], None]] = None, 
                arg: Any = None, start: bool = True, priority: int = 1, div: int = 0) -> None:
        """Initialize hardware timer | 初始化硬件定时器
        
        Args:
            id: Timer ID [0~2] (TIMER0~TIMER2) | 定时器ID [0~2] (TIMER0~TIMER2)
            channel: Timer channel [0~3] (CHANNEL0~CHANNEL3) | 定时器通道 [0~3] (CHANNEL0~CHANNEL3)
            mode: Timer mode (MODE_ONE_SHOT, MODE_PERIODIC, MODE_PWM) | 定时器模式
            period: Timer period, callback will be called after this time | 定时器周期，回调函数将在此时间后被调用
            unit: Time unit for period (UNIT_S, UNIT_MS, UNIT_US, UNIT_NS) | 周期的时间单位
            callback: Callback function, defined with two parameters: timer object and arg | 回调函数，定义为两个参数：定时器对象和arg
            arg: Argument to pass to callback function as second parameter | 传给回调函数的参数，作为第二个参数
            start: Whether to start timer immediately after initialization | 是否在初始化后立即启动定时器
            priority: Hardware timer interrupt priority [1,7], smaller value = higher priority | 硬件定时器中断优先级[1,7]，值越小优先级越高
            div: Hardware timer clock divider [0,255], clk_timer = clk_pll0/2^(div+1) | 硬件定时器时钟分频器[0,255]
        
        Note:
            - Callback function is called in interrupt context, avoid long operations or dynamic allocation | 
              回调函数在中断上下文中调用，避免长时间操作或动态分配
            - clk_timer*period(unit:s) should be < 2^32 and >=1 | 
              clk_timer*period(unit:s) 应该 < 2^32 并且 >=1
        
        Example:
            def on_timer(timer):
                print("time up:", timer)
                print("param:", timer.callback_arg())
            
            tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_ONE_SHOT, 
                       period=3000, callback=on_timer, arg=on_timer)
        """
        ...
    
    def init(self, id: int, channel: int, mode: int = MODE_ONE_SHOT, 
            period: int = 1000, unit: int = UNIT_MS, 
            callback: Optional[Callable[['Timer', Any], None]] = None, 
            arg: Any = None, start: bool = True, priority: int = 1, div: int = 0) -> None:
        """Initialize timer (alternative to constructor) | 初始化定时器（构造函数的替代方法）
        
        Same parameters as constructor | 参数与构造函数相同
        
        Example:
            tim = Timer(Timer.TIMER0, Timer.CHANNEL0)
            tim.init(id=Timer.TIMER0, channel=Timer.CHANNEL0, mode=Timer.MODE_PERIODIC,
                    period=1, unit=Timer.UNIT_S, callback=on_timer, arg=on_timer, start=False)
        """
        ...
    
    def callback_arg(self) -> Any:
        """Get the argument passed to callback function | 获取传给回调函数的参数
        
        Returns:
            The argument object passed during timer initialization | 初始化定时器时传入的参数对象
        
        Example:
            arg = tim.callback_arg()
            print("Callback argument:", arg)
        
        Note:
            Can only be called on Timer instance, not on Timer class | 只能在Timer实例上调用，不能在Timer类上调用
        """
        ...
    
    def callback(self, callback: Optional[Callable[['Timer', Any], None]] = None) -> Callable[['Timer', Any], None]:
        """Get or set callback function | 获取或设置回调函数
        
        Args:
            callback: New callback function to set, if None then only get current callback | 
                     要设置的新回调函数，如果为None则只获取当前回调
        
        Returns:
            Current callback function | 当前回调函数
        
        Example:
            # Get current callback
            current_cb = tim.callback()
            
            # Set new callback
            def new_callback(timer):
                print("New callback triggered")
            tim.callback(new_callback)
        """
        ...
    
    def period(self, period: Optional[int] = None) -> int:
        """Get or set timer period | 获取或设置定时器周期
        
        Args:
            period: New period value to set, if None then only get current period | 
                   要设置的新周期值，如果为None则只获取当前周期
        
        Returns:
            Current period value | 当前周期值
        
        Example:
            # Get current period
            current_period = tim.period()
            print("Current period:", current_period)
            
            # Set new period (2000ms)
            tim.period(2000)
        """
        ...
    
    def start(self) -> None:
        """Start the timer | 启动定时器
        
        Example:
            tim.start()  # Start timer if not started in constructor | 启动定时器（如果构造函数中没有启动）
        """
        ...
    
    def stop(self) -> None:
        """Stop the timer | 停止定时器
        
        Example:
            tim.stop()  # Stop timer operation | 停止定时器操作
        """
        ...
    
    def restart(self) -> None:
        """Restart the timer | 重新启动定时器
        
        Example:
            tim.restart()  # Restart timer from beginning | 从头重新启动定时器
        """
        ...
    
    def deinit(self) -> None:
        """Deinitialize timer and release hardware resources | 反初始化定时器并释放硬件资源
        
        Stops timer, releases hardware occupancy, and closes hardware clock | 
        停止定时器，释放硬件占用，并关闭硬件时钟
        
        Example:
            tim.deinit()  # Properly cleanup timer resources | 正确清理定时器资源
        
        Note:
            Same as __del__ method, can be called explicitly or automatically when object is destroyed | 
            与__del__方法相同，可以显式调用或在对象销毁时自动调用
        """
        ...
    
    def __del__(self) -> None:
        """Destructor, same as deinit() | 析构函数，与deinit()相同
        
        Automatically called when timer object is destroyed | 定时器对象销毁时自动调用
        """
        ...
        
class SPI:
    """SPI (Serial Peripheral Interface) controller | SPI（串行外设接口）控制器
    
    Synchronous serial protocol consisting of master and slave devices.
    Standard 4-wire mode uses SCK (SCLK), CS (chip select), MOSI, and MISO lines.
    | 同步串行协议，由主机和从机组成。
    标准4线模式由 SCK（SCLK）， CS（片选）， MOSI， MISO 4条线连接主从机
    
    K210 SPI features:
    - 4 SPI devices available (SPI0-SPI3), plus software SPI (SPI4/SPI_SOFT)
    - SPI0, SPI1, SPI3 can only work in master mode
    - SPI2 can only work in slave mode (not implemented in MaixPy yet)
    - SPI3 is reserved for SPI Flash connection
    - Supports 1/2/4/8-line full-duplex modes (MaixPy only supports standard 4-wire mode)
    - Maximum transfer rate: 45MHz (1/2 CPU frequency, ~200Mbps)
    - Supports DMA (Direct Memory Access)
    - 4 configurable hardware chip selects (CS0-CS3)
    | K210 SPI特性：
    - 共有4个SPI设备(SPI0-SPI3)，外加软件SPI(SPI4/SPI_SOFT)
    - SPI0, SPI1, SPI3只能工作在主机模式
    - SPI2只能工作在从机模式（MaixPy中尚未实现）
    - SPI3已用于SPI Flash连接（保留）
    - 支持1/2/4/8线全双工模式（MaixPy仅支持标准4线模式）
    - 最高传输速率：45MHz（1/2主频，约200Mbps）
    - 支持DMA（直接内存访问）
    - 4个可配置任意引脚的硬件片选
    """
    
    # SPI device IDs | SPI设备ID
    SPI0: int = 0  # SPI device 0 | SPI设备0
    SPI1: int = 1  # SPI device 1 | SPI设备1
    SPI2: int = 2  # SPI device 2 (slave mode only, not implemented) | SPI设备2（仅从机模式，未实现）
    SPI3: int = 3  # SPI device 3 (reserved for SPI Flash) | SPI设备3（保留用于SPI Flash）
    SPI4: int = 4  # SPI device 4 (software SPI) | SPI设备4（软件SPI）
    SPI_SOFT: int = 4  # Software SPI alias | 软件SPI别名
    
    # Operation modes | 操作模式
    MODE_MASTER: int = 0     # Master mode (standard 4-wire) | 主机模式（标准4线）
    MODE_MASTER_2: int = 1   # Master mode (2-wire) - not supported in MaixPy | 主机模式（2线）- MaixPy不支持
    MODE_MASTER_4: int = 2   # Master mode (4-wire) - not supported in MaixPy | 主机模式（4线）- MaixPy不支持  
    MODE_MASTER_8: int = 3   # Master mode (8-wire) - not supported in MaixPy | 主机模式（8线）- MaixPy不支持
    MODE_SLAVE: int = 4      # Slave mode - not implemented in MaixPy | 从机模式 - MaixPy中未实现
    
    # Bit order | 位顺序
    MSB: int = 0  # Most Significant Bit first | 先发送高位/高字节
    LSB: int = 1  # Least Significant Bit first | 先发送低位/低字节
    
    # Chip select lines | 片选线
    CS0: int = 0  # Chip Select 0 | 片选0
    CS1: int = 1  # Chip Select 1 | 片选1
    CS2: int = 2  # Chip Select 2 | 片选2
    CS3: int = 3  # Chip Select 3 | 片选3
    
    def __init__(self, id: int, mode: int = MODE_MASTER, baudrate: int = 500000,
                polarity: int = 0, phase: int = 0, bits: int = 8, 
                firstbit: int = MSB, sck: Optional[int] = None, 
                mosi: Optional[int] = None, miso: Optional[int] = None,
                cs0: Optional[int] = None, cs1: Optional[int] = None,
                cs2: Optional[int] = None, cs3: Optional[int] = None) -> None:
        """Initialize SPI controller | 初始化SPI控制器
        
        Args:
            id: SPI device ID, range [0,4]. Currently only 0, 1, and 4 (SPI_SOFT) are supported | 
                SPI ID，取值范围[0,4]。目前只支持0和1、4（.SPI_SOFT）
                - 0, 1: Hardware SPI in master mode | 0, 1: 硬件SPI主机模式
                - 2: Hardware SPI in slave mode (not implemented) | 2: 硬件SPI从机模式（未实现）
                - 3: Reserved for SPI Flash | 3: 保留用于SPI Flash
                - 4: Software SPI simulation | 4: 软件SPI模拟
            mode: SPI mode. Currently only MODE_MASTER is supported | 
                SPI模式。目前只支持MODE_MASTER
            baudrate: SPI baud rate (frequency) in Hz | SPI波特率（频率）(Hz)
                - Typical range: 1Hz to 45000000 (45MHz) | 典型范围：1Hz到45000000 (45MHz)
                - Default: 500000 (500kHz) | 默认：500000 (500kHz)
            polarity: Clock polarity when idle, 0 = low, 1 = high | 
                时钟空闲时极性，0 = 低电平，1 = 高电平
            phase: Clock phase for data sampling, 0 = first edge, 1 = second edge | 
                数据采样时钟相位，0 = 第一个跳变沿，1 = 第二个跳变沿
            bits: Data width in bits, range [4,32] | 数据宽度(位)，范围[4,32]
                - Default: 8 bits | 默认：8位
            firstbit: Bit transmission order, MSB or LSB | 位传输顺序，MSB或LSB
                - Default: MSB (most significant bit first) | 默认：MSB（先发送高位）
            sck: SCK (clock) pin number [0,47]. Can be None to use fm for pin mapping | 
                SCK（时钟）引脚编号[0,47]。可以为None以使用fm进行引脚映射
            mosi: MOSI (master out) pin number [0,47]. Can be None to use fm for pin mapping | 
                MOSI（主机输出）引脚编号[0,47]。可以为None以使用fm进行引脚映射
            miso: MISO (master in) pin number [0,47]. Can be None to use fm for pin mapping | 
                MISO（主机输入）引脚编号[0,47]。可以为None以使用fm进行引脚映射
            cs0: CS0 (chip select 0) pin number [0,47]. Can be None to use fm for pin mapping | 
                CS0（片选0）引脚编号[0,47]。可以为None以使用fm进行引脚映射
            cs1: CS1 (chip select 1) pin number [0,47]. Can be None to use fm for pin mapping | 
                CS1（片选1）引脚编号[0,47]。可以为None以使用fm进行引脚映射
            cs2: CS2 (chip select 2) pin number [0,47]. Can be None to use fm for pin mapping | 
                CS2（片选2）引脚编号[0,47]。可以为None以使用fm进行引脚映射
            cs3: CS3 (chip select 3) pin number [0,47]. Can be None to use fm for pin mapping | 
                CS3（片选3）引脚编号[0,47]。可以为None以使用fm进行引脚映射
        
        Note:
            - For hardware SPI (id 0-3), use sck/mosi/miso/cs0-cs3 or fm for pin mapping | 
              对于硬件SPI (id 0-3)，使用sck/mosi/miso/cs0-cs3或fm进行引脚映射
            - For software SPI (id 4), all pins must be specified | 
              对于软件SPI (id 4)，必须指定所有引脚
            - Currently only standard 4-wire Motorola mode is supported | 
              目前仅支持标准4线摩托罗拉模式
            - SPI3 (id=3) is reserved for internal SPI Flash | 
              SPI3 (id=3) 已保留用于内部SPI Flash
        
        Example:
            # Hardware SPI master mode | 硬件SPI主机模式
            spi = SPI(SPI.SPI1, mode=SPI.MODE_MASTER, baudrate=10000000,
                     polarity=0, phase=0, bits=8, firstbit=SPI.MSB,
                     sck=28, mosi=29, miso=30, cs0=27)
            
            # Software SPI | 软件SPI
            spi_soft = SPI(SPI.SPI_SOFT, mode=SPI.MODE_MASTER, baudrate=1000000,
                          sck=10, mosi=11, miso=12, cs0=13)
        """
        ...
    
    def init(self, id: int, mode: int = MODE_MASTER, baudrate: int = 500000,
            polarity: int = 0, phase: int = 0, bits: int = 8, 
            firstbit: int = MSB, sck: Optional[int] = None, 
            mosi: Optional[int] = None, miso: Optional[int] = None,
            cs0: Optional[int] = None, cs1: Optional[int] = None,
            cs2: Optional[int] = None, cs3: Optional[int] = None) -> None:
        """Initialize SPI controller (alternative to constructor) | 初始化SPI控制器（构造函数的替代方法）
        
        Same parameters as constructor | 参数与构造函数相同
        
        Example:
            spi = SPI(SPI.SPI1)
            spi.init(id=SPI.SPI1, mode=SPI.MODE_MASTER, baudrate=10000000,
                    polarity=0, phase=0, sck=28, mosi=29, miso=30, cs0=27)
        """
        ...
    
    def read(self, nbytes: int, write: int = 0x00, cs: int = CS0) -> bytes:
        """Read data from SPI slave device | 从SPI从机设备读取数据
        
        Args:
            nbytes: Number of bytes to read | 要读取的字节数
            write: Value to send on MOSI line during read (full-duplex operation) | 
                  读取时在MOSI线上发送的值（全双工操作）
                - Default: 0x00 (always low) | 默认：0x00（始终低电平）
            cs: Chip select line to use (SPI.CS0-SPI.CS3) | 要使用的片选线(SPI.CS0-SPI.CS3)
                - Default: SPI.CS0 | 默认：SPI.CS0
        
        Returns:
            Read data as bytes | 读取的数据(bytes类型)
        
        Example:
            # Read 5 bytes from slave device | 从从机设备读取5字节
            data = spi.read(5, write=0x00, cs=SPI.CS0)
            print("Read data:", data)
        """
        ...
    
    def readinto(self, buf: bytearray, write: int = 0x00, cs: int = CS0) -> None:
        """Read data from SPI slave device into buffer | 从SPI从机设备读取数据到缓冲区
        
        Args:
            buf: bytearray buffer to store read data | 用于存储读取数据的bytearray缓冲区
            write: Value to send on MOSI line during read (full-duplex operation) | 
                  读取时在MOSI线上发送的值（全双工操作）
                - Default: 0x00 (always low) | 默认：0x00（始终低电平）
            cs: Chip select line to use (SPI.CS0-SPI.CS3) | 要使用的片选线(SPI.CS0-SPI.CS3)
                - Default: SPI.CS0 | 默认：SPI.CS0
        
        Example:
            # Read 4 bytes into buffer | 读取4字节到缓冲区
            buffer = bytearray(4)
            spi.readinto(buffer, write=0x00, cs=SPI.CS0)
            print("Buffer contents:", buffer)
        """
        ...
    
    def write(self, buf: Union[bytes, bytearray], cs: int = CS0) -> None:
        """Write data to SPI slave device | 向SPI从机设备写入数据
        
        Args:
            buf: Data to write (bytes or bytearray) | 要写入的数据(bytes或bytearray)
            cs: Chip select line to use (SPI.CS0-SPI.CS3) | 要使用的片选线(SPI.CS0-SPI.CS3)
                - Default: SPI.CS0 | 默认：SPI.CS0
        
        Example:
            # Write string data | 写入字符串数据
            spi.write(b'1234', cs=SPI.CS0)
            
            # Write binary data | 写入二进制数据
            data = bytearray([0x01, 0x02, 0x03, 0x04])
            spi.write(data, cs=SPI.CS0)
        """
        ...
    
    def write_readinto(self, write_buf: Union[bytes, bytearray], 
                      read_buf: bytearray, cs: int = CS0) -> None:
        """Write data and read response simultaneously (full-duplex) | 同时写入数据和读取响应（全双工）
        
        Args:
            write_buf: Data to write (bytes or bytearray) | 要写入的数据(bytes或bytearray)
            read_buf: bytearray buffer to store read data | 用于存储读取数据的bytearray缓冲区
            cs: Chip select line to use (SPI.CS0-SPI.CS3) | 要使用的片选线(SPI.CS0-SPI.CS3)
                - Default: SPI.CS0 | 默认：SPI.CS0
        
        Example:
            # Full-duplex communication | 全双工通信
            write_data = b'1234'
            read_buffer = bytearray(4)
            spi.write_readinto(write_data, read_buffer, cs=SPI.CS0)
            print("Read response:", read_buffer)
        """
        ...
    
    def deinit(self) -> None:
        """Deinitialize SPI hardware and release resources | 反初始化SPI硬件并释放资源
        
        Stops SPI operation, releases hardware resources, and closes SPI clock | 
        停止SPI操作，释放硬件资源，并关闭SPI时钟
        
        Example:
            spi.deinit()  # Properly cleanup SPI resources | 正确清理SPI资源
        """
        ...
    
    def __del__(self) -> None:
        """Destructor, same as deinit() | 析构函数，与deinit()相同
        
        Automatically called when SPI object is destroyed | SPI对象销毁时自动调用
        """
        ...
        
class WDT:
    """Watchdog Timer (WDT) | 看门狗定时器
    
    Hardware watchdog timer that resets the system when the application crashes or becomes unresponsive.
    Once started, the system will automatically reset after timeout if not regularly fed.
    | 用于在应用程序崩溃且最终进入不可恢复状态时重启系统的硬件看门狗定时器。
    一旦开始，当硬件运行期间没有定期进行喂狗（feed）就会在超时后自动复位。
    
    Features:
    - Hardware-based watchdog with automatic system reset | 基于硬件的看门狗，支持自动系统复位
    - Configurable timeout in milliseconds | 可配置的超时时间（毫秒）
    - Optional callback function on timeout | 超时时可选的回调函数
    - Context data can be passed to callback | 可向回调函数传递上下文数据
    - Multiple watchdog instances supported (ID 0-2) | 支持多个看门狗实例（ID 0-2）
    """
    
    def __init__(self, id: int, timeout: int = 4000, 
                callback: Optional[Callable[['WDT'], None]] = None, 
                context: Optional[Dict[str, Any]] = None) -> None:
        """Initialize Watchdog Timer | 初始化看门狗定时器
        
        Args:
            id: Watchdog ID to distinguish different watchdogs, range [0, 2] | 
                看门狗ID用于区分不同的看门狗，范围[0, 2]
            timeout: Watchdog timeout in milliseconds (ms) | 
                看门狗超时时间，单位为毫秒（ms）
                - Minimum: 1ms | 最小值：1ms
                - Maximum: Depends on hardware (typically several seconds) | 最大值：取决于硬件（通常几秒）
                - Default: 4000ms (4 seconds) | 默认：4000ms（4秒）
            callback: Optional callback function to execute on timeout | 
                可选的回调函数，在超时时执行
                - Signature: def callback(wdt: WDT) -> None | 签名：def callback(wdt: WDT) -> None
                - The callback receives the WDT object itself as parameter | 回调函数接收WDT对象本身作为参数
            context: Optional context data to pass to callback function | 
                可选的上下文数据，传递给回调函数
                - Default: Empty dictionary {} | 默认：空字典{}
                - Can be accessed via wdt.context() method in callback | 可通过回调中的wdt.context()方法访问
        
        Note:
            - Once initialized, the watchdog starts immediately | 
              一旦初始化，看门狗立即启动
            - The application must call feed() regularly to prevent reset | 
              应用程序必须定期调用feed()以防止复位
            - Callback function is executed before system reset | 
              回调函数在系统复位前执行
            - In callback, you can feed() or stop() the watchdog to prevent reset | 
              在回调函数中，可以调用feed()或stop()来防止复位
        
        Example:
            # Basic usage | 基础使用
            wdt = WDT(id=0, timeout=3000)  # 3 second timeout | 3秒超时
            
            # Advanced usage with callback | 带回调的高级使用
            def on_wdt(wdt):
                print("Watchdog timeout!", wdt.context())
                wdt.feed()  # Feed to prevent reset | 喂狗以防止复位
            
            wdt = WDT(id=1, timeout=4000, callback=on_wdt, context={"app": "main"})
        """
        ...
    
    def feed(self) -> None:
        """Feed the watchdog timer | 喂养看门狗
        
        Resets the watchdog timer to prevent system reset. This should be called regularly
        when the application is functioning normally.
        | 重置看门狗定时器以防止系统重置。当应用程序正常运行时应定期调用。
        
        Note:
            - Must be called before timeout expires | 必须在超时到期前调用
            - Should only be called after verifying application is working properly | 
              应仅在验证应用程序正常工作后才调用
            - In callback function, feeding prevents system reset | 
              在回调函数中，喂狗可以防止系统复位
        
        Example:
            wdt = WDT(id=0, timeout=5000)
            while True:
                # Application logic here | 应用程序逻辑
                wdt.feed()  # Reset watchdog timer | 重置看门狗定时器
                time.sleep(1)
        """
        ...
    
    def stop(self) -> None:
        """Stop the watchdog timer | 停止看门狗定时器
        
        Disables the watchdog timer and releases hardware resources. After stopping,
        the watchdog will no longer monitor the system or cause resets.
        | 禁用看门狗定时器并释放硬件资源。停止后，看门狗将不再监控系统或导致复位。
        
        Note:
            - Use with caution - stopping watchdog removes system protection | 
              谨慎使用 - 停止看门狗会移除系统保护
            - Cannot be restarted once stopped (create new WDT object instead) | 
              一旦停止无法重新启动（请创建新的WDT对象）
            - Useful for debugging or when watchdog is no longer needed | 
              适用于调试或不再需要看门狗时
        
        Example:
            wdt = WDT(id=0, timeout=3000)
            # ... application logic ...
            wdt.stop()  # Disable watchdog when no longer needed | 当不再需要时禁用看门狗
        """
        ...
    
    def context(self) -> Dict[str, Any]:
        """Get context data for callback function | 获取回调函数的上下文数据
        
        Returns the context dictionary that was passed during initialization. This is
        typically used within the callback function to access application-specific data.
        | 返回初始化时传递的上下文字典。这通常在回调函数中使用，以访问应用程序特定数据。
        
        Returns:
            Context dictionary | 上下文字典
        
        Example:
            def on_wdt(wdt):
                context = wdt.context()
                app_name = context.get("app", "unknown")
                print(f"Watchdog timeout for application: {app_name}")
                # Handle timeout based on context | 根据上下文处理超时
        """
        ...