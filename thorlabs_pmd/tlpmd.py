import usb.core
import usbtmc
import sys
from typing import List, NamedTuple, Tuple

if sys.platform == 'win32':
    import libusb_package
    libusb_backend = libusb_package.get_libusb1_backend()
else:
    libusb_backend = None

REN_CONTROL = 160 # Optional. Mechanism to enable or disable local controls on a device.
GO_TO_LOCAL = 161 # Optional. Mechanism to enable local controls on a device. 

class DeviceNotFound(Exception): ...

THORLABS_VID = 0x1313
PM100D_PID = 0x8078
LINE_FREQUENCY_EUROPE = 50
S120C_APERTURE_SIZE_MM = 9.5
PID_RANGE = (0x8078, 0x8079) # TODO check actual values
area = 3.14159 * (S120C_APERTURE_SIZE_MM/2)**2

# S120C 
# Active Detector Area 	9.7 mm x 9.7 mm
# Aperture Size 	Ø9.5 mm
# to display the power or energy density or the light intensity value in W/cm² or
# J/cm² in the right sub display it is necessary to enter the diameter of the incident
# beam or at an overfilled sensor the diameter of the sensor aperture.

class DevInfo(NamedTuple):
    vid: int
    pid: int
    serial_number: str

def list_powermeters() -> List[DevInfo]:
    
    devices = usb.core.find(
        idVendor = THORLABS_VID, 
        backend = libusb_backend, 
        custom_match = lambda d: d.idProduct in range(*PID_RANGE),
        find_all = True
    )

    res = []
    for dev in devices:
        res.append(DevInfo(
            vid = dev.idVendor,
            pid = dev.idProduct,
            serial_number = dev.serial_number 
        ))

    return res

