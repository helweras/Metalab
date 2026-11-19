import pytest
from dataclasses import FrozenInstanceError
from types import MappingProxyType

from metalab.agent_snapshot import AgentSnapshot
from metalab.attribute import Attribute


class TestAgentSnapshot:
    def test_init(self):
        attributes = {Attribute.HEALTH: 100}

        snapshot = AgentSnapshot(attributes)

        assert snapshot.attributes == attributes

    def test_attributes_is_mapping_proxy(self):
        snapshot = AgentSnapshot({Attribute.HEALTH: 100})

        assert isinstance(snapshot.attributes, MappingProxyType)

    def test_attributes_are_immutable(self):
        snapshot = AgentSnapshot({Attribute.HEALTH: 100})

        with pytest.raises(TypeError):
            snapshot.attributes[Attribute.HEALTH] = 50

    def test_source_mapping_changes_do_not_affect_snapshot(self):
        attributes = {Attribute.HEALTH: 100}

        snapshot = AgentSnapshot(attributes)
        attributes[Attribute.HEALTH] = 50

        assert snapshot.attributes[Attribute.HEALTH] == 100

    def test_init_copies_source_mapping(self):
        attributes = {Attribute.HEALTH: 100}

        snapshot = AgentSnapshot(attributes)

        assert snapshot.attributes is not attributes

    def test_immutable(self):
        snapshot = AgentSnapshot({Attribute.HEALTH: 100})

        with pytest.raises(FrozenInstanceError):
            snapshot.attributes = {Attribute.HEALTH: 50}
