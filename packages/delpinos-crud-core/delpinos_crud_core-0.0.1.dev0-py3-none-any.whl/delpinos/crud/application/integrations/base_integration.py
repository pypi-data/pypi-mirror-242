# -*- coding: utf-8 -*-
# pylint: disable=C0114

from delpinos.core.factories.factory import Factory
from delpinos.crud.domain.entities.trigger_entity import TriggerEntity
from delpinos.crud.domain.integrations.base_integration_abstract import (
    BaseIntegrationAbstract,
)


class BaseIntegration(BaseIntegrationAbstract, Factory):
    def integrate_insert(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return trigger_obj

    def integrate_update(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return trigger_obj

    def integrate_delete(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return trigger_obj
