import sys
import os
import string
from PyQt4 import QtGui, QtCore, uic
from PyQt4.Qt import SIGNAL
import subprocess
from parse import *
from ConfigParser import *
from configobj import ConfigObj
from flogger3 import *
from flogger_settings import * 
from LatLon import *


# 20170311 

# get the directory of this script
path = os.path.dirname(os.path.abspath(__file__))
print("Path: " + path) 
#settings = class_settings()

Ui_MainWindow, base_class = uic.loadUiType(os.path.join(path,"flogger_config_1.ui"))
#Ui_MainWindow, base_class = uic.loadUiType(os.path.join(path,"flogger.ui"))


#class Window (QtGui.QMainWindow, form_class):
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        global settings
        settings = class_settings()
        
        self.actionStart.triggered.connect(self.floggerStart)  
        self.actionStop.triggered.connect(self.floggerStop)  
        self.actionQuit.triggered.connect(self.floggerQuit)  
#        self.AirfieldBaseButton.clicked.connect(self.floggerAirfieldEdit) 
#        self.AirfieldBaseButton.clicked.connect(self.floggerAirfieldEdit)   
#        self.APRSUserButton.clicked.connect(self.floggerAPRSUserEdit)   
#        self.AirfieldDetailsButton.clicked.connect(self.floggerAirfieldDetailsEdit)   
#        self.MinFlightTimeButton.clicked.connect(self.floggerMinFlightTimeEdit)  
        self.FleetCheckRadioButton.toggled.connect(self.floggerFleetCheckRadioButton) 
        self.RecordTracksRadioButton.toggled.connect(self.floggerRecordTracksRadioButton)
#        self.DBSchemaButton.clicked.connect(self.floggerDBSchemaEdit)  
#        self.SMTPServerURLButton.clicked.connect(self.floggerSMTPServerURLEdit) 
#        self.SMTPServerPortButton.clicked.connect(self.floggerSMTPServerPortEdit)
#        self.APRSBase1Button.clicked.connect(self.floggerAPRSBaseEdit)
        self.UpdateButton.clicked.connect(self.floggerUpdateConfig)
        self.CancelButton.clicked.connect(self.floggerCancelConfigUpdate)

        self.RunningLabel.setStyleSheet("color: red") 
        
        
        # Initialise values from config file

#        filepath = os.path.join(path, "flogger_settings.py")
        filepath = os.path.join(path, "flogger_settings_file.txt")

#        filename = open(filepath)
        try:
            self.config = ConfigObj("flogger_settings_file.txt", raise_errors = True)
            print "Opened"
        except:
            print "Open failed"
            print self.config
            
#
# This section reads all the values from the config file and outputs these in the gui fields.
# It also initialises the corresponding settings object config fields. If the values are changed
# in the gui they must be saved in the config file and used as the current values in the settings object
#          
        old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_NAME")
        settings.FLOGGER_AIRFIELD_NAME = old_val
#        print settings.FLOGGER_AIRFIELD_NAME
        self.AirfieldBase.setText(old_val)
         
        old_val = self.getOldValue(self.config, "APRS_USER")
        settings.APRS_USER = old_val
        self.APRSUser.setText(old_val)
        
        old_val = self.getOldValue(self.config, "APRS_PASSCODE")    # This might get parsed as an int - need to watch it!
        settings.APRS_PASSCODE = old_val
        self.APRSPasscode.setText(old_val)
        
        old_val = self.getOldValue(self.config, "APRS_SERVER_HOST")    
        settings.APRS_SERVER_HOST = old_val
        self.APRSServerHostName.setText(old_val)
        
        old_val = self.getOldValue(self.config, "APRS_SERVER_PORT")    # This might get parsed as an int - need to watch it!
        settings.APRS_SERVER_PORT = int(old_val)
        self.APRSServerPort.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_RAD")    # This might get parsed as an int - need to watch it!
        settings.FLOGGER_RAD = int(old_val)
        self.AirfieldFlarmRadius.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_DETAILS")    
        settings.FLOGGER_AIRFIELD_DETAILS = old_val
        self.AirfieldDetails.setText(old_val)
          
        old_val = self.getOldValue(self.config, "FLOGGER_QFE_MIN")    
        settings.FLOGGER_QFE_MIN = old_val
        self.MinFlightQFE.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_MIN_FLIGHT_TIME")    
        settings.FLOGGER_MIN_FLIGHT_TIME = old_val
        self.MinFlightTime.setText(old_val)
        
        
        old_val = self.getOldValue(self.config, "FLOGGER_V_TAKEOFF_MIN")    
        settings.FLOGGER_V_TAKEOFF_MIN = old_val
        self.MinFlightTakeoffVelocity.setText(old_val)
            
        old_val = self.getOldValue(self.config, "FLOGGER_V_LANDING_MIN")    
        settings.FLOGGER_V_LANDING_MIN = old_val
        self.MinFlightLandingVelocity.setText(old_val) 
                   
        old_val = self.getOldValue(self.config, "FLOGGER_DT_TUG_LAUNCH")    
        settings.FLOGGER_DT_TUG_LAUNCH = old_val
        self.MinTugLaunchTIme.setText(old_val)
