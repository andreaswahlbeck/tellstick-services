from flask import Flask,jsonify
import simplejson 
import json
import optparse


TSS_NAME="tellstick-services"
app = Flask(__name__)


methods=['GET']
@app.route("/")
def start():
	"""Just the index request"""
	return jsonify(status='running',status_url='/status')


methods=['GET']
@app.route("/status")
def status():
	"""On status request return the list of all devices and their status"""
	return "status"


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
