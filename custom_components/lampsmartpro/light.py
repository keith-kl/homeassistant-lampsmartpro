"""Platform for light integration."""
from __future__ import annotations

from .lampsmartpro import LampSmartProAPI
import logging
import voluptuous as vol
# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv

from homeassistant.components.light import (ATTR_BRIGHTNESS, 
                                            ATTR_COLOR_TEMP_KELVIN,
                                            PLATFORM_SCHEMA,
                                            ColorMode,
                                            LightEntity,
                                            filter_supported_color_modes)

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, EVENT_HOMEASSISTANT_STOP
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

DEFAULT_NAME = "Lamp"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    }
)

_LOGGER = logging.getLogger(__name__)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    _LOGGER.info("setup_platform")
    unique_name = config[CONF_NAME]

    api = LampSmartProAPI()

    # Add devices
    add_entities([LampSmartPro(unique_name, api)], True)

def normalize_value(value: int, max: int, new_max: int) -> int:
    """Normalize value to new range."""
    return int(value * new_max / max)

class LampSmartPro(LightEntity):
    min_color_temp_kelvin = 3000
    max_color_temp_kelvin = 6400
    

    def __init__(self, name, api) -> None:
        """Initialize"""
        self._api = api
        self._name = name
        self._is_on = False

        #brightness from 0 to 255 (device format)
        self._brightness = 255
        
        self._attr_color_mode = ColorMode.COLOR_TEMP
        self._attr_supported_color_modes = set()
        
        self._attr_supported_color_modes.add(ColorMode.COLOR_TEMP)
        
        
        #color temp from 3000 to 6400 (device format)
        self._color_temp_kelvin = 6400
        _LOGGER.info("initialized")

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info"""
        return DeviceInfo(
            identifiers={
                self._name,
            },
            name=self._name,
            manufacturer="Taobao",
        )

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique, Home assistant friendly identifier for this entity"""
        return "UUID-" + self._name

    @property
    def brightness(self):
        """Return the brightness of the light.
        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._brightness

    @property
    def color_mode(self) -> ColorMode | None:
        return ColorMode.COLOR_TEMP

    @property
    def supported_color_mode(self) -> Set[ColorMode] | None:
        return {ColorMode.COLOR_TEMP}
        
    @property
    def color_temp_kelvin(self) -> int | None:
        """Return the color temperature of the light.
        This method is optional. Removing it indicates to Home Assistant
        that color_temp is not supported for this light.
        """
        return self._color_temp_kelvin


    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._is_on

    def turn_on(self, **kwargs: Any) -> None:
        _LOGGER.debug("Run setup pairing %s", kwargs)
        self._api.setup()
        
        _LOGGER.debug("turn on %s", kwargs)
        self._api.turn_on()
        self._is_on = True
        
        brightness_unit = normalize_value(self._brightness, 255, 9);
        
        if ATTR_BRIGHTNESS in kwargs:
            self._brightness = kwargs[ATTR_BRIGHTNESS]
            brightness_unit = normalize_value(kwargs[ATTR_BRIGHTNESS], 255, 9)
            _LOGGER.debug("set brightness to %s", brightness_unit)
        if ATTR_COLOR_TEMP_KELVIN in kwargs:
            self._color_temp_kelvin = kwargs[ATTR_COLOR_TEMP_KELVIN]
            _LOGGER.debug("set color temp to %sK", self._color_temp_kelvin)
        if self._color_temp_kelvin < 4000:
            #warm
            _LOGGER.debug("warm %s", brightness_unit)
            ret = self._api.warm(brightness_unit)
        elif self._color_temp_kelvin > 5000:
            #cold
            _LOGGER.debug("cold %s", brightness_unit)
            ret = self._api.cold(brightness_unit)
        else:
            #dual
            _LOGGER.debug("dual %s", brightness_unit)
            ret = self._api.dual(brightness_unit)
        _LOGGER.debug("turn on ret=%s", ret)
        
    def turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        _LOGGER.debug("turn off %s", kwargs)
        ret = self._api.turn_off()
        self._is_on = False
        _LOGGER.debug("turn off ret=%s", ret)

    def update_state(self, attrs):
        _LOGGER.debug("update state event to %s", attrs)

    def update(self) -> None:
        _LOGGER.debug("update")

