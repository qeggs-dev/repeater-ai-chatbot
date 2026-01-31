from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

from ...._resource import Resource
from .._user_data_type import UserDataType, get_manager
from .....Nexus_Client import InvalidUUIDError

class DownloadRequest(BaseModel):
    id: str

class DownloadResponse(BaseModel):
    message: str = ""
    nexus_message: str = ""

@Resource.app.post("/nexus/download/{user_id}/{user_data_type}")
async def download_nexus(user_id: str, user_data_type: UserDataType, request: DownloadRequest):
    manager = get_manager(user_data_type)
    try:
        response = await Resource.nexus_client.download(user_data_type.value, request.id)
    except InvalidUUIDError as e:
        return ORJSONResponse(
            content = DownloadResponse(
                message = "Invalid UUID",
                nexus_message = str(e)
            ).model_dump(),
            status_code = 400
            
        )
    if response.code != 200:
        return ORJSONResponse(
            content = DownloadResponse(
                message = "Nexus server error",
                nexus_message = response.content
            ).model_dump(),
        )
    
    data = response.data()
    if data is None:
        return ORJSONResponse(
            content = DownloadResponse(
                message = "Nexus response error",
                nexus_message = response.content
            ).model_dump(),
        )
    
    await manager.save(user_id, data.data)