import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


def get_console_logger_from_config(config: dict) -> logging.StreamHandler:
	console_handler = logging.StreamHandler()
	console_handler.setLevel(config.get("level").upper())
	console_handler.setFormatter(logging.Formatter(config.get("format"), config.get("datefmt")))
	return console_handler


def get_rotating_file_logger_from_config(config: dict, logpath: str) -> TimedRotatingFileHandler:
	file_handler = TimedRotatingFileHandler(
		filename=logpath,
		when=config.get("when"),
		interval=config.get("interval"),
		backupCount=config.get("backupCount")
	)
	file_handler.setLevel(config.get("level").upper())
	file_handler.setFormatter(logging.Formatter(config.get("format"), config.get("datefmt")))
	file_handler.namer = lambda name: name.replace(".log", "") + ".log"
	return file_handler


def initialize_logger(logger, config):
	# Check that the app_log_path exists. If not then create
	if not os.path.exists(Path(config.get("app_log_path"))):
		os.mkdir(config.get("app_log_path"))

	# Create App logger
	app_logpath = f'{config.get("app_log_path")}/{config.get("app_log_filename")}'
	rotating_file_log_handler = get_rotating_file_logger_from_config(
		config=config.get("loggers").get("rotating_file"),
		logpath=app_logpath
	)

	# Create console logger
	console_log_handler = get_console_logger_from_config(config.get("loggers").get("console"))
	logger.addHandler(console_log_handler)

	# Create rotating file logger
	logger.addHandler(rotating_file_log_handler)