#
# Note this could be done using LatLon
#        
        old_val_lat = self.getOldValue(self.config, "FLOGGER_LATITUDE")    # This might get parsed as a real - need to watch it!
        print "Old_val: " + old_val_lat
        settings.FLOGGER_LATITUDE = old_val_lat
        
        old_val_lon = self.getOldValue(self.config, "FLOGGER_LONGITUDE")    # This might get parsed as a real - need to watch it!
        print "Old_lon: " + old_val_lon
        settings.FLOGGER_LONGITUDE = old_val_lon
#        self.AirfieldLongitude.setText(old_val_lon)
        
        old_latlon = LatLon(Latitude( old_val_lat), Longitude(old_val_lon))
        old_latlonstr = old_latlon.to_string('D% %H')
        self.AirfieldLatitude.setText(old_latlonstr[0])
        self.AirfieldLongitude.setText(old_latlonstr[1])
               
        old_val = self.getOldValue(self.config, "FLOGGER_FLEET_CHECK")
        print "Fleet Check: " + old_val 
        if old_val == "Y":
            print "Y"
            self.FleetCheckRadioButton.setChecked(True)
        else:
            print "N"   
        settings.FLOGGER_FLEET_CHECK = old_val
        
        old_val = self.getOldValue(self.config, "FLOGGER_TRACKS")
        print "Record Tracks: " + old_val 
        if old_val == "Y":
            print "Y"
            self.RecordTracksRadioButton.setChecked(True)
        else:
            print "N"   
        settings.FLOGGER_TRACKS = old_val 
        
        old_val = self.getOldValue(self.config, "FLOGGER_DB_SCHEMA")    
        settings.FLOGGER_DB_SCHEMA = old_val
        self.DBSchemaFile.setText(old_val)
        settings.FLOGGER_DB_SCHEMA = old_val
        
        
        old_val = self.getOldValue(self.config, "FLOGGER_DB_NAME")    
        settings.FLOGGER_DB_NAME = old_val
        self.DBName.setText(old_val)
        settings.FLOGGER_DB_NAME = old_val    
        
        old_val = self.getOldValue(self.config, "FLOGGER_FLARMNET_DB_URL")    
        settings.FLOGGER_FLARMNET_DB_URL = old_val
        self.FlarmnetURL.setText(old_val)
