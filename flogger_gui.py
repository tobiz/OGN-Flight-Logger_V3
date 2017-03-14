import sys
import os
import string
from PyQt4 import QtGui, QtCore, uic
from PyQt4.Qt import SIGNAL
import subprocess
#import flogger_settings
import flogger_settings
from parse import *
from ConfigParser import *
from configobj import ConfigObj
from flogger3 import *
from flogger_settings import * 


# 20170311 

# get the directory of this script
path = os.path.dirname(os.path.abspath(__file__))
print("Path: " + path) 
#settings = class_settings()

Ui_MainWindow, base_class = uic.loadUiType(os.path.join(path,"flogger.ui"))

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
        self.SMTPServerPortButton.clicked.connect(self.floggerSMTPServerPortEdit)
        self.APRSBase1Button.clicked.connect(self.floggerAPRSBaseEdit)
        self.UpdateButton.clicked.connect(self.floggerUpdateConfig)
        self.CancelButton.clicked.connect(self.floggerCancelConfigUpdate)

        self.RunningLabel.setStyleSheet("color: red") 
        
        
        # Initialise values from config file

#        filepath = os.path.join(path, "flogger_settings.py")
        filepath = os.path.join(path, "flogger_settings_file.txt")

#        filename = open(filepath)
        try:
#            config = ConfigObj(filename, encoding='UTF8', raise_errors = True)
#            self.config = ConfigObj("flogger_settings.py", raise_errors = True)
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
        
        old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_DETAILS")    
        settings.FLOGGER_AIRFIELD_DETAILS = old_val
        self.AirfieldDetails.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_MIN_FLIGHT_TIME")    
        settings.FLOGGER_MIN_FLIGHT_TIME = old_val
        self.MinFlightTime.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_LATITUDE")    # This might get parsed as an real - need to watch it!
        print "Old_val: " + old_val
        settings.FLOGGER_LATITUDE = old_val
        self.AirfieldLatitude.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_LONGITUDE")    # This might get parsed as an real - need to watch it!
        settings.FLOGGER_LONGITUDE = old_val
        self.AirfieldLongitude.setText(old_val)
        
        if settings.FLOGGER_LATITUDE < 0:
            latitude = str(settings.FLOGGER_LATITUDE)[1:] + " S"
        else:
            latitude = str(settings.FLOGGER_LATITUDE)[1:] + " N"
#        print "Latitude: " + latitude
        
        if settings.FLOGGER_LONGITUDE < 0:
            longitude = str(settings.FLOGGER_LONGITUDE)[1:] + " E"
        else:
            longitude = str(settings.FLOGGER_LONGITUDE)[1:] + " W"
#        print "Latitude: " + longitude
        self.AirfieldLatitude.setText(latitude)
        self.AirfieldLongitude.setText(longitude)
        
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
                
        old_val = self.getOldValue(self.config, "FLOGGER_APRS_BASES")
        i = 1
        for item in old_val:
            print "APRS Base: " + item
            if i == 1:
                self.APRSBase1Edit.setText(item)
                i = i + 1
                continue
            if i == 2:
                self.APRSBase2Edit.setText(item)
                i = i + 1
                continue
            if i == 3:
                self.APRSBase3Edit.setText(item)
                i = i + 1
                continue
            if i == 4:
                self.APRSBase4Edit.setText(item)
                i = i + 1  
                continue 
            if i == 5:
                self.APRSBase5Edit.setText(item)
                i = i + 1  
                continue 
        settings.FLOGGER_APRS_BASES = old_val
        print "APRS_BASES: ", old_val
        print "APRS_BASES: ", settings.FLOGGER_APRS_BASES
        
        
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
        flogger.flogger_run(settings)
        
        
    def floggerStop(self):
        settings.FLOGGER_RUN = False
        self.RunningLabel.setStyleSheet("color: red")
        self.RunningLabel.setText("Stopped")
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
        self.floggerAirfieldDetailsEdit2(True)
        self.floggerMinFlightTimeEdit2(True)
        self.floggerDBSchemaFileEdit2(True)
        self.floggerSMTPServerURLEdit2(True)
        self.floggerSMTPServerPortEdit()
        self.floggerAPRSBaseEdit()
        return
    
    def floggerCancelConfigUpdate(self):
        print "floggerCancelConfigUpdate called"
        self.floggerAirfieldEdit2(False)
        self.floggerAPRSUserEdit2(False)
        self.floggerAPRSPasscodeEdit2(False)
        self.floggerAPRSServerhostEdit2(False)
        self.floggerAPRSServerportEdit2(False)
        self.floggerAirfieldDetailsEdit2(False)
        self.floggerMinFlightTimeEdit2(False)
        self.floggerDBSchemaFileEdit2(False)
        self.floggerSMTPServerURLEdit2(False)
        return
                       
