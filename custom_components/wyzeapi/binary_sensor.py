#!/usr/bin/python3

"""Platform for binary_sensor integration."""
import logging
from .wyzeapi.wyzeapi import WyzeApi
from . import DOMAIN

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
# Import the device class from the component that you want to support
from homeassistant.components.binary_sensor import (
	PLATFORM_SCHEMA,
	BinarySensorDevice,
	DEVICE_CLASS_MOTION,
	DEVICE_CLASS_DOOR
	)
	
_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, add_entities, discovery_info=None):
	"""Set up the Wyze binary_sensor platform."""
	_LOGGER.debug("""Creating new WyzeApi binary_sensor component""")

	# Add devices
	add_entities(WyzeSensor(sensor) for sensor in await hass.data[DOMAIN]["wyzeapi_account"].async_list_binary_sensors())

class WyzeSensor(BinarySensorDevice):
	"""Representation of a Wyze binary_sensor."""

	def __init__(self, sensor):
		"""Initialize a Wyze binary_sensor."""
		self._sensor = sensor
		self._name = sensor._friendly_name
		self._state = sensor._state
		self._avaliable = True

	@property
	def name(self):
		"""Return the display name of this sensor."""
		return self._name

	@property
	def available(self):
		"""Return the connection status of this sensor"""
		return self._avaliable

	@property
	def is_on(self):
		"""Return true if sensor is on."""
		return self._state

	async def async_update(self):
		"""Fetch new state data for this sensor.
		This is the only method that should fetch new data for Home Assistant.
		"""
		await self._sensor.async_update()
		self._state = self._sensor._state
