#Tellstick Services#

##About##

This is a small REST interface for controling configured tellstick devices.

Uses a python wrapper for [libtelldus-core](http://developer.telldus.se/doxygen/index.html)
called [pytelldus](https://bitbucket.org/andreassvanberg/pytelldus).

At the moment only turning on and off is supported.

Info about configuring devices can be found [here](http://developer.telldus.com/wiki/TellStick_conf).


##Setup##

After cloning you need to init and update submodules.

You need to have Flask and simplejson installed.


##Running the service##

Run it by executing:
<pre>
python tellstick-services.py
</pre>

The following options are supported:

* -d, --debug  Run in debug mode
* -t, --test   Run in test mode, no interaction with telldusd
* -l, --local  Only run on localhost

##GUI##

There is a small web UI for controling the devices at:
http://<ipaddress>:5000

##REST-interface##

The REST-interface returns JSON.

Sample request using curl when running in test mode using a simulator:

**Get status of all devices:**
<pre>
curl http://localhost:5000/devices
</pre>
**Get status of device 1:**
<pre>
curl http://localhost:5000/devices/1
</pre>
**Turn on device 1:**
<pre>
curl -X POST http://localhost:5000/devices/1/on
</pre>