#    def floggerAirfieldEdit(self):
#        print "Base Airfield button clicked" 
#        # Values have been put into gui field from setting.txt and may then have been changed interactively
#        airfield_base = self.AirfieldBase.toPlainText()  
#        print "Airfield Base: " + airfield_base
#        # Put current value into settings.txt file for future use
#        self.editConfigField("flogger_settings_file.txt", "FLOGGER_AIRFIELD_NAME", airfield_base)
#        # Now update python variable to current value in gui and settings.txt
#        self.FLOGGER_AIRFIELD_NAME = airfield_base
        
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

#    def floggerAPRSUserEdit(self):
#        print "APRS User button clicked" 
#        APRSUser = self.APRSUser.toPlainText()  
#       print "Airfield B: " + airfield_base
#        self.editConfigField("settings.py", "APRS_USER", APRSUser)
#        APRSUser = self.config["APRS_USER"]
        
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
        
#    def floggerAirfieldDetailsEdit(self):
#        print "Airfield Details button clicked"
#        airfield_details = self.AirfieldDetails.toPlainText()
#        self.editConfigField("flogger_settings_file.txt", "FLOGGER_AIRFIELD_DETAILS", airfield_details)
#        airfield_details = self.config["FLOGGER_AIRFIELD_DETAILS"]
#        self.FLOGGER_AIRFIELD_DETAILS = airfield_details
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
        
            
    def floggerAirfieldDetailsEdit2(self, mode):
        print "Airfield Details button clicked"
        if mode:
            airfield_details = self.AirfieldDetails.toPlainText()
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_DETAILS")
            self.AirfieldDetails.setText(old_val)
            airfield_details = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_AIRFIELD_DETAILS", airfield_details)
#        airfield_details = self.config["FLOGGER_AIRFIELD_DETAILS"]
#        self.FLOGGER_AIRFIELD_DETAILS = airfield_details
        
        
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

            
    def floggerDBSchemaEdit(self):
        print "DB Schema File button clicked" 
        db_schema_file = self.DBSchemaFile.toPlainText()  
        print "DB Schema File: " + db_schema_file
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_DB_SCHEMA", db_schema_file)
        db_schema = self.config["FLOGGER_DB_SCHEMA"]
#        self.AirfieldBase.setText(settings.FLOGGER_AIRFIELD_NAME)
        self.FLOGGER_DB_SCHEMA = db_schema_file 
            
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
        
        
         
        smtp_server_URL = self.SMTPServerURL.toPlainText()  
        print "SMTP Server URL: " + smtp_server_URL
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_SMTP_SERVER_URL", smtp_server_URL)
        smtp_server_URL = self.config["FLOGGER_SMTP_SERVER_URL"]
        self.FLOGGER_SMTP_SERVER_URL = smtp_server_URL 
        
                       
    def floggerSMTPServerPortEdit(self):
        print "SMTP Server Port button clicked" 
        smtp_server_port = self.SMTPServerPort.toPlainText()  
        print "SMTP Server Port: " + smtp_server_port
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_SMTP_SERVER_PORT", smtp_server_port)
        smtp_server_port = self.config["FLOGGER_SMTP_SERVER_PORT"]
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
     
    def floggerAPRSBaseEdit(self):  
        print "APRS Base station list called" 
        APRSBase1 = self.APRSBase1Edit.toPlainText()
        APRSBase2 = self.APRSBase2Edit.toPlainText() 
        APRSBase3 = self.APRSBase3Edit.toPlainText() 
        APRSBase4 = self.APRSBase4Edit.toPlainText() 
        APRSBaseList = [str(APRSBase1), str(APRSBase2), str(APRSBase3), str(APRSBase4)]
        print "APRSBaseList: ", APRSBaseList
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_APRS_BASES", APRSBaseList)
#        APRSBase = self.config["FLOGGER_APRS_BASES"]
        self.FLOGGER_APRS_BASES = APRSBaseList 
        
    def floggerRunningMovie(self, frame_rate):
        print "RunningMovie called"
        print "Running.."
        self.RunningLabel.setStyleSheet("color: green")
        self.RunningLabel.setText("Running..")
        time.sleep(frame_rate)
        print "Running..."
        self.RunningLabel.setText("Running...")
        time.sleep(frame_rate)
        print "Running."
        self.RunningLabel.setText("Running.")
        time.sleep(frame_rate)
        return
        
          
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


    