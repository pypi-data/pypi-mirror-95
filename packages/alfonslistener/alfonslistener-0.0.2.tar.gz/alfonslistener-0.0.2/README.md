# Alfons Listener
Simple program for listening on a topic and when it's received running a script.

## Setup
### config.yaml
	info:
	    server: "host:port"
	    username: "username"
	    password: "iot"
	    ssl: True

	commands:
	  - topic: "topic"
	    script: "script-to-run"
	  - topic: "topic2"
	    python: "module:function"
	    script: "script-to-run2"

### Creating a daemon

	$ ./service_install.sh

If you want to install the service under a name other than "alfonslistener" you can change the `name` variable on the top of the file.
