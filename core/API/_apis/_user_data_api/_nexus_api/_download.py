from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

from ...._resource import Resource
from .._user_data_type import UserDataType, get_manager

class DownloadRequest(BaseModel):
    id: str

@Resource.app.post("/nexus/download/{user_id}/{user_data_type}")
async def download_nexus(user_id: str, user_data_type: UserDataType, request: DownloadRequest):
    manager = get_manager(user_data_type)
    response = await Resource.nexus_client.download(user_data_type.value, request.id)
    if response.code != 200:
        return ORJSONResponse(
            content={
                "message": "Nexus server error",
                "nexus_message": response.content
            }
        )
    
    data = response.data()
    if data is None:
        return ORJSONResponse(
            content={
                "message": "Nexus response error",
                "nexus_message": response.content
            }
        )
    
    await manager.save(user_id, )