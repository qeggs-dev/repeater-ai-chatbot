from fastapi.responses import ORJSONResponse

from ...._resource import Resource
from .._user_data_type import UserDataType, get_manager
from .....Nexus_Client import InvalidUUIDError
from ._download_model import DownloadRequest, DownloadResponse
from ._environment_model import EnvironmentModel

@Resource.app.post("/nexus/download/{user_id}/environment")
async def download_env_from_nexus(user_id: str, request: DownloadRequest):
    context_manager = get_manager(UserDataType.CONTEXT)
    prompt_manager = get_manager(UserDataType.PROMPT)
    config_manager = get_manager(UserDataType.CONFIG)
    
    try:
        response = await Resource.nexus_client.download("repeater.environment", user_id, "content")
    except InvalidUUIDError as e:
        return ORJSONResponse(
            content = DownloadResponse(
                message = "Invalid UUID",
                nexus_message = {
                    "error": str(e)
                }
            ).model_dump(),
            status_code = 400
            
        )
    if response.code != 200:
        return ORJSONResponse(
            content = DownloadResponse(
                message = "Nexus server error",
                nexus_message = response.json_or_str()
            ).model_dump(),
            status_code = 500
        )
    
    data = response.data()
    
    if data is None:
        return ORJSONResponse(
            content = DownloadResponse(
                message = "Nexus response error",
                nexus_message = response.json_or_str()
            ).model_dump(),
        )
    
    env_data = EnvironmentModel(**data.data)
    await context_manager.save(user_id, env_data.context)
    await prompt_manager.save(user_id, env_data.prompt)
    await config_manager.save(user_id, env_data.config)

    return ORJSONResponse(
        content = DownloadResponse(
            message = "Success",
            nexus_message = response.json_or_str()
        ).model_dump(),
    )