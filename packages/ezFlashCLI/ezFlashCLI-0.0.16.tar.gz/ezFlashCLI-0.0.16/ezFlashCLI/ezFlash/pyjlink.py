# The MIT License (MIT)
# Copyright (c) 2019 ezflash
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import os,sys
from enum import IntEnum
from ctypes import CDLL, Structure, c_char_p, c_uint8, c_uint16, c_uint32, byref, c_uint, c_ubyte, c_ulonglong, c_char, c_int, c_byte
import logging

class JLINKARM_HOSTIF(IntEnum):
    JLINKARM_HOSTIF_USB = 1
    JLINKARM_HOSTIF_IP  = 2
        
class JLINKARM_TIF(IntEnum):
    JLINKARM_TIF_JTAG =              0
    JLINKARM_TIF_SWD =               1
    JLINKARM_TIF_BDM3 =              2
    JLINKARM_TIF_FINE =              3
    JLINKARM_TIF_2_WIRE_JTAG_PIC32 = 4
    JLINKARM_TIF_SPI  =              5
    JLINKARM_TIF_C2 =                6

class JLINKARM_SPEED(IntEnum):    
    JLINKARM_SPEED_AUTO =         0
    JLINKARM_SPEED_INVALID =      0xFFFE
    JLINKARM_SPEED_ADAPTIVE =     0xFFFF
     
class JLINKARM_EMU_CONNECT_INFO(Structure):
    _fields_ = [("SerialNumber", c_uint),             # This is the serial number reported in the discovery process, which is the "true serial number" for newer J-Links and 123456 for older J-Links.
                ("Connection", c_uint),               # Either JLINKARM_HOSTIF_USB = 1 or JLINKARM_HOSTIF_IP = 2
                ("USBAddr", c_uint),                  # USB Addr. Default is 0, values of 0..3 are permitted (Only filled if for J-Links connected via USB)
                ("aIPAddr", c_ubyte * 16),            # IP Addr. in case emulator is connected via IP. For IP4 (current version), only the first 4 bytes are used.
                ("Time", c_int),                      # J-Link via IP only: Time period [ms] after which we have received the UDP discover answer from emulator (-1 if emulator is connected over USB)
                ("Time_us", c_ulonglong),             # J-Link via IP only: Time period [us] after which we have received the UDP discover answer from emulator (-1 if emulator is connected over USB)
                ("HWVersion", c_uint),                # J-Link via IP only: Hardware version of J-Link
                ("abMACAddr", c_ubyte * 6),           # J-Link via IP only: MAC Addr
                ("acProduct", c_byte * 32),           # Product name
                ("acNickName", c_char * 32),          # J-Link via IP only: Nickname of J-Link
                ("acFWString", c_char * 112),         # J-Link via IP only: Firmware string of J-Link
                ("IsDHCPAssignedIP", c_char),         # J-Link via IP only: Is J-Link configured for IP address reception via DHCP?
                ("IsDHCPAssignedIPIsValid", c_char),  # J-Link via IP only
                ("NumIPConnectionsIsValid", c_char),  # J-Link via IP only
                ("aPadding", c_ubyte *  34)]          # Pad struct size to 264 bytes


class JLINKARM_ERROR_CODES(IntEnum):
    JLINK_ERR_EMU_NO_CONNECTION =          -256 # (0xFFFFFF00) No connection to emulator / Connection to emulator lost
    JLINK_ERR_EMU_COMM_ERROR =             -257 # (0xFFFFFEFF) Emulator communication error (host-interface module reproted error)
    JLINK_ERR_DLL_NOT_OPEN =               -258 # (0xFFFFFEFE) DLL has not been opened but needs to be (JLINKARM_Open() needs to be called first)
    JLINK_ERR_VCC_FAILURE =                -259 # (0xFFFFFEFD) Target system has no power (Measured VTref < 1V)
    JLINK_ERR_INVALID_HANDLE =             -260 # (0xFFFFFEFC) File handle / memory area handle needed for operation, but given handle is not valid
    JLINK_ERR_NO_CPU_FOUND =               -261 # (0xFFFFFEFB) Could not find supported CPU
    JLINK_ERR_EMU_FEATURE_NOT_SUPPORTED =  -262 # (0xFFFFFEFA) Emulator does not support the selected feature (Usually returned by functions which need specific emulator capabilities)
    JLINK_ERR_EMU_NO_MEMORY =              -263 # (0xFFFFFEF9) Emulator does not have enough memory to perform the requested operation
    JLINK_ERR_TIF_STATUS_ERROR =           -264 # (0xFFFFFEF8) Things such as "TCK is low but should be high"
    JLINK_ERR_FLASH_PROG_COMPARE_FAILED =  -265
    JLINK_ERR_FLASH_PROG_PROGRAM_FAILED =  -266
    JLINK_ERR_FLASH_PROG_VERIFY_FAILED =   -267
    JLINK_ERR_OPEN_FILE_FAILED =           -268
    JLINK_ERR_UNKNOWN_FILE_FORMAT =        -269
    JLINK_ERR_WRITE_TARGET_MEMORY_FAILED = -270

