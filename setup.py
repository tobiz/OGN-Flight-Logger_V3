from setuptools import setup, find_packages 
#from setuptools import setup

# See https://medium.com/small-things-about-python/lets-talk-about-python-packaging-6d84b81f1bb5#.pjxrklmi6

setup(name='OGN_Flogger',   
      version='0.3.1.14',
      scripts=['flogger_gui.py'],      # Command to run 
      description='Realtime logging of glider flights from Flarm data',
      long_description='Realtime logging and tracking of gliders from Flarm signals using APRS.',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
      ],
      keywords='OGN Open Glider Flarm Logging Tracking',
      url='http://github.com/tobiz/OGN-Flight-Logger_V3',
      author='tobiz',
      author_email='pjrobinson@metronet.co.uk',
      license='GPL', 
      py_modules=[
                'flarm_db',
                'flogger3',
                'flogger_dump_flights',
                'flogger_dump_IGC',
                'flogger_dump_tracks',
                'flogger_email_log',
                'flogger_email_msg',
                'flogger_find_tug',
                'flogger_functions',
                'flogger_get_coords',
                'flogger_gui',
                'flogger_landout',
                'flogger_OGN_db',
                'flogger_process_log',
                'flogger_progress_indicator',
                'flogger_resources_rc',
                'flogger_settings',
                'flogger_signals',
                'flogger_test_YorN',
                'flogger_ui',
                'gpxTracks',
                'libfap',
                'open_db'
                ],
                
      install_requires=[
                        'aerofiles>=0.3',
                        'configobj>=4.7.2',
                        'geocoder>=1.4.0',
                        'geopy>=1.11.0',
                        'pytz>=2012c',
                        'requests>=2.13.0',
                        'setuptools>=3.3',
                        'LatLon>=1.0.2',
#                        'PyQt4>=4.11.4',
                        'pyephem>=3.7.6.0',
                        'protobuf>=3.2.0',
                        'parse>=1.8.0',
                        'adhocracy_pysqlite>=2.6.3'
                        ],
#      data_files=[('', ['*.png'])],  
#      package_data={'': ['*.png']},
      include_package_data=True,
      zip_safe=False)