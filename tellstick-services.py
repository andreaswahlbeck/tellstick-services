from flask import Flask
import simplejson 
import json
import optparse
from pytelldus import td


TSS_NAME="tellstick-services"
app = Flask(__name__)
td.init(defaultMethods = td.TELLSTICK_TURNON | td.TELLSTICK_TURNOFF)



@app.route("/", methods=['GET'])
def start():
	"""Just the index request"""
	return json.dumps({'status_url':'/status'})


@app.route("/status", methods=['GET'])
def status():
	"""On status request return the list of all devices and their status"""

	result = []
	number_of_devices = td.getNumberOfDevices()

	if (number_of_devices >= 0):
		for i in range(number_of_devices):
			device_id = td.getDeviceId(i)
			result.append(get_status_for_device(device_id))

		return json.dumps(result)
	else:
		# failed, return 503
		return make_response(503)


@app.route("/device/<int:device_id>", methods=['GET'])
def device_status(device_id):
	"""Get device status for device_id"""
	return json.dumps(get_status_for_device(device_id))


@app.route("/device/<int:device_id>/<command>", methods=['POST'])
def controll_device(device_id, command):
	"""Control device with device_id and command (on/off valid)"""
	supported_cmds = ['on', 'off']
	if (command in supported_cmds):
		if (command == 'on'):
			rc = td.turnOn(device_id)
		elif (command == 'off'):
			rc = td.turnOff(device_id)
		else:
			rc = -1

		if (rc == 0):
			return json.dumps(get_status_for_device(device_id))
		else:
			return json.dumps({'error':'failed to execute command'})
	
	else:
		return json.dumps({'error':'invalid command'})
	

def get_status_for_device(device_id):
	name = td.getName(device_id)
	status = td.lastSentCommand(device_id, readable = True)
	return {'deviceId':device_id,'deviceName':name,'status':status}

def init_opts():
	usage = "Support the following arguments"
	
	parser = optparse.OptionParser(usage = usage)
	parser.add_option("-d", "--debug", 
						action="store_true", dest="debug", 
						default=False,help="Run in debug mode")
	return parser.parse_args()


def handle_opts():
	(options, args) =init_opts()
	if options.debug:
		print "starting in debug mode"
		app.debug = True


if __name__ == "__main__":
	handle_opts()
	app.run()
