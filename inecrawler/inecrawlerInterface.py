from abc import abstractmethod
from abc import ABCMeta


class INECrawlerInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_operation_list():
        """ This funciton must be used to obtain a list of all operation ids
            from the portal.

            return ids: list
        """
        pass
    
    @abstractmethod
    def get_tables(id):
        """ This funciton must be used to obtain the tables from a given operation id.

            return ids: list
        """
        pass

    @abstractmethod
    def get_elements(id):
        """ This function must be used to obtain the metadata from a given
            table id and also format the metadata with the following
            structure inside a dict:

            metadata['identifier'] -> Packages identifier: OperationID_TableID_ElementID
            metadata['title'] -> Packages title: OperationName_TableName
            metadata['description'] -> Packages Description: OperationName_TableName_ElementName
            metadata['theme'] -> Packages category, theme, topic... (Turism)
            meta['resources'] -> List of resources: fileName.csv (ElementData)
                            resource['id'] -> Resource name: ElementId
                            resource['name'] -> Resource name: ElementName
                            resource['date'] -> Resource date: ElementDate
                            resource['year'] -> Resource year: ElementYear
                            resource['month'] -> Resource month: ElementMonth
                            resource['value'] -> Resource value: ElementValue
            metadata['modified'] -> Last modification of the table
            metadata['license'] -> INE license
            metadata['source'] -> INE url

            return metadata: dict
        """
        pass
