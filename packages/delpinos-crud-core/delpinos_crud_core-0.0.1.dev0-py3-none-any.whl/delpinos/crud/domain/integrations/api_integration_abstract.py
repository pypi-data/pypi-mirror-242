# -*- coding: utf-8 -*-
# pylint: disable=C0114

from typing import Callable

import requests
from delpinos.crud.domain.entities.api_integration_entity import ApiIntegrationEntity
from delpinos.crud.domain.integrations.base_integration_abstract import (
    abstractmethod,
    BaseIntegrationAbstract,
)


class ApiIntegrationAbstract(BaseIntegrationAbstract):
    @abstractmethod
    def save_api_integration(
        self, api_integration: ApiIntegrationEntity
    ) -> ApiIntegrationEntity:
        raise NotImplementedError()

    @abstractmethod
    def execute_api(
        self,
        request: Callable[[], requests.Response],
        api_integration: ApiIntegrationEntity,
    ) -> ApiIntegrationEntity:
        raise NotImplementedError()
