"""The Synology Photo Album integration."""
from __future__ import annotations

import logging

from homeassistant.components.media_source import async_register_source
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from . import media_source as synology_media_source

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = []


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Synology Photo Album component."""
    # Register media source at setup time
    hass.data.setdefault(DOMAIN, {})
    synology_source = await synology_media_source.async_get_media_source(hass)
    async_register_source(hass, synology_source)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Synology Photo Album from a config entry."""
    # Store config entry data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Remove config entry data
    if DOMAIN in hass.data:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return True

