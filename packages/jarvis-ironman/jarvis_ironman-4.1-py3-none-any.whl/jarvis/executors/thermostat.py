import time
from threading import Thread
from typing import Union

from pyhtcc import AuthenticationError, PyHTCC, Zone

from jarvis.modules.audio import speaker
from jarvis.modules.logger import logger
from jarvis.modules.models import models
from jarvis.modules.utils import support, util


class Thermostat:
    """Controller object for device object and expiration time.

    >>> Thermostat

    """

    device: Union[Zone, None] = None
    expiration = time.time() + 86_400  # tested to last at least 24 hours


def create_connection() -> None:
    """Creates a new connection and stores the device object and expiration time in a dedicated object."""
    try:
        tcc_object: PyHTCC = PyHTCC(models.env.tcc_username, models.env.tcc_password)
    except AuthenticationError as error:
        logger.error(error)
        Thermostat.device = "LOGIN"
        return
    try:
        Thermostat.device = tcc_object.get_zone_by_name(models.env.tcc_device_name)
    except NameError as error:
        logger.error(error)
        Thermostat.device = "DEVICE"


# Initiate connection only for main and offline communicators
# WATCH OUT: for changes in function name
if models.settings.pname in ('JARVIS', 'telegram_api', 'jarvis_api'):
    if all((models.env.tcc_username, models.env.tcc_password, models.env.tcc_device_name)):
        logger.info("Creating a new thermostat connection for '%s'", models.settings.pname)
        Thread(target=create_connection).start()


def get_thermostat(phrase: str) -> None:
    """Get operations to be performed on the thermostat.

    Args:
        phrase: Takes the phrase spoken as an argument.
    """
    if "current" in phrase or "status" in phrase:
        mode = Thermostat.device.get_system_mode()
        fan = Thermostat.device.get_fan_mode()
        speaker.speak(text=f"Currently your thermostat is set to {mode.name.lower()}, and "
                           f"the fan is set to {fan.name.lower()}")
        return
    if "indoor" in phrase:
        if "humidity" in phrase:
            value = str(util.format_nos(Thermostat.device.get_indoor_humidity_raw())) + "%"
            logger.info("Humidity: %s", value)
            speaker.speak(text=f"The current indoor humidity is {value} {models.env.title}!")
            return
        if "temperature" in phrase:
            value = util.format_nos(Thermostat.device.get_indoor_temperature_raw())
            logger.info("Temperature: %s\N{DEGREE SIGN}F", value)
            speaker.speak(text=f"The current indoor temperature is {value}\N{DEGREE SIGN}F {models.env.title}!")
            return
        if "heat" in phrase:
            value = util.format_nos(Thermostat.device.get_heat_setpoint_raw())
            logger.info("Heat set point: %s\N{DEGREE SIGN}F", value)
            speaker.speak(text=f"The current heat set point is {value}\N{DEGREE SIGN}F {models.env.title}!")
            return
        if "cool" in phrase:
            value = util.format_nos(Thermostat.device.get_cool_setpoint_raw())
            logger.info("Cool set point: %s\N{DEGREE SIGN}F", value)
            speaker.speak(text=f"The current cool set point is {value}\N{DEGREE SIGN}F {models.env.title}!")
            return
    if "outdoor" in phrase:
        if "temperature" in phrase:
            value = util.format_nos(Thermostat.device.get_outdoor_temperature_raw())
            logger.info("Outdoor temperature: %s\N{DEGREE SIGN}F", value)
            speaker.speak(text=f"The current outdoor temperature is {value}\N{DEGREE SIGN}F {models.env.title}!")
            return
    speaker.speak(f"I'm sorry {models.env.title}! I'm not programmed to retrieve this information.")


def set_thermostat(phrase: str) -> None:
    """Update operations to be performed on the thermostat.

    Args:
        phrase: Takes the phrase spoken as an argument.
    """
    if "cool" in phrase:
        if value := util.extract_nos(phrase, method=int):
            Thermostat.device.set_temp_cool_setpoint(value)
            speaker.speak(text=f"I've set the thermostat to cool, {value}\N{DEGREE SIGN}F {models.env.title}!")
        else:
            speaker.speak(text=f"Please specify a value for the cool point {models.env.title}!")
    if "heat" in phrase:
        if value := util.extract_nos(phrase, method=int):
            Thermostat.device.set_temp_heat_setpoint(value)
            speaker.speak(text=f"I've set the thermostat to heat, {value}\N{DEGREE SIGN}F {models.env.title}!")
        else:
            speaker.speak(text=f"Please specify a value for the heat point {models.env.title}!")


def thermostat_controls(phrase: str) -> None:
    """Directs to the target function based on user requirement.

    Args:
        phrase: Takes the phrase spoken as an argument.
    """
    if all((models.env.tcc_username, models.env.tcc_password, models.env.tcc_device_name)):
        phrase = phrase.lower()
    else:
        logger.warning("TCC email or password or device_name not found.")
        support.no_env_vars()
        return
    expiry = util.epoch_to_datetime(seconds=Thermostat.expiration, format_="%B %d, %Y - %I:%M %p")
    if time.time() - Thermostat.expiration >= 86_400:
        logger.info("Creating a new connection since the current session expired at: %s", expiry)
        create_connection()
    else:
        logger.info("Current session is valid until: %s", expiry)
    if Thermostat.device == "LOGIN":
        speaker.speak(f"I'm sorry {models.env.title}! I ran into an authentication error.")
        return
    if Thermostat.device == "DEVICE":
        speaker.speak(f"I'm sorry {models.env.title}! "
                      f"I wasn't able to find the thermostat, {models.env.tcc_device_name} in your account.")
        return
    if Thermostat.device:
        logger.debug("Device instantiated")
    else:
        logger.critical("Something went wrong")
        speaker.speak(f"I'm sorry {models.env.title}! I wasn't able to connect to your thermostat.")
        return
    if "set" in phrase.split():
        set_thermostat(phrase)
    else:
        get_thermostat(phrase)
