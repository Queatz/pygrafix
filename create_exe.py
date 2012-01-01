from distutils.core import setup
import py2exe
import sys

sys.argv = [sys.argv[0], "py2exe"]

setup(
    console = ["test.py"],
    data_files = ["map.png"],
    zipfile = "dependencies.dat",
    options = {
        "py2exe" : {
            "optimize": 2,
            "bundle_files": 2,
        }
    }
)

# ugly hack to wait until dependencies.dat is created for further building, one second timeout
import subprocess
import os.path
import shutil
import time

start = time.clock()
while not os.path.exists("dist\\dependencies.dat"):
    now = time.clock()

    if (now - start) > 1:
        raise Exception("Waiting for dist\\dependencies.dat took too long")

# repack using 7z
subprocess.call("7z -aoa x dist\\dependencies.dat -odist\\dependencies\\")
os.remove("dist\\dependencies.dat")
os.chdir("dist\\dependencies")
subprocess.call("7z a -tzip -mx9 ..\\dependencies.dat -r")
os.chdir("..")
shutil.rmtree("dependencies")
os.remove("w9xpopen.exe")

# compress more with upx (optional)
subprocess.call("upx --best *.*")

# and pack all together for easy dist
subprocess.call("7z a -tzip -mx9 dist.zip -r")

# and return to original dir
os.chdir("..")
