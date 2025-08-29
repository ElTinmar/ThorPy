import usbtmc

THORLABS_VID = 0x1313
PM100D_PID = 0x8078
LINE_FREQUENCY_EUROPE = 50
S120C_APERTURE_SIZE = 9.5

area = 3.14159 * (S120C_APERTURE_SIZE/2)**2

# S120C 
# Active Detector Area 	9.7 mm x 9.7 mm
# Aperture Size 	Ø9.5 mm
# to display the power or energy density or the light intensity value in W/cm² or
# J/cm² in the right sub display it is necessary to enter the diameter of the incident
# beam or at an overfilled sensor the diameter of the sensor aperture.

#TODO handle multiple devices with serial number

class TLPMD:

    def __init__(
            self,
            PID: int = PM100D_PID,
        ) -> None:
        
        self.instr = usbtmc.Instrument(THORLABS_VID, PID)
        self.instr.write("SENS:RANGE:AUTO ON")
        self.instr.write("SENS:POW:UNIT W")
        self.instr.write("SENS:AVER:1000")
        self.instr.write(f"SYST:LFR:{LINE_FREQUENCY_EUROPE}")

        #self.instr.write(f"SENS:CORR:BEAM {S120C_APERTURE_SIZE}") 
        self.sensor_area = self.instr.ask("SENS:CORR:BEAM?") 
        print(self.instr.ask("CAL:STR?"))
        

    def set_wavelength(self, wavelength: float) -> None:
        self.instr.write(f"SENS:CORR:WAV {wavelength}")

    def get_power(self) -> float:
        power = self.instr.ask("MEAS:POW?")
        return float(power)
    
    def get_power_density(self) -> float:
        
        return self.get_power()/self.sensor_area

if __name__ == '__main__':

    dev = TLPMD()