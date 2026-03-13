from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

from ...._resource import Resource
from .._user_data_type import UserDataType, get_manager
from .....Nexus_Client import InvalidUUIDError
from ._upload_model import UploadRequest, UploadResponse

@Resource.app.post("/nexus/upload/{user_id}/single/{user_data_type}")
async def upload_to_nexus(user_id: str, user_data_type: UserDataType, request: UploadRequest):
    manager = get_manager(user_data_type)
    data = await manager.load(user_id)
    if isinstance(data, BaseModel):
        data = data.model_dump(exclude_none = True)
    try:
        response = await Resource.nexus_client.submit(
            f"repeater.{user_data_type.value}",
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
                nexus_message = {
                    "error": str(e)
                }
            ).model_dump(exclude_none=True),
            status_code = 400
        )

    if response.code == 200:
        data = response.data()
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
                    resources_uuid = data.resource_uuid,
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