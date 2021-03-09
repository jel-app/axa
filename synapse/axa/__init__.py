# -*- coding: utf-8 -*-
# Copyright 2019 The Matrix.org Foundation C.I.C.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
logger = logging.getLogger(__name__)

from typing import Dict, List, Optional, Tuple
from twisted.internet import defer
from synapse.api.constants import EventTypes, JoinRules, Membership, RoomCreationPreset
from synapse.api.errors import SynapseError
from synapse.config._base import ConfigError
from synapse.events import EventBase
from synapse.module_api import ModuleApi
from synapse.types import Requester, StateMap, UserID, get_domain_from_id

class Rules(object):
    """Allows server admins to provide a Python module implementing an extra
    set of rules to apply when processing events.

    This is designed to help admins of closed federations with enforcing custom
    behaviours.
    """

    def __init__(
        self, config: Dict, module_api: ModuleApi,
    ):
        self.module_api = module_api

        self.domains_forbidden_when_restricted = config.get(
            "domains_forbidden_when_restricted", []
        )

    @staticmethod
    def parse_config(config: Dict) -> Dict:
        """Parses and validates the options specified in the homeserver config.
        Args:
            config: The config dict.
        Returns:
            The config dict.
        Raises:
            ConfigError: If there was an issue with the provided module configuration.
        """

        return config

    async def on_create_room(
        self, requester: Requester, _config: Dict, _is_requester_admin: bool
    ) -> bool:
        """Allows only dyna to create rooms"""
        if requester.app_service is not None:
            return requester.app_service.id == "dyna"

        return False

    @defer.inlineCallbacks
    @staticmethod
    def check_threepid_can_be_invited(
        _medium: str, _address: str, _state_events: StateMap[EventBase],
    ) -> bool:
        """Disallows threepid invites"""
        return False

    @staticmethod
    async def check_event_allowed(
        _event: EventBase, _state: StateMap[EventBase]
    ) -> bool:
        """Allows all events"""
        return True
