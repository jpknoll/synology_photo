"""Config flow for Photo Album Share."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_SHARING_URL, DEFAULT_UPDATE_INTERVAL, CONF_UPDATE_INTERVAL
from .scraper import PhotoAlbumScraper

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_SHARING_URL): str,
        vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): int,
    }
)


class PhotoAlbumShareConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Photo Album Share."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        # Validate the URL
        sharing_url = user_input[CONF_SHARING_URL]
        if not sharing_url.startswith(("http://", "https://")):
            errors[CONF_SHARING_URL] = "invalid_url"
        else:
            # Test the URL by trying to fetch it
            try:
                session = async_get_clientsession(self.hass)
                scraper = PhotoAlbumScraper(sharing_url, session)
                album_info = await scraper.get_album_info()
                if not album_info:
                    errors[CONF_SHARING_URL] = "cannot_connect"
            except Exception as e:
                _LOGGER.error("Error validating URL: %s", e)
                errors[CONF_SHARING_URL] = "cannot_connect"

        if errors:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
            )

        # Check if already configured
        await self.async_set_unique_id(sharing_url)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title="Photo Album Share",
            data=user_input,
        )

