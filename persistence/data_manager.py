
"""
    DataManager class that implements the iPersistenceManager interface.
    Handles data persistence using JSON files.
"""

import json
import os
import glob
from persistence.data_manager_interface import IPersistenceManager


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
        
    def save(self, id, type, entity):
        """
            --REVISAR--
            añadí cosas para guardarlo bien

        Save an entity to a JSON file
        Attributes:
            entity: the entity to save to a JSON file.
        Returns:
            The entity and entity type in a JSON file
        """

        entity_type = type
        entity_id = id
        file_path = self._file_path(entity_type, entity_id)

        with open(file_path, 'w') as file:
            json.dump(entity, file)
        
        result = {
            'entity': entity,
            'entity_type': entity_type
        }
        return result

    def get(self, entity_id, entity_type):
        """
        Retrieves an entity from a JSON file
        Attributes:
            entity_id: the ID of the entity
            entity_type: the type of the entity
        Return: the retrieved entity or None if not found
        """

        file_path = self._file_path(entity_type, entity_id)
        if not os.path.exists(file_path):
            return None
        else:
            with open(file_path, 'r') as file:
                entity = json.load(file)
            return entity

    def update(self, entity_id, entity_type, data):
        """
        Update an entity by saving it again to the JSON file
        Attributes:
            entity_id: the id entity
            entity_type: type to entity
            data: new data fo entity
        Returns:
            The entity and entity type to update
        """
        file_path = self._file_path(entity_type, entity_id)

        with open(file_path, 'r') as file:
            entiy = json.load(file)

            entiy.update(data)

        with open(file_path, 'w') as file:
            json.dump(entiy, file)

        return data

    def delete(self, entity_id, entity_type):
        """
        Delete an entity by removing its JSON file
        Attributes:
            entity_id: the ID of the entity to delete
            entity_type: the type of the identity
        Raises:
            FileNotFoundError: No such entity {entity_type} with {entity_id}
        Returns:
            The entity deleted
        """
        file_path = self._file_path(entity_type, entity_id)
        if os.path.exists(file_path):
            os.remove(file_path)
            return {f'Entity {entity_id} of type {entity_type} deleted'}
        else:
            raise FileNotFoundError(f"No such entity: {entity_type} with {entity_id}")
            """
            no estoy segura del raise peeero para que no se rompa todo
            """

    def get_all(self, entity_type):
        """
        Retrieves all entities of a given type
        Attributes:
        entity_type: the type of entities to retrieve
        Return: a list of all entities of the given type in JSON
        """
        path = os.path.join(self.storage_path, f"{entity_type}_*.json")
        files = glob.glob(path)
        entities = []
        for file_path in files:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    entities.append(data)
        return entities

    def get_by_property(self, entity_type, property_name, property_value):
        """
        Retrieves all entities of a given type that match a specific property
        Attributes:
            entity_type: the type of entities to retrieve
            property_name: the property name to match
            property_value: the property value to match
        Return: a list of entities that match the given property in JSON
        """
        all_entities = self.get_all(entity_type)
        matched_entities = [entity for entity in all_entities if entity.get(property_name) == property_value]
        return matched_entities
    
    def get_countries(self, code):
        """
        Calls the method get_by_property
        Attributes:
            code: as name of property
            country: as type of entity
        Returns:
            All countries that matches with a specific code in JSON
        """
        return self.get_by_property("Country", "code", code)
