#!/usr/bin/python3

"""
data manager
"""
class IPersistenceManager:
    def save(self, entity):
        pass

    def get(self, entity_id, entity_type):
        pass

    def update(self, entity):
        pass

    def delete(self, entity_id, entity_type):
        pass

    def get_all(self, entity_type):
        pass

    def get_by_property(self, entity_type, property_name, property_value):
        pass