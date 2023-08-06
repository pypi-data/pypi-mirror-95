# Alfons Command Line Interface

This is a tool to publish and subscribing to MQTT packets to [Alfons](https://github.com/ntoonio/Alfons).

	$ alfonscli
		-p, --profile    Profile to load default arguments from
		-s, --server     Host:port
		-u, --user       Username
		-pw,--password   Password
		-t, --topic      Topic to subscribe/publish to
		-m, --message    Message to publish. Only subscribing if not set
		-c, --continuous Don't quit after receiving the first packet