#        settings.FLOGGER_FLARMNET_DB_URL = old_val
       
        old_val = self.getOldValue(self.config, "FLOGGER_OGN_DB_URL")    
        settings.FLOGGER_OGN_DB_URL = old_val
        self.OGNURL.setText(old_val)
 #       settings.FLOGGER_OGN_DB_URL = old_val
                
        old_val = self.getOldValue(self.config, "FLOGGER_KEEPALIVE_TIME")    
        settings.FLOGGER_KEEPALIVE_TIME = int(old_val)
        self.APRSKeepAliveTIme.setText(old_val)

        old_val = self.getOldValue(self.config, "FLOGGER_SMTP_SERVER_URL")  
        print "Initialise FLOGGER_SMTP_SERVER_URL"  
        settings.FLOGGER_SMTP_SERVER_URL = old_val
        self.SMTPServerURL.setText(old_val)
        settings.FLOGGER_SMTP_SERVER_URL = old_val
        print "settings.FLOGGER_SMTP_SERVER_URL: ", settings.FLOGGER_SMTP_SERVER_URL
        
        old_val = self.getOldValue(self.config, "FLOGGER_SMTP_SERVER_PORT")    
        settings.FLOGGER_SMTP_SERVER_PORT = int(old_val)
        self.SMTPServerPort.setText(old_val)
        settings.FLOGGER_SMTP_SERVER_PORT = int(old_val)
        
                
        old_val = self.getOldValue(self.config, "FLOGGER_SMTP_TX") 
        print "TX from file: ", old_val   
        settings.FLOGGER_SMTP_TX = old_val
        self.EmailSenderTX.setText(old_val)
        settings.FLOGGER_SMTP_TX = old_val     
                
        old_val = self.getOldValue(self.config, "FLOGGER_SMTP_RX")    
        settings.FLOGGER_SMTP_RX = old_val
        self.EmailReceiverRX.setText(old_val)
        settings.FLOGGER_SMTP_RX = old_val
                
        old_val = self.getOldValue(self.config, "FLOGGER_APRS_BASES")
        i = 1
        for item in old_val:
            print "APRS Base: " + item
            if i == 1:
                self.APRSBase1Edit.setText(item)
                i += 1
                continue
            if i == 2:
                self.APRSBase2Edit.setText(item)
                i += 1
                continue
            if i == 3:
                self.APRSBase3Edit.setText(item)
                i += 1
                continue
            if i == 4:
                self.APRSBase4Edit.setText(item)
                i += 1
                continue 
            if i == 5:
                self.APRSBase5Edit.setText(item)
                i += 1
                continue 
        settings.FLOGGER_APRS_BASES = old_val
        print "APRS_BASES: ", old_val
        print "APRS_BASES: ", settings.FLOGGER_APRS_BASES
        
        old_val = self.getOldValue(self.config, "FLOGGER_FLEET_LIST") 
#        print "FLOGGER_FLEET_LIST: ", old_val 
        for key in old_val.keys():
            old_val[key] = int(old_val[key])
#            print "Key: ", key, " = ", int(old_val[key])
        settings.FLOGGER_FLEET_LIST = old_val
#        for key in settings.FLOGGER_FLEET_LIST.keys():
#            settings.FLOGGER_FLEET_LIST[key] = int(settings.FLOGGER_FLEET_LIST[key])
        print "FLOGGER_FLEET_LIST: ", settings.FLOGGER_FLEET_LIST
            
#
# GUI Initialisation end
#  

#
# Actions Start. Menu Bar
#      
    def floggerStart(self):
        print "flogger start"
        settings.FLOGGER_RUN = True
        flogger = flogger3()
#        flogger.flogger_start(settings)
#        print "settings.FLOGGER_SMTP_SERVER_URL: ", settings.FLOGGER_SMTP_SERVER_URL
#        print "settings.FLOGGER_SMTP_SERVER_PORT: ", settings.FLOGGER_SMTP_SERVER_PORT
#        print "settings.FLOGGER_DB_SCHEMA: ", settings.FLOGGER_DB_SCHEMA
        self.RunningLabel.setStyleSheet("color: green")
        self.RunningLabel.setText("Running...")
#        self.RunningProgressBar.maximum(0)
        self.RunningProgressBar.setProperty("maximum", 0) 
        flogger.flogger_run(settings)
        
        
    def floggerStop(self):
        settings.FLOGGER_RUN = False
        self.RunningLabel.setStyleSheet("color: red")
        self.RunningLabel.setText("Stopped")
        self.RunningProgressBar.setProperty("maximum", 1)
        print "flogger stop"
    
    def floggerQuit(self):
        print "flogger quit"
        
