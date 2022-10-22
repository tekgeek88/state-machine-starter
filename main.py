from __future__ import annotations

from utils.log_utils import initialize_logger

import logging
import time
import toml
import sys
from state_driver import StateDriver

# Create a global logger instance
logger = logging.getLogger('state_driver')
logger.setLevel(logging.DEBUG)

# Static config file
CONFIG_FILE = './settings/config.toml'


# noinspection PyUnresolvedReferences
def main(config):
	logger.info(f"State driver starting")

	state = StateDriver(config=config)

	# Initial state starts out with running = True
	while state.running:
		# Optionally modify a state's handler to handle the type of data as needed
		state.handler(None)
		time.sleep(0.01)  # Approximately 100 ticks per second

	# Main has finished successfully
	return True


if __name__ == '__main__':
	# Get app config
	try:
		logger.info(f"Loading config file: {CONFIG_FILE}")
		app_config = toml.load(CONFIG_FILE)
	except TypeError:
		logger.error(f"Failed to load config from file {CONFIG_FILE} exiting")
		sys.exit(1)

	initialize_logger(logger, app_config)

	# noinspection PyBroadException
	try:
		if main(app_config):
			pass
		else:
			logger.info('Failed to finish successfully!')
		logger.info(f"Program completed")
	except KeyboardInterrupt:
		pass
	except Exception as e:
		logger.exception("Failed to finish successfully due to uncaught exception!")
