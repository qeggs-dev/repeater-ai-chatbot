from fastapi.responses import ORJSONResponse

from ...._resource import Resource
from .._user_data_type import UserDataType, get_manager
from .....Nexus_Client import InvalidUUIDError
from ._environment_model import EnvironmentModel
from ._upload_model import UploadRequest, UploadResponse

@Resource.app.post("/nexus/upload/{user_id}/environment")
async def upload_nexus(user_id: str, request: UploadRequest):
    context_manager = get_manager(UserDataType.CONTEXT)
    prompt_manager = get_manager(UserDataType.PROMPT)
    config_manager = get_manager(UserDataType.CONFIG)

    data = EnvironmentModel(
        context = await context_manager.load(user_id),
        prompt = await prompt_manager.load(user_id),
        config = await config_manager.load(user_id)
    )
    try:
        response = await Resource.nexus_client.submit(
            "environment",
            content = {
                "metadata": {
                    "user_id": user_id
                },
                "content": data
            },
            timeout = request.timeout
        )
    except InvalidUUIDError as e:
        return ORJSONResponse(
            content=UploadResponse(
                message = "Invalid uuid",
                nexus_message = str(e)
            ).model_dump(exclude_none=True),
            status_code = 400
        )

    if response.code == 200:
        data = response.data()
        if data is None:
            return ORJSONResponse(
                content=UploadResponse(
                    message = "Nexus response error",
                    nexus_message = response.content
                ).model_dump(exclude_none=True),
                status_code = 502
            )
        else:
            return ORJSONResponse(
                content = UploadResponse(
                    file_uuid = data.file_uuid,
                    message = "File uploaded",
                    nexus_message = response.content
                ).model_dump(exclude_none=True),
                status_code = 200
            )
    else:
        return ORJSONResponse(
            content=UploadResponse(
                message = "Nexus server error",
                nexus_message = response.content
            ).model_dump(exclude_none=True),
            status_code = 500
        )