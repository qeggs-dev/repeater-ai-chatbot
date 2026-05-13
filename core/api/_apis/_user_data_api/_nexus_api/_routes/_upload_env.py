from fastapi.responses import ORJSONResponse

from ......repeater_main import RepeaterMain
from .._router import nexus_router
from ..._user_data_type import UserDataType, get_manager
from ......clients.nexus_client import InvalidUUIDError
from .._models import EnvironmentModel
from .._models import UploadRequest, UploadResponse

@nexus_router.post("/upload/{user_id}/environment")
async def upload_env_to_nexus(user_id: str, request: UploadRequest):
    context_manager = get_manager(UserDataType.CONTEXT)
    prompt_manager = get_manager(UserDataType.PROMPT)
    config_manager = get_manager(UserDataType.CONFIG)
    
    server = RepeaterMain.get_now_server()
    runtime = server.runtime

    data = EnvironmentModel(
        context = await context_manager.load(user_id = user_id),
        prompt = await prompt_manager.load(user_id = user_id),
        config = await config_manager.load(user_id = user_id)
    )
    try:
        response = await runtime.nexus_client.submit(
            "repeater.environment",
            content = {
                "metadata": {
                    "user_id": user_id
                },
                "content": data.model_dump(exclude_none=True)
            },
            timeout = request.timeout
        )
    except InvalidUUIDError as e:
        return ORJSONResponse(
            content=UploadResponse(
                message = "Invalid uuid",
                nexus_message = {
                    "error": str(e)
                }
            ).model_dump(exclude_none=True),
            status_code = 400
        )

    if response.code == 200:
        data = response.get_data()
        if data is None:
            return ORJSONResponse(
                content=UploadResponse(
                    message = "Nexus response error",
                    nexus_message = response.json_or_str(),
                ).model_dump(exclude_none=True),
                status_code = 502
            )
        else:
            return ORJSONResponse(
                content = UploadResponse(
                    resource_uuid = data.resource_uuid,
                    message = "File uploaded",
                    nexus_message = response.json_or_str(),
                ).model_dump(exclude_none=True),
                status_code = 200
            )
    else:
        return ORJSONResponse(
            content=UploadResponse(
                message = "Nexus server error",
                nexus_message = response.json_or_str(),
            ).model_dump(exclude_none=True),
            status_code = 500
        )