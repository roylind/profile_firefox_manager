from setuptools import setup, find_packages

setup(name='profile_firefox_manager',
      version="0.1",
      packages=find_packages(),
	  install_requires=["PySide2"],
      entry_points={
            'console_scripts': ['ProfileFirefoxManager=profile_firefox_manager.profile_browser:main'],
      }
     )