class TLPMD:

    def __init__(
            self,
            device_info: DevInfo,
        ) -> None:
        
        self.instr = usbtmc.Instrument(device_info.vid, device_info.pid, device_info.serial_number)
        self.instr.clear = lambda: None
        self.instr.open()
        self.instr.device.ctrl_transfer(bmRequestType=0xA1, bRequest=REN_CONTROL, wValue=0x0001, wIndex=0x0000, data_or_wLength=1)
        self.initialize()
        
    def initialize(self): 
        self.instr.write("*CLS;*SRE 0;*ESE 0;:STAT:PRES")
        self.check_error_code()
        self.instr.write("ABOR")
        self.instr.write("CONF:POW")
        self.instr.write("SENS:AVER:COUN 1")
        self.check_error_code()

        # self.instr.write("*CLS;*SRE 0;*ESE 0;:STAT:PRES")
        # self.check_error_code()

        # print(self.instr.ask("SYST:SENS:IDN?"))
        # print(self.instr.ask("STAT:AUX:COND?"))
        # print(self.instr.ask("*IDN?"))
        # print(self.instr.ask("CAL:STR?"))

        # print(self.instr.ask("SYST:SENS:IDN?"))    
        # print(self.instr.ask("SENS:CORR:WAV? MIN"))
        # print(self.instr.ask("SENS:CORR:WAV? MAX"))
        
        # self.instr.write("ABOR")
        # self.instr.write("CONF:Current")

        # print(self.instr.ask("SENS:CORR?"))
        # print(self.instr.ask("SENS:CORR? MIN"))
        # print(self.instr.ask("SENS:CORR? MAX"))
        # print(self.instr.ask("SENS:CORR:BEAM?"))
        # print(self.instr.ask("SENS:CORR:BEAM? MIN"))
        # print(self.instr.ask("SENS:CORR:BEAM? MAX"))
        # print(self.instr.ask("SENS:CORR:WAV?"))
        # print(self.instr.ask("SENS:CORR:WAV? MIN"))
        # print(self.instr.ask("SENS:CORR:WAV? MAX"))
        # print(self.instr.ask("SENS:CORR:POW:PDI:RESP?"))
        # print(self.instr.ask("INP:FILT?"))
        # print(self.instr.ask("SENS:CORR:COLL:ZERO:MAGN?"))
        # print(self.instr.ask("SENS:CURR:RANG:AUTO?"))
        # print(self.instr.ask("SENS:CURR:RANG:UPP?"))
        # print(self.instr.ask("SENS:CURR:RANG:UPP? MIN"))

        # self.instr.write("SENS:AVER:COUN 1")
        # self.check_error_code()
        # print(self.instr.ask("SENS:CURR:RANG:UPP?"))
        # print(self.instr.ask("Read?"))

        # print(self.instr.ask("SENS:CORR?"))
        # print(self.instr.ask("SENS:CORR? MIN"))
        # print(self.instr.ask("SENS:CORR? MAX"))
        # print(self.instr.ask("SENS:CORR:BEAM?"))
        # print(self.instr.ask("SENS:CORR:BEAM? MIN"))
        # print(self.instr.ask("SENS:CORR:BEAM? MAX"))
        # print(self.instr.ask("SENS:CORR:WAV?"))
        # print(self.instr.ask("SENS:CORR:WAV? MIN"))
        # print(self.instr.ask("SENS:CORR:WAV? MAX"))
        # print(self.instr.ask("SENS:CORR:POW:PDI:RESP?"))
        # print(self.instr.ask("INP:FILT?"))
        # print(self.instr.ask("SENS:CORR:COLL:ZERO:MAGN?"))
        # print(self.instr.ask("SENS:CURR:RANG:AUTO?"))
        # print(self.instr.ask("SENS:CURR:RANG:UPP?"))
        # print(self.instr.ask("SENS:CURR:RANG:UPP? MIN"))

        # print(self.instr.ask("SENS:CORR:BEAM?"))
        # print(self.instr.ask("SENS:CORR:BEAM?"))

        # print(self.instr.ask("SENS:CORR?"))
        # print(self.instr.ask("SENS:CORR? MIN"))
        # print(self.instr.ask("SENS:CORR? MAX"))
        # print(self.instr.ask("SENS:CORR:BEAM?"))
        # print(self.instr.ask("SENS:CORR:BEAM? MIN"))
        # print(self.instr.ask("SENS:CORR:BEAM? MAX"))
        # print(self.instr.ask("SENS:CORR:WAV?"))
        # print(self.instr.ask("SENS:CORR:WAV? MIN"))
        # print(self.instr.ask("SENS:CORR:WAV? MAX"))
        # print(self.instr.ask("SENS:CORR:POW:PDI:RESP?"))
        # print(self.instr.ask("INP:FILT?"))
        # print(self.instr.ask("SENS:CORR:COLL:ZERO:MAGN?"))
        # print(self.instr.ask("SENS:CURR:RANG:AUTO?"))
        # print(self.instr.ask("SENS:CURR:RANG:UPP?"))
        # print(self.instr.ask("SENS:CURR:RANG:UPP? MIN"))
        
        # print(self.instr.ask("SENS:CURR:RANG:AUTO?"))
        # print(self.instr.ask("SENS:CURR:RANG:UPP?"))
        # print(self.instr.ask("SENS:CURR:RANG:UPP? MIN"))
        # print(self.instr.ask("Read?"))
        # print(self.instr.ask("Read?"))
        # print(self.instr.ask("Read?"))
        # print(self.instr.ask("Read?"))

    def check_error_code(self) -> None:
        error = self.instr.ask("SYST:ERR?")
        code, descr = error.split(',', 1)
        code, descr = int(code), descr.strip('"')
        if code != 0:
            raise RuntimeError(f'Error code {code}: {descr}')

    def get_line_frequency_Hz(self) -> float:
        return float(self.instr.ask(f"SYST:LFR?"))

    def set_line_frequency_Hz(self, line_frequency: float) -> None:
        self.instr.write(f"SYST:LFR {line_frequency}")
        self.check_error_code()

    def get_beam_diameter_mm(self) -> float:
        return float(self.instr.ask("SENS:CORR:BEAM?"))
    
    def set_beam_diameter_mm(self, diameter: float) -> None:
        self.instr.write(f"SENS:CORR:BEAM {diameter}")
        self.check_error_code()

    def get_max_wavelength_nm(self) -> float:
        return float(self.instr.ask(f"SENS:CORR:WAV? MAX"))
    
    def get_min_wavelength_nm(self) -> float:
        return float(self.instr.ask(f"SENS:CORR:WAV? MIN"))
    
    def get_wavelength_nm(self) -> float:
        return float(self.instr.ask(f"SENS:CORR:WAV?"))

    def set_wavelength_nm(self, wavelength: float) -> None:
        self.instr.write(f"SENS:CORR:WAV {wavelength}")
        self.check_error_code()

    def get_power_mW(self) -> float:
        power = self.instr.ask("Read?")
        return float(power)*10**3
    
    def get_power_density_mW_cm2(self) -> float:
        beam_diameter_cm = self.get_beam_diameter_mm() * 0.1
        area_cm2 = 3.14159 * (beam_diameter_cm/2)**2
        return self.get_power_mW()/area_cm2

    def close(self) -> None:
        self.instr.device.ctrl_transfer(bmRequestType=0xA1, bRequest=GO_TO_LOCAL, wValue=0x0000, wIndex=0x0000, data_or_wLength=1)
        self.instr.device.ctrl_transfer(bmRequestType=0xA1, bRequest=REN_CONTROL, wValue=0x0000, wIndex=0x0000, data_or_wLength=1)
        self.instr.close()
        self.instr = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

if __name__ == '__main__':

    powermeters = list_powermeters()
    dev = TLPMD(powermeters[0])
    dev.set_wavelength_nm(550)
    print(dev.get_power_density_mW_cm2())
    dev.close()