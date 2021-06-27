from setuptools import setup

APP = ['app.py']
DATA_FILES = ['AppIcon.icns']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'AppIcon.icns',
    'plist': {
        'CFBundleShortVersionString': '1.0.0',
        'LSUIElement': True,
    },
    'packages': ['rumps']
}

setup(
    app=APP,
    name='Musicbar',
    py_modules=['helper'],
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['rumps']
)
