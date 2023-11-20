#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"


########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2020.11.04                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE: Consider moving to multiprocessing::Process instead.                                                       #
#                                                                                                                      #
########################################################################################################################


from mpzinke import typename
import sys
from typing import Optional
import threading
import warnings


def warning_message(message, *_: list) -> str:
	"""
	SUMMARY: Used to override warning format & return only the warning message.
	"""
	return str(message)+"\n"


class BaseThread(threading.Thread):
	def __init__(self, name: str, *, action: callable, time: callable):
		threading.Thread.__init__(self, name=name, target=self)

		self.action: callable = action  # operations special to child object
		self._condition: threading.Condition = threading.Condition()  # allows for sleep/wake feature
		self._is_active: bool = False  # used by thread_loop() for maintaining while loop
		self.time: callable = time  # function pointer to determine/return the amount of time it should sleep

		self.decorate_call()

		warnings.formatwarning = warning_message


	def __init_subclass__(cls):
		if(not "__call__" in dir(cls)):
			raise Exception(f"Class {cls.__name__} requires a '__call__' method to be a child class of BaseThread")


	def __enter__(self):
		self._is_active = True


	def __exit__(self, exc_type, exc_val, exc_tb):
		self._is_active = False


	def __del__(self) -> None:
		if(self.is_alive()):
			self.kill()


	def decorate_call(self) -> None:
		__call__copy = type(self).__call__
		def __call__(self):
			with self:
				try:
					__call__copy(self)
				except Exception as error:
					print(error, file=sys.stderr)

		type(self).__call__ = __call__


	def kill(self) -> None:
		"""
		SUMMARY: Ends a thread.
		DETAILS: Releases loop, wakes sleeping condition, joins thread with rest of program.
		"""
		self._is_active = False
		with self._condition:
			self._condition.notify()


	def sleep(self, seconds: Optional[int]=None) -> None:
		"""
		SUMMARY: Sleeps thread loop for amount of time.
		PARAMS:  Takes a numeric amount of time defaulted to None.
		NOTES: Sleeps for default amount of time if specified, otherwise indefinitely.
		"""
		with self._condition:
			if(seconds is None):
				warnings.warn(f"Thread: {self.name} has been indefinitely put to sleep")

			self._condition.wait(seconds)


	def wake(self) -> None:
		"""
		SUMMARY: Wakes thread (condition from sleep).
		"""
		with self._condition:
			self._condition.notify()
