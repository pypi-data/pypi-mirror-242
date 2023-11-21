from typing                   import List, Optional, Union
from .api_resource            import APIResource
from ..types.cortex_inference import CortexInference

class Inferences(APIResource):
    """
    Cortex Inferences API.
    """
    @classmethod
    def get(
        cls,
        resource_id: Optional[str] = None,
        model_id: Optional[str] = None,
        pipeline_id: Optional[str] = None,
        successful: Optional[bool] = None,
        annotation: Optional[str] = None,
        tags: Optional[List[str]] = None,
        email: Optional[str] = None,
        ip_address: Optional[str] = None,
        session_id: Optional[str] = None,
        thread_id: Optional[str] = None
    ) -> Union[CortexInference, List[CortexInference]]:
        """
        Gets one or many inferences.

        Args:
            resource_id (str, optional):
            The ID of the inference to retrieve. If None, retrieves all
            inferences.

        Returns:
            CortexInference or list[CortexInference]: 
            If resource_id is provided, returns a single CortexInference object.
            If resource_id is None, returns a list of CortexInference objects.
        """
        params = cls._handle_optional_params({
            'model_id': model_id,
            'pipeline_id': pipeline_id,
            'successful': successful,
            'annotation': annotation,
            'tags': tags,
            'email': email,
            'ip_address': ip_address,
            'session_id': session_id,
            'thread_id': thread_id
        })

        return cls._generic_get(
            path        = f'/inferences/{resource_id or ""}',
            return_type = CortexInference,
            params      = params
        )
