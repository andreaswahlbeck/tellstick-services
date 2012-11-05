from flask import Flask
import simplejson 
import json
import optparse
from pytelldus import td


TSS_NAME="tellstick-services"
app = Flask(__name__)
td.init()


methods=['GET']
@app.route("/")
def start():
	"""Just the index request"""
	return json.dumps(status_url='/status')


methods=['GET']
@app.route("/status")
def status():
	"""On status request return the list of all devices and their status"""

	result = []
	number_of_devices = td.getNumberOfDevices()

	if (number_of_devices >= 0):
		for i in range(number_of_devices):
			device_id = td.getDeviceId(i)
			name = td.getName(device_id)
			status = td.lastSentCommand(device_id, readable = True)
			result.append({'deviceId':device_id,'deviceName':name,'status':status})

		return json.dumps(result)
	else:
		# failed, return 503
		return make_response(503)


methods=['GET']
@app.route("/status-update")
def update_status():
	"""On status update request reread state from telldusd and the return status"""
	return "will update status"


methods=['GET']
@app.route("/device/<int:device_id>")
def device_status(device_id):
	"""Get device status for device_id"""
	app.logger.debug('checking logger')
	return jsonify(device_id=device_id, status='on')


methods=['POST']
@app.route("/device/<int:device_id>/<command>")
def controll_device(device_id, command):
	"""Control device with device_id and command (on/off valid)"""
	return "updating device %s with command %s" % device_id, command


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
