from distutils.core import setup
import py2exe

setup(console=['main.py'])
setup(console=[
    { "script":"main.py",
            "icon_resources": [(0, "icon.ico")]
    }])