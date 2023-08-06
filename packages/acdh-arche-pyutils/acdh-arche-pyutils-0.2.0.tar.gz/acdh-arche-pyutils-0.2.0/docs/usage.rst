=====
Usage
=====

Retrieve the API-Configuration::

    from acdh_arche_pyutils.client import ArcheApiClient

    endpoint = "https://arche-dev.acdh-dev.oeaw.ac.at/api/"
    client = ArcheApiClient(endpoint)
    client.description
    # returns something like:
    {
        'rest':
            {
                'headers': 
                    {
                        'metadataReadMode': 'X-METADATA-READ-MODE',
                        'metadataParentProperty': 'X-PARENT-PROPERTY',
                        'metadataWriteMode': 'X-METADATA-WRITE-MODE',
                        'transactionId': 'X-TRANSACTION-ID'
                    },
                'urlBase': 'https://arche-dev.acdh-dev.oeaw.ac.at',
                'pathBase': '/api/'
            },
        'schema':
            {
                id': 'https://vocabs.acdh.oeaw.ac.at/schema#hasIdentifier',
                'parent': 'https://vocabs.acdh.oeaw.ac.at/schema#isPartOf',
                'label': 'https://vocabs.acdh.oeaw.ac.at/schema#hasTitle',
                ...
            }
        }
    }