from __future__ import annotations

from abc import ABC, abstractmethod
from signal import signal, SIGINT

import logging

logger = logging.getLogger("state_driver")
logger.setLevel(logging.DEBUG)

should_terminate = False


# noinspection PyUnusedLocal
def signal_handler(signal_received, frame):
	"""
	Signal interceptor used to let states know they need to terminate
	:param signal_received:
	:param frame:
	:return:
	"""
	# Handle any cleanup here
	logger.info(f'SIGNAL {signal_received} or CTRL-C detected.')
	global should_terminate
	should_terminate = True


signal(SIGINT, signal_handler)


# noinspection PyAttributeOutsideInit
class IState(ABC):
	"""
	The State interface
	All states must implement a handler function
	"""

	@property
	def context(self) -> StateDriver:
		return self._context

	@context.setter
	def context(self, context: StateDriver) -> None:
		self._context = context

	@abstractmethod
	def handler(self, char) -> None:
		pass


class State1(IState):
	"""
	Simple state that runs for 500 ticks or 5 seconds before switching to State 2
	"""

	def __init__(self):
		self.tick_count = 0

	def handler(self, char) -> None:
		if should_terminate:
			self.context.set_state(Terminate())

		# Runs only on the states first tick
		if self.tick_count == 0:
			logger.debug(f"The context is in {type(self).__name__}")
		self.tick_count += 1

		# If this state has executed 500x switch to State 2
		if self.tick_count > 500:
			self.context.set_state(State2())


class State2(IState):
	"""
	Simple state that runs for 500 ticks or 5 seconds before switching to back to State 1
	"""

	def __init__(self):
		self.tick_count = 0

	def handler(self, char) -> None:
		if should_terminate:
			self.context.set_state(Terminate())

		# Runs only on the states first tick
		if self.tick_count == 0:
			logger.debug(f"The context is in {type(self).__name__}")
		self.tick_count += 1

		# If this state has executed 500x switch to State 1
		if self.tick_count > 500:
			self.context.set_state(State1())


# noinspection PyUnresolvedReferences
class Terminate(IState):

	def __init__(self):
		self.tick_count = 0

	# Runs only on the states first tick
	def handler(self, char) -> None:
		if self.tick_count == 0:
			logger.debug(f"The context is in {type(self).__name__}")
		self.tick_count += 1

		logger.info("Running state set to False")
		self.context.running = False


# noinspection PyUnresolvedReferences
class StateDriver:

	def __init__(self, config):
		self._state = None
		self._running = True
		self.config = config
		self.set_state(State1())

	def set_state(self, state):
		"""
		The state passed in is a reference to the current state that should have its handler function executed
		Each state gets a reference pointer back to its driver class so data can be shared between states.
		:param state:
		:return:
		"""
		logger.debug(f'Context: Transitioning to {type(state).__name__}')
		self._state = state
		self._state.context = self

	@property
	def running(self) -> bool:
		return self._running

	@running.setter
	def running(self, running: bool) -> None:
		self._running = running

	def handler(self, char):
		self._state.handler(char)
