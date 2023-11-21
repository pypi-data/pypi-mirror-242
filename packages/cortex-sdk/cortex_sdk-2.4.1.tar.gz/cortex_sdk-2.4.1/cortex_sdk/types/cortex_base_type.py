import json

class CortexBaseType:
    """
    Base class for all Cortex types.
    """

    def __init__(self):
        pass

    def _handle_extra_kwargs(self, **kwargs):
        if kwargs:
            print(f'__init__() got an unexpected keyword argument {list(kwargs.keys())[0]}\nThis may signify an outdated version of the Cortex SDK library. Please upgrade to the latest version.')

            for key, value in kwargs.items():
                setattr(self, key, value)
