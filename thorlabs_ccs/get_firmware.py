import subprocess
from pathlib import Path
import urllib.request
import shutil

# this is a bit brittle since it can change anytime
URL = "https://www.thorlabs.com/software/THO/OSA/V2_90/ThorlabsOSASW_Full_setup.exe"

def extract_ccs_firmware():

    # Install innoextract check (optional)
    if shutil.which("innoextract") is None:
        raise RuntimeError("Please install 'innoextract' before running this function.")

    # Download the installer
    print(f'Downloading {URL}')
    exe_path = Path("ThorlabsOSASW_Full_setup.exe")
    urllib.request.urlretrieve(URL, exe_path)

    # Create directories
    ccs_dir = Path("ccs_firmware")
    temp_dir = Path("temp_extract")
    ccs_dir.mkdir(exist_ok=True)
    temp_dir.mkdir(exist_ok=True)

    # Run innoextract
    includes = [
        "app/CCS/inf/Loader/CCS100.spt",
        "app/CCS/inf/Loader/CCS125.spt",
        "app/CCS/inf/Loader/CCS150.spt",
        "app/CCS/inf/Loader/CCS175.spt",
        "app/CCS/inf/Loader/CCS200.spt",
    ]
    cmd = ["innoextract", "--extract", f"--output-dir={temp_dir}"] + sum([["--include", f] for f in includes], []) + [str(exe_path)]
    subprocess.run(cmd, check=True)

    # Move firmware files
    for file in temp_dir.glob("app/CCS/inf/Loader/CCS*.spt"):
        shutil.move(str(file), ccs_dir)

    # Cleanup
    shutil.rmtree(temp_dir)
    exe_path.unlink()

    print(f"Firmware extraction complete. Files are in {ccs_dir}")

if __name__ == '__main__':

    extract_ccs_firmware()