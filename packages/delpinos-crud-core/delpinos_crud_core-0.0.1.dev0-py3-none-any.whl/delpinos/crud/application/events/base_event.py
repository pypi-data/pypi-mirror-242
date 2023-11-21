# -*- coding: utf-8 -*-
# pylint: disable=C0114

from typing import Dict
from delpinos.core.factories.factory import Factory
from delpinos.crud.domain.events.base_event_abstract import BaseEventAbstract

from delpinos.crud.domain.validators.base_validator_abstract import (
    BaseValidatorAbstract,
)
from delpinos.crud.domain.integrations.base_integration_abstract import (
    BaseIntegrationAbstract,
)
from delpinos.crud.domain.entities.trigger_entity import TriggerEntity


from domain.entities.trigger_entity import TriggerEntity


class BaseEvent(BaseEventAbstract, Factory):
    @property
    def validator(self) -> BaseValidatorAbstract:
        raise NotImplementedError()

    @property
    def integration(self) -> BaseIntegrationAbstract:
        raise NotImplementedError()

    def validate_insert(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return self.validator.validate_insert(trigger_obj)

    def validate_update(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return self.validator.validate_update(trigger_obj)

    def validate_delete(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return self.validator.validate_delete(trigger_obj)

    def integrate_insert(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return self.integration.integrate_insert(trigger_obj)

    def integrate_update(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return self.integration.integrate_update(trigger_obj)

    def integrate_delete(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return self.integration.integrate_delete(trigger_obj)

    def before_insert(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return trigger_obj

    def before_update(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return trigger_obj

    def before_delete(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return trigger_obj

    def after_insert(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return trigger_obj

    def after_update(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return trigger_obj

    def after_delete(self, trigger_obj: TriggerEntity) -> TriggerEntity:
        return trigger_obj
