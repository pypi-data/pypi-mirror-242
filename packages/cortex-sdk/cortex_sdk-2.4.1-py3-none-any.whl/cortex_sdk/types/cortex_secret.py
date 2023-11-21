from .cortex_base_type import CortexBaseType


class CortexSecret(CortexBaseType): 
    def __init__(
        self,
        _id:          str,
        clientKey:    str,
        friendlyName: str,
        createdDate:  str,
        updatedDate:  str,
        **kwargs
    ): 
        self.id           = _id
        self.client_key   = clientKey
        self.name         = friendlyName
        self.created_date = createdDate
        self.updated_date = updatedDate

        self._handle_extra_kwargs(**kwargs)
