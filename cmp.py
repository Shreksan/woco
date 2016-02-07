from distutils.core import setup
import py2exe

Mydata_files = [('lib', ['./lib/std_dict.txt'])]
excludes=["pywin", "pywin.debugger", "pywin.debugger.dbgcon",
            "pywin.dialogs", "pywin.dialogs.list", 
            "Tkconstants","Tkinter","tcl"]

setup(
    console=["woco.py"], zipfile='library.zip',
    data_files = Mydata_files,
    options={"py2exe": {"includes":["translate_func"], "bundle_files":3, "optimize": 2, "excludes":excludes, "compressed":True}}
)

