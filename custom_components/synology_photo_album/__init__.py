"""The Photo Album Share integration."""
from __future__ import annotations

import logging

from homeassistant.components.media_source import async_register_source
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from . import media_source as photo_album_media_source

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = []


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Photo Album Share component."""
    # Register media source at setup time
    hass.data.setdefault(DOMAIN, {})
    photo_album_source = await photo_album_media_source.async_get_media_source(hass)
    async_register_source(hass, photo_album_source)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Photo Album Share from a config entry."""
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