#
# Actions Start, update fields
#

    def floggerUpdateConfig(self):
        print "floggerUpdateConfig called"
        self.floggerAirfieldEdit2(True)
        self.floggerAPRSUserEdit2(True)
        self.floggerAPRSPasscodeEdit2(True)
        self.floggerAPRSServerhostEdit2(True)
        self.floggerAPRSServerportEdit2(True)
        self.floggerFlarmRadiusEdit2(True)
        self.floggerAirfieldDetailsEdit2(True)
        self.floggerAirfieldLatLonEdit2(True)
        self.floggerMinFlightTimeEdit2(True)
        self.floggerMinTakeoffVelocityEdit2(True)
        self.floggerMinLandingVelocityEdit2(True)
        self.floggerMinFlightQFEEdit2(True)
        self.floggerTugLaunchEdit2(True)
        self.floggerKeepAliveTime2(True)
        self.floggerDBSchemaFileEdit2(True)
        self.floggerDBNameEdit2(True)
        self.floggerFlarmnetURL2(True)
        self.floggerOGNURL2(True)
        self.floggerSMTPServerURLEdit2(True)
        self.floggerSMTPServerPortEdit2(True)
        self.floggerEmailSenderEdit2(True)
        self.floggerEmailReceiverEdit2(True)
        self.floggerAPRSBaseEdit2(True)
        return


    
    def floggerCancelConfigUpdate(self):
        print "floggerCancelConfigUpdate called"
        self.floggerAirfieldEdit2(False)
        self.floggerAPRSUserEdit2(False)
        self.floggerAPRSPasscodeEdit2(False)
        self.floggerAPRSServerhostEdit2(False)
        self.floggerAPRSServerportEdit2(False)
        self.floggerFlarmRadiusEdit2(False)
        self.floggerAirfieldDetailsEdit2(False)
        self.floggerAirfieldLatLonEdit2(False)
        self.floggerMinFlightTimeEdit2(False)
        self.floggerMinTakeoffVelocityEdit2(False)
        self.floggerMinLandingVelocityEdit2(False)
        self.floggerMinFlightQFEEdit2(False)
        self.floggerTugLaunchEdit2(False)
        self.floggerKeepAliveTime2(False)
        self.floggerDBSchemaFileEdit2(False)
        self.floggerDBNameEdit2(False)
        self.floggerFlarmnetURL2(False)
        self.floggerOGNURL2(False)
        self.floggerSMTPServerURLEdit2(False)
        self.floggerSMTPServerPortEdit2(False)
        self.floggerEmailSenderEdit2(False)
        self.floggerEmailReceiverEdit2(False)
        self.floggerAPRSBaseEdit2(False)
        return
                       
        
    def floggerAirfieldEdit2(self, mode):
        # Mode: True - update all fields, valraible to latest valuese
        #       False - restore all fields and variables to values from config (settings.txt) file
        print "Base Airfield button clicked ", "Mode: ", mode 
        if mode:
            # Values have been put into gui field from setting.txt and may then have been changed interactively
            airfield_base = self.AirfieldBase.toPlainText()  
        else:
            # Restore old values from settings.txt
            old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_NAME")
#            settings.FLOGGER_AIRFIELD_NAME = old_val
            print settings.FLOGGER_AIRFIELD_NAME
            self.AirfieldBase.setText(old_val)
            print "Airfield Base: " + old_val
            airfield_base = old_val
        # Put current value into settings.txt file for future use
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_AIRFIELD_NAME", airfield_base)
        # Now update python variable to current value in gui and settings.txt
        self.FLOGGER_AIRFIELD_NAME = airfield_base

        
    def floggerAPRSUserEdit2(self, mode):
        print "APRS User button clicked"
        if mode: 
            APRSUser = self.APRSUser.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "APRS_USER")
            self.APRSUser.setText(old_val)
            APRSUser = old_val
