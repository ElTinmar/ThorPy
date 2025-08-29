from ctypes import CDLL, c_int, c_double, byref, c_void_p

lib = CDLL("./libtlccs.so")

ccs_handle=c_int(0)

# this does not work on linux
lib.tlccs_init(b'USB0::0x1313::0x8081::M00300454::RAW', 0, 0, byref(ccs_handle))   

integration_time=c_double(10.0e-3)
lib.tlccs_setIntegrationTime(ccs_handle, integration_time)

wavelengths=(c_double*3648)()
lib.tlccs_getWavelengthData(ccs_handle, 0, byref(wavelengths), c_void_p(None), c_void_p(None))

#start scan
lib.tlccs_startScan(ccs_handle)

#wait for acquisition and data fetching finish
status=c_int(0)
while(status.value & 0x0010)==0:
    lib.tlccs_getDeviceStatus(ccs_handle,byref(status))

#retrieve data
data_array=(c_double*3648)()
lib.tlccs_getScanData(ccs_handle, byref(data_array))

for w, i in zip(wavelengths, data_array):
    print(f'{w} nm', i)

#close
lib.tlccs_close (ccs_handle)