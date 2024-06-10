#!/usr/bin/python3

import json
import os
from iPersistenceManager import IPersistenceManager # no anda

"""
DataManager class that implements the iPersistenceManager interface.
Handles data persistence using JSON files.
"""


class DataManager(IPersistenceManager):
    """
    Handles data persistence using JSON files
    """
    def __init__(self, storage_path='data'):
        """
        Initializes the DataManager with a storage path
        Attributes:
            storage_path: The path to the storage directory
        """
        self.storage_path = storage_path
        if not os.path.exists(storage_path):
            os.makedirs(self.storage_path)

    def _file_path(self, entity_type, entity_id=None):
        """
        Generates the file path for an entity
        Attributes:
            entity_type: the type of an entity
            entity_id: The id of the entity
        Return: the file path for the entity
        """
        if entity_id:
            return os.path.join(self.storage_path, f"{entity_type}_{entity_id}.json")
        else:
            return os.path.join(self.storage_path, f"{entity_type}.json")
        
    def save(self, entity):
        """
        Save an entity to a JSON file
        Attributes:
            entity: the entity to save to a JSON file.
        """
        entity_type = type(entity).__name__
        entity_id = entity.get('id')
        file_path = self._file_path(entity_type, entity_id)

        with open(file_path, 'w') as file:
            json.dump(entity, file)

    def get(self, entity_id, entity_type):
        """
        Retrieves an entity from a JSON file
        Attributes:
            entity_id: the ID of the entity
            entity_type: the type of the entity
        Return: the retrieved entity or None if not found
        """

        file_path = self._file_path(entity_type, entity_id)
        if not file_path.exists:
            return None
        else:
            with open(file_path, 'r') as file:
                return json.load(file)

    def update(self, entity):
        """
        Update an entity by saving it again to the JSON file
        Attributes:
            entity: the entity to update
        """
        self.save(entity)

    def delete(self, entity_id, entity_type):
        """
        Delete an entity by removing its JSON file
        Attributes:
            entity_id: the ID of the entity to delete
            entity_type: the type of the identity
        Raises:
            FileNotFoundError: No such entity {entity_type} with {entity_id}
        """
        file_path = self._file_path(entity_id, entity_type)

        if file_path.exists():
            file_path.unlink()
        else:
            raise FileNotFoundError(f"No such entity: {entity_type} with {entity_id}")
            """
            no estoy segura del raise peeero para que no se rompa todo
            """
