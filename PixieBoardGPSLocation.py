import subprocess


class PixieBoardGPSLocation():		

	def __init__(self):

		self.PIXIE_BOARDS_PASSWORD = "pixiepro"
		self.COMMAND_OK_CALLBACK = "OK"
		self.ENABLE_AT_COMMAND = "echo 'ATE1' | socat - /dev/ttyUSB2,cr"
		self.SESSION_STATUS = "echo 'AT+QGPS?' | socat - /dev/ttyUSB2,cr | grep '+QGPS:'"
		self.STOP_SESSION = "echo 'AT+QGPSEND' | socat - /dev/ttyUSB2,cr"
		self.CONFIGURE_GPS_TRACKING = "echo 'AT+QGPS=1,30,50,0,1' | socat - /dev/ttyUSB2,cr"
		self.GET_GPS_LOCATION = "echo 'AT+QGPSLOC?' | socat - /dev/ttyUSB2,cr"
		self.GET_GPS_LOCATION_PRETTY = "echo 'AT+QGPSLOC=2' | socat - /dev/ttyUSB2,cr"

		self.ModemStatus = ""

		self.UTCTime = ""
		self.Latitude = ""
		self.Longitude = ""
		self.HorizontalPrecision = ""
		self.Altitude = ""
		self.Fix = ""
		self.Cog = ""
		self.SpeedOverGroundKmH = ""
		self.SpeedOverGroundKnots = ""
		self.Date = ""
		self.NumberOfSatellites = ""


	def EnableATCommands(self):
		(command_output, error) = self.SendShellCommand(self.ENABLE_AT_COMMAND)
		if self.ParseOKInMsg(command_output):
			return True, command_output, error
		else:
			return False, command_output, error

	def StopSession(self):
		sessionStatus, sessionOutput, sessionError = self.SessionStatus()
		if sessionStatus:
			(command_output, error) = self.SendShellCommand(self.STOP_SESSION)
			if self.ParseOKInMsg(command_output):
				return True, command_output, error
			else:
				return False, command_output, error
		else:
			return False, sessionOutput, sessionError

	def SessionStatus(self):
		(command_output, error) = self.SendShellCommand(self.SESSION_STATUS)
		if (str(command_output)[-4:-3]) == "1":
			return True, command_output, error
		else:
			return False, command_output, error


	def ConfigureGPSTracking(self):
		(command_output, error) = self.SendShellCommand(self.CONFIGURE_GPS_TRACKING)
		if self.ParseOKInMsg(command_output):
			return True, command_output, error
		else:
			return False, command_output, error

	def GetGPSLocation(self):
		(command_output, error) = self.SendShellCommand(self.GET_GPS_LOCATION)
		if self.ParseOKInMsg(command_output):
			self.ParseGPSLocation(command_output)
			return True, command_output, error
		else:
			return False, command_output, error

	def GetGPSLocationPretty(self):
		(command_output, error) = self.SendShellCommand(self.GET_GPS_LOCATION_PRETTY)
		if self.ParseOKInMsg(command_output):
			self.ParseGPSLocation(command_output)
			return True, command_output, error
		else:
			return False, command_output, error

	def SendShellCommand(self, shellCommand):
		command = subprocess.Popen([shellCommand], stdout=subprocess.PIPE, shell=True)
		(command_output, error) = command.communicate(self.PIXIE_BOARDS_PASSWORD)
		return command_output, error

	def ParseGPSLocation(self, command_output):
		locationData = str(command_output).split(",")
		self.UTCTime = locationData[0][30:]
		self.Latitude = locationData[1]
		self.Longitude = locationData[2]
		self.HorizontalPrecision = locationData[3]
		self.Altitude = locationData[4]
		self.Fix = locationData[5]
		self.Cog = locationData[6]
		self.SpeedOverGroundKmH = locationData[7]
		self.SpeedOverGroundKnots = locationData[8]
		self.Date = locationData[9]
		self.NumberOfSatellites = locationData[10][0:2]

	def ParseOKInMsg(self, command_output):
		output = str(command_output)
		if self.COMMAND_OK_CALLBACK in output:
			return True
		else:
			return False