#       print "Airfield B: " + airfield_base
        self.editConfigField("flogger_settings_file.txt", "APRS_USER", APRSUser)
        self.APRS_USER = APRSUser
        

    def floggerAPRSPasscodeEdit2(self, mode):
            print "APRS Passcode button clicked"
            if mode: 
                APRSPasscode = self.APRSPasscode.toPlainText()  
            else:
                old_val = self.getOldValue(self.config, "APRS_PASSCODE")
                self.APRSPasscode.setText(old_val)
                APRSPasscode = old_val
            self.editConfigField("flogger_settings_file.txt", "APRS_PASSCODE", APRSPasscode)
            self.APRS_PASSCODE = APRSPasscode
            
    
    def floggerAPRSServerhostEdit2(self, mode):
            print "APRS Server Host button clicked"
            if mode: 
                APRSServerhost = self.APRSServerHostName.toPlainText()  
            else:
                old_val = self.getOldValue(self.config, "APRS_SERVER_HOST")
                self.APRSServerHostName.setText(old_val)
                APRSServerhost = old_val
            self.editConfigField("flogger_settings_file.txt", "APRS_SERVER_HOST", APRSServerhost)
            self.APRS_SERVER_HOST = APRSServerhost
            
    
    def floggerAPRSServerportEdit2(self, mode):
            print "APRS Server Port button clicked"
            if mode: 
                APRSServerport = self.APRSServerPort.toPlainText()  
            else:
                old_val = self.getOldValue(self.config, "APRS_SERVER_PORT")
                self.APRSServerPort.setText(old_val)
                APRSServerport = old_val
            self.editConfigField("flogger_settings_file.txt", "APRS_SERVER_PORT", APRSServerport)
            self.APRS_SERVER_PORT = int(APRSServerport)
            
    
    def floggerFlarmRadiusEdit2(self, mode):
            print "Flarm Radius button clicked"
            if mode: 
                FlarmRadius = self.AirfieldFlarmRadius.toPlainText()  
            else:
                old_val = self.getOldValue(self.config, "FLOGGER_RAD")
                self.AirfieldFlarmRadius.setText(old_val)
                FlarmRadius = old_val
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_RAD", FlarmRadius)
            self.FLOGGER_RAD = int(FlarmRadius)
        
            
    def floggerAirfieldDetailsEdit2(self, mode):
        print "Airfield Details button clicked"
        if mode:
            airfield_details = self.AirfieldDetails.toPlainText()
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_DETAILS")
            self.AirfieldDetails.setText(old_val)
            airfield_details = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_AIRFIELD_DETAILS", airfield_details)

    def floggerAirfieldLatLonEdit2(self, mode):
        print "Airfield latitude, longitude called"
        if mode:
            airfieldLat = self.AirfieldLatitude.toPlainText()
            airfieldLon = self.AirfieldLongitude.toPlainText()
            airfieldlatlon = string2latlon(str(airfieldLat), str(airfieldLon), 'D% %H')
            print "Airfield lat/lon: ", airfieldlatlon
            airfieldLatLonStr = airfieldlatlon.to_string("%D")
            print "Update Lat/Lon: ", airfieldLatLonStr
            print "Latlonstr: ", airfieldLatLonStr[0], " :", airfieldLatLonStr[1]
            old_val_lat = airfieldLatLonStr[0]
            old_val_lon = airfieldLatLonStr[1]
        else:
            old_val_lat = self.getOldValue(self.config, "FLOGGER_LATITUDE")
            old_val_lon = self.getOldValue(self.config, "FLOGGER_LONGITUDE")
            print "Old Lat: ", old_val_lat, " Old Lon: ", old_val_lon
            airfieldlatlon = LatLon(Latitude(old_val_lat), Longitude(old_val_lon))
            print "airfieldlatlon: ", airfieldlatlon
            airfieldLatLonStr = airfieldlatlon.to_string('D% %H')
            print "airfieldlatlonStr: ", airfieldLatLonStr
            self.AirfieldLatitude.setText(airfieldLatLonStr[0])
            self.AirfieldLongitude.setText(airfieldLatLonStr[1])
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_LATITUDE", old_val_lat)
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_LONGITUDE", old_val_lon)
        return
                  
    def floggerMinFlightTimeEdit2(self, mode):
        print "Min Flight Time button clicked"
        # Note. Format is "HH:MM:SS" ie a string
        if mode:
            min_flight_time = self.MinFlightTime.toPlainText() 
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_MIN_FLIGHT_TIME")
            self.MinFlightTime.setText(old_val)
            min_flight_time = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_MIN_FLIGHT_TIME", min_flight_time) 
        
                  
    def floggerMinTakeoffVelocityEdit2(self, mode):
        print "Min Takeoff Velocity button clicked"
        # Note. Format is "HH:MM:SS" ie a string
        if mode:
            min_takeoff_velocity = self.MinFlightTakeoffVelocity.toPlainText() 
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_V_TAKEOFF_MIN")
            self.MinFlightTakeoffVelocity.setText(old_val)
            min_takeoff_velocity = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_V_TAKEOFF_MIN", min_takeoff_velocity) 
        
                  
    def floggerMinLandingVelocityEdit2(self, mode):
        print "Min Landing Velocity button clicked"
        # Note. Format is "HH:MM:SS" ie a string
        if mode:
            min_landing_velocity = self.MinFlightLandingVelocity.toPlainText() 
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_V_LANDING_MIN")
            self.MinFlightLandingVelocity.setText(old_val)
            min_landing_velocity = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_V_LANDING_MIN", min_landing_velocity) 
        
                  
    def floggerMinFlightQFEEdit2(self, mode):
        print "Min QFE button clicked"
        # Note. Format is "HH:MM:SS" ie a string
        if mode:
            min_QFE = self.MinFlightQFE.toPlainText() 
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_QFE_MIN")
            self.MinFlightQFE.setText(old_val)
            min_QFE = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_QFE_MIN", min_QFE) 
                  
    def floggerTugLaunchEdit2(self, mode):
        print "Delta Tug Time button clicked"
        # Note. Format is "HH:MM:SS" ie a string
        if mode:
            min_tug_time = self.MinTugLaunchTIme.toPlainText() 
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_DT_TUG_LAUNCH")
            self.MinTugLaunchTIme.setText(old_val)
            min_tug_time = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_DT_TUG_LAUNCH", min_tug_time) 
        
    
    def floggerFleetCheckRadioButton(self):
        print "Fleet Check Radio Button clicked" 
        if self.FleetCheckRadioButton.isChecked():
            print "Fleet check checked"
            self.FLOGGER_FLEET_CHECK = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_FLEET_CHECK", "Y")
        else:
            print "Fleet check unchecked"
            selfFLOGGER_FLEET_CHECK = "N"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_FLEET_CHECK", "N")
            
    def floggerRecordTracksRadioButton(self):
        print "Record Tracks Radio Button clicked" 
        if self.RecordTracksRadioButton.isChecked():
            print "Record Tracks checked"
            self.FLOGGER_TRACKS = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_TRACKS", "Y")
        else:
            print "Record Tracks unchecked"
            self.FLOGGER_TRACKS = "N"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_TRACKS", "N")       
            
    def floggerKeepAliveTime2(self, mode):
        print "Keep Alive Time button clicked" 
        if mode:
            keep_alive_time = self.APRSKeepAliveTIme.toPlainText() 
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_KEEPALIVE_TIME") 
            self.APRSKeepAliveTIme.setText(old_val)
            keep_alive_time = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_KEEPALIVE_TIME", keep_alive_time)
        self.FLOGGER_KEEPALIVE_TIME = keep_alive_time 
            
    def floggerDBSchemaFileEdit2(self, mode):
        print "DB Schema File button clicked"
        if mode: 
            db_schema_file = self.DBSchemaFile.toPlainText() 
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_DB_SCHEMA")
            self.DBSchemaFile.setText(old_val)
            db_schema_file = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_DB_SCHEMA", db_schema_file) 
        self.FLOGGER_DB_SCHEMA = db_schema_file   
                 
    def floggerDBNameEdit2(self, mode):
        print "DB Schema File button clicked"
        if mode: 
            db_name = self.DBName.toPlainText() 
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_DB_NAME")
            self.DBName.setText(old_val)
            db_name = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_DB_NAME", db_name) 
        self.FLOGGER_DB_NAME = db_name
                       
    def floggerFlarmnetURL2(self, mode):
        print "Flarmnet URL button clicked"
        if mode: 
            Flarmnet_URL = self.FlarmnetURL.toPlainText() 
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_FLARMNET_DB_URL")
            self.FlarmnetURL.setText(old_val)
            Flarmnet_URL = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_FLARMNET_DB_URL", Flarmnet_URL) 
        self.FLOGGER_FLARMNET_DB_URL = Flarmnet_URL
        
                       
    def floggerOGNURL2(self, mode):
        print "OGN URL button clicked"
        if mode: 
            OGNURL = self.OGNURL.toPlainText() 
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_OGN_DB_URL")
            self.OGNURL.setText(old_val)
            OGNURL = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_OGN_DB_URL", OGNURL) 
        self.FLOGGER_OGN_DB_URL = OGNURL
                
    def floggerSMTPServerURLEdit(self):
        print "SMTP Server URL button clicked" 
        smtp_server_URL = self.SMTPServerURL.toPlainText()  
        print "SMTP Server URL: " + smtp_server_URL
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_SMTP_SERVER_URL", smtp_server_URL)
        smtp_server_URL = self.config["FLOGGER_SMTP_SERVER_URL"]
        self.FLOGGER_SMTP_SERVER_URL = smtp_server_URL   
                      
    def floggerSMTPServerURLEdit2(self, mode):
        print "SMTP Server URL button clicked"
        if mode: 
            smtp_server_URL = self.SMTPServerURL.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_SMTP_SERVER_URL")
            self.SMTPServerURL.setText(old_val)
            smtp_server_URL = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_SMTP_SERVER_URL", smtp_server_URL)
        self.FLOGGER_SMTP_SERVER_URL = smtp_server_URL       
                      
    def floggerEmailSenderEdit2(self, mode):
        print "SMTP Sender Tx button clicked"
        if mode: 
            EmailSenderTX = self.EmailSenderTX.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_SMTP_TX")
            self.EmailSenderTX.setText(old_val)
            EmailSenderTX = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_SMTP_TX", EmailSenderTX)
        self.FLOGGER_SMTP_TX = EmailSenderTX        
                      
    def floggerEmailReceiverEdit2(self, mode):
        print "SMTP Receiver Rx button clicked"
        if mode: 
            EmailReceiverRX = self.EmailReceiverRX.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_SMTP_RX")
            self.EmailReceiverRX.setText(old_val)
            EmailReceiverRX = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_SMTP_RX", EmailReceiverRX)
        self.FLOGGER_SMTP_RX = EmailReceiverRX 
                             
    def floggerSMTPServerPortEdit2(self, mode):
        print "SMTP Server Port button clicked"
        if mode :
            smtp_server_port = self.SMTPServerPort.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_SMTP_SERVER_PORT")
            self.SMTPServerPort.setText(old_val)
            smtp_server_port = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_SMTP_SERVER_PORT", smtp_server_port)
        self.FLOGGER_SMTP_SERVER_PORT = int(smtp_server_port)      
    
    def floggerAPRSBasesListEdit(self):
        print "APRS Bases list clicked"
