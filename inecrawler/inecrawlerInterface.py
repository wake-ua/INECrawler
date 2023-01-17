from abc import abstractmethod
from abc import ABCMeta


class INECrawlerInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_package_list():
        """ This funciton must be used to obtain a list of all packages ids
            from the portal.

            return ids: list
        """
        pass

    @abstractmethod
    def get_package(id):
        """ This function must be used to obtain the metadata from a given
            package id and also format the metadata with the following
            structure inside a dict:

            metadata['identifier'] -> Packages identifier
            metadata['title'] -> Packages title
            metadata['description'] -> Packages Description
            metadata['theme'] -> Packages category, theme, topic...
            meta['resources'] -> List of resources
                            resource['name'] -> Resource name
                            resource['downloadUrl'] -> Resource url to download
                            resource['mediaType'] -> Type of resource Ex. csv, pdf..
            metadata['modified'] -> Last modification of the package
            metadata['license'] -> Package license
            metadata['source'] -> Package source(domain)

            return metadata: dict
        """
        pass
