
"""
    Data manager
    Handles:
        Save
        Get
        Update
        Delete
        Get all
        Get by property
        Get countries
"""

from abc import ABC, abstractmethod


class IPersistenceManager:

    @abstractmethod
    def save(self, entity):
        pass
    
    @abstractmethod
    def get(self, entity_id, entity_type):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, entity_id, entity_type):
        pass

    @abstractmethod
    def get_all(self, entity_type):
        pass

    @abstractmethod
    def get_by_property(self, entity_type, property_name, property_value):
        pass

    @abstractmethod
    def get_countries(self, code):
        pass