class pyJLinkException(Exception): 
    pass

class pyjlink(object):
    """Provides an API to a SEGGER J-Link debug probe.

    The J-Link can be connected to the host PC via USB or ethernet. Specific
    J-Link debug probe can be selected if multiple J-Links are connected.
    
    The pylink class allows functionality such as:
    
    * Initiate (open) a connection to a core on a target system
    * Close a connection to a target
    * Accessing the memory on a target system for reading and writing
    * Reset the core on the target system
    * Restart the core on the target system
    * Download a binary file (.hex format) to the memory on the target system
    
    Attributes:
        key: Windows Registry path for the SEGGER software
        library: Windows path for SEGGER SDK J-Link DLL
        serialno: Serial number of the J-Link which shall be selected
        iphost: Host name or an IP address for a connection to the J-Link via TCP/IP
        speed: Speed of the JTAG connection in kHz
        Device: Name of the device connected to the J-Link
        jl: Handle for the J-Link DLL
        logger: Handle for the class logger
    """    
    
    version = '1.01'
    
    def __init__(self):
        """Sets the initial state of the pyjlink object"""
        
        self.serialno = None
        self.iphost = None
        # Speed of JTAG connection in kHz.
        self.speed = 4000
        self.Device  = b'Cortex-M33' # select M33 by default to issue exit dormant state
        self.jl = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.library = None

    def __del__(self):
        self.close()
    
    def init(self):
        """Initializes the connection to the target system 
        
        Raises:
            TODO: TODO
        """    
        
        self.logger.debug('init')
        
        if self.library is None:
            import platform
            if platform.system() in 'Darwin':
                dll = 'libjlinkarm.dylib'
            elif platform.system() in 'Linux':
                if platform.machine().startswith("arm"):
                    dll = 'libjlinkarm_arm.so.6.82.2'
                else:
                    if platform.architecture()[0]=='64bit':
                        dll = 'libjlinkarm_x64.so.6.50.2'
                    else:
                        dll = 'libjlinkarm_x86.so.6.50.2*'
            else:
                if platform.architecture()[0]=='64bit':
                    dll = 'JLink_x64.dll'
                else:
                    dll = 'JLinkARM.dll'
                
            if getattr(sys, 'frozen', False):
                self.library = dll       
            else:
                self.library = os.path.join(os.path.dirname(__file__),'..','third-party','segger',dll)       
        try:
            self.jl = CDLL(self.library)
        except:
            logging.error('Error loading J-Link Library')
            sys.exit(1)
        
        self.logger.debug('J-Link library loaded')
        
        return
        # # Select and configure the connection to the J-Link via TCP/IP.         
        # if self.iphost is not None:
        #     self.logger.debug('Connect to the J-Link via TCP/IP.  Host name/IP address: ' + str(self.iphost))  
        #     iphostbuf = c_char_p(self.iphost.encode('UTF-8'))
        #     r = self.jl.JLINKARM_SelectIP(iphostbuf, 0)
        #     if r == 1:
        #         raise pyJLinkException('Error occurred during configuration of IP interface')
             
        # # Select a specific J-Link to be connected to by specifying the serial number of the number  
        # if self.serialno is not None:
        #     self.logger.debug('Selecting J-Link with the serial number: ' + str(self.serialno))
        #     c_serialno = c_uint32(self.serialno)
        #     r = self.jl.JLINKARM_EMU_SelectByUSBSN(c_serialno)
        #     if r < 0 :
        #         raise pyJLinkException('Error: Specific serial number not found on USB')
                
        # self.logger.debug("Opens the connection to J-Link")
        # self.jl.JLINKARM_Open.restype = c_char_p
        # sError = self.jl.JLINKARM_Open()
        # if sError is not None:
        #     raise pyJLinkException(sError)

        # self.logger.debug("Select device or core")
        # c_acIn =  c_char_p(b'Device = ' + self.Device)
        # acOut = b' ' * 80
        # c_acOut = c_char_p(acOut)
        # c_buffersize = c_int(80)
        # self.jl.JLINKARM_ExecCommand(c_acIn, c_acOut, c_buffersize)
        # if not acOut[0] == 0:
        #     raise pyJLinkException(acOut)
                
        # self.logger.debug("Selects the SWD interface")
        # c_interface = c_int(JLINKARM_TIF.JLINKARM_TIF_SWD.value)
        # self.jl.JLINKARM_TIF_Select(c_interface)

        # self.logger.debug("Set the speed for J-Link communication with the core")
        # c_speed = c_uint32(self.speed)
        # self.jl.JLINKARM_SetSpeed(c_speed)
        
        # self.logger.debug("Establish a connection to the target system")
        # r = self.jl.JLINKARM_Connect()
        # self.wr_mem(32, 0x50040300, 0x8)
        # if r == -1:
        #     raise pyJLinkException('Unspecified error')
        # elif r < 0 :
        #     raise pyJLinkException(JLINKARM_ERROR_CODES(r).name)
    


    def browse(self):
        maxDevice = 20
        interfaces = (JLINKARM_EMU_CONNECT_INFO * maxDevice)()

        if self.jl.JLINKARM_EMU_GetList(JLINKARM_HOSTIF.JLINKARM_HOSTIF_USB,byref(interfaces),c_int(maxDevice)):
            self.logger.debug("Get device List")
            return(interfaces)

    def connect(self,serialno):
        
        if type(serialno)  != type(int):
            try:
                serialno = int(serialno)
            except:
                self.logger.debug("Failed to interpret JLink id: {}, will use default interface".format(serialno))
                #return

        if serialno:
            self.logger.debug('Selecting J-Link with the serial number: ' + str(serialno))
            c_serialno = c_uint32(serialno)
            r = self.jl.JLINKARM_EMU_SelectByUSBSN(c_serialno)
            if r < 0 :
                raise pyJLinkException('Error: Specific serial number not found on USB')


        self.logger.debug("Opens the connection to J-Link")
        self.jl.JLINKARM_Open.restype = c_char_p
        sError = self.jl.JLINKARM_Open()
        if sError is not None:
            raise pyJLinkException(sError)

        self.logger.debug("Select device or core")
        c_acIn =  c_char_p(b'Device = ' + self.Device)
        acOut = b' ' * 80
        c_acOut = c_char_p(acOut)
        c_buffersize = c_int(80)
        self.jl.JLINKARM_ExecCommand(c_acIn, c_acOut, c_buffersize)
        if not acOut[0] == 0:
            raise pyJLinkException(acOut)
                
        self.logger.debug("Selects the SWD interface")
        c_interface = c_int(JLINKARM_TIF.JLINKARM_TIF_SWD.value)
        self.jl.JLINKARM_TIF_Select(c_interface)

        self.logger.debug("Set the speed for J-Link communication with the core")
        c_speed = c_uint32(self.speed)
        self.jl.JLINKARM_SetSpeed(c_speed)
        
        self.logger.debug("Establish a connection to the target system")
        if self.jl.JLINKARM_IsConnected():
            self.logger.debug("Closing existing connection")
            self.close()

        r = self.jl.JLINKARM_Connect()
        # self.wr_mem(32, 0x50040300, 0x8)
        if r == -1:
            raise pyJLinkException('Unspecified error')
        elif r < 0 :
            raise pyJLinkException(JLINKARM_ERROR_CODES(r).name)


        try:
            self.logger.debug("Read 69x identifier")
            id= self.rd_mem(32, 0x50040200, 4)
        except:
            self.logger.debug("Failed to read 69x identifier")
            self.logger.debug("Read 58x/68x identifier")
            id = self.rd_mem(8, 0x50003200, 5)
            pass
        

        c_acIn =  c_char_p(b'DisableInfoWinFlashDL')
        acOut = b' ' * 80
        c_acOut = c_char_p(acOut)
        c_buffersize = c_int(80)
        self.jl.JLINKARM_ExecCommand(c_acIn,c_acOut,c_buffersize)

        return(str(id))

    def close(self):
        """Closes the connection to the target system"""
        self.jl.JLINKARM_Close()

    def rd_mem(self, widthBits, addr, numItems):
        """Reads from target memory in units of widthBits-bits
        
        Args:
            widthBits: Word size (8, 16 or 32)
            
            addr: Memory address
            
            numItems: Number of items to be read
            
        Returns:
            A list with the containing numItems elements with the data
            read for the target memory starting at address addr.
            
        Raises:
            pyJLinkException: Failed to read data @ addr
        
        Example::
        
            values = obj.rd_mem(8,0x2000A000,1024)
        """
        
        pStatus = c_uint32(0)
        c_addr = c_uint32(addr)
        c_numItems = c_uint32(numItems)
        c_status = (c_uint8 * int(numItems))()
        
        if widthBits == 16:
            buftype = c_uint16 * int(numItems)
            buf = buftype()
            status = self.jl.JLINKARM_ReadMemU16(addr, numItems, buf, pStatus)

        elif widthBits == 8:
            buftype = c_uint8 * int(numItems)
            buf = buftype()
            status = self.jl.JLINKARM_ReadMemU8(c_addr, c_numItems, buf, pStatus)

        elif widthBits == 32:
            buftype = c_uint32 * int(numItems)
            buf = buftype()
            status = self.jl.JLINKARM_ReadMemU32(c_addr, c_numItems, buf, pStatus)

        self.logger.debug("Read @{:08X}, [{}]".format(addr,', '.join(hex(i) for i in buf)))
            
        if status != numItems:
            raise pyJLinkException("Failed to read {} @ 0x{:08X}".format(numItems, addr))            

        returnValue = [elem.real for elem in buf]
        return returnValue


    def wr_mem(self, widthBits, addr, wr_val):
        """Writes a unit of widthBits-bits to the target system.

        Args:
            widthBits: Word size (8, 16 or 32)
            
            addr: Memory address
            
            wr_val: Value to be written
            
        Returns:
            The status of the write access
            
            status == 0: O.K.
            
            status != 0: Error.
                
        Example::
        
            stat = obj.wr_mem(8,0x2000A000,20255)
        """

        c_addr = c_uint32(addr)
        if widthBits == 8:
            self.logger.debug("Written 0x{:02X} to 0x{:08X}".format(wr_val,addr))
            c_wr_val = c_uint8(wr_val)
            status = self.jl.JLINKARM_WriteU8(c_addr, c_wr_val)
        elif widthBits == 16:
            self.logger.debug("Written 0x{:04X} to 0x{:08X}".format(wr_val,addr))
            c_wr_val = c_uint16(wr_val)
            status = self.jl.JLINKARM_WriteU16(c_addr, c_wr_val)
        elif widthBits == 32:
            self.logger.debug("Written 0x{:08X} to 0x{:08X}".format(wr_val,addr))
            c_wr_val = c_uint32(wr_val)
            status = self.jl.JLINKARM_WriteU32(c_addr, c_wr_val)

        return status
            
    def reset(self):
        """Resets and halts the core on the target system"""
        
        self.jl.JLINKARM_Reset()
    def resetNoHalt(self):
        """Resets and halts the core on the target system"""
        
        self.jl.JLINKARM_ResetNoHalt()

    def go(self):
        """Restarts the core on the target system after it has been halted."""
        
        self.jl.JLINKARM_Go() 
        
    def _download(self, addr, filename):
        """Downloads a binary file to the target system
        
        Args:
            addr: Start address where the binary file is stored
            filename: File name of the binary file
        """

        import platform
        if platform.architecture()[0] == '64bit':        
            filenamebuf = c_char_p(filename.encode('UTF-8'))
            c_addr = c_uint32(addr)
            self.jl.JLINK_DownloadFile(filenamebuf, c_addr)
        else:
            from intelhex import IntelHex
            ih = IntelHex()
            
            extension = os.path.splitext(filename)[1][1:]
            ih.fromfile(filename,format=extension)
            
            for (a, d) in zip(ih.addresses(), ih.tobinarray()):
                self.wr_mem(8, addr+a, d)
                
