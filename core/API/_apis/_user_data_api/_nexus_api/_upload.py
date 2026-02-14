from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

from ...._resource import Resource
from .._user_data_type import UserDataType, get_manager
from .....Nexus_Client import InvalidUUIDError

class UploadRequest(BaseModel):
    timeout: int | None = None

class UploadResponse(BaseModel):
    message: str = ""
    nexus_message: str = ""
    file_uuid: str | None = None

@Resource.app.post("/nexus/upload/{user_id}/{user_data_type}")
async def upload_nexus(user_id: str, user_data_type: UserDataType, request: UploadRequest):
    manager = get_manager(user_data_type)
    data = await manager.load(user_id)
    try:
        response = await Resource.nexus_client.submit(
            user_data_type.value,
            data,
            request.timeout
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