#        sel_items = listWidget.selectedItems()
        sel_items = self.APRSBasesListWidget.selectedItems()
        for item in sel_items:
            new_val = item.text()
            print new_val
            item.editItem()
#            item.setText(item.text()+"More Text")
     
    def floggerAPRSBaseEdit2(self, mode):  
        print "APRS Base station list called" 
        if mode:
            APRSBaseList = []
            APRSBaseList.append(self.APRSBase1Edit.toPlainText())
            APRSBaseList.append(self.APRSBase2Edit.toPlainText())
            APRSBaseList.append(self.APRSBase3Edit.toPlainText())
            APRSBaseList.append(self.APRSBase4Edit.toPlainText())
            APRSBaseList.append(self.APRSBase5Edit.toPlainText())
            print "APRSBaseList: ", APRSBaseList
#            APRSBaseList[1] = self.APRSBase2Edit.toPlainText() 
#            APRSBaseList[2] = self.APRSBase3Edit.toPlainText() 
#            APRSBaseList[3] = self.APRSBase4Edit.toPlainText()
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_APRS_BASES")
            self.APRSBase1Edit.setText(old_val[0])
            self.APRSBase2Edit.setText(old_val[1])
            self.APRSBase3Edit.setText(old_val[2])
            self.APRSBase4Edit.setText(old_val[3])
            self.APRSBase5Edit.setText(old_val[4])
            APRSBaseList = old_val
        APRSBaseList = [str(APRSBaseList[0]), str(APRSBaseList[1]), str(APRSBaseList[2]), str(APRSBaseList[3]), str(APRSBaseList[4])]
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_APRS_BASES", APRSBaseList)
        self.FLOGGER_APRS_BASES = APRSBaseList 
        print "FLOGGER_APRS_BASES: ", self.FLOGGER_APRS_BASES
          
    def editConfigField (self, file_name, field_name, new_value):
        print "editConfig called"
        self.config[field_name] = new_value
        self.config.write()

            
    def setOldValue(self, config_field_name): 
#        val = self.config[config_field_name]
        val = settings.config[config_field_name]
        setattr(self, config_field_name, val) #equivalent to: self.varname= 'something'
#        settings.config_field_name = val
        return self.config[config_field_name]
    
    def getOldValue(self, config, config_field_name): 
        val = config[config_field_name]
        setattr(self, config_field_name, val)
        return config[config_field_name]
#
# Actions End
#            
               
            
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())


    