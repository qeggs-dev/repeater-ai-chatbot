import random
import asyncio

from .....auxiliary.aioping.executor import Response
from fastapi.responses import ORJSONResponse
from .._send_ping import send_ping, Detail
from .....global_config_manager import ConfigManager
from .....repeater_main import RepeaterMain
from .....special_exception import HTTPException
from .._router import ping_provider_router
from .request import PingRequest
from .response import PingResponse, PingDetail

@ping_provider_router.post("/{user_id}")
async def ping_provider(user_id: str, request: PingRequest):
    global_config = ConfigManager.get_configs()
    server = RepeaterMain.get_now_server()
    runtime = server.runtime
    user_configs = await runtime.user_config_manager.load(user_id)

    model_uids = request.model_uid

    if model_uids is None:
        model_uids = user_configs.model_uid
    if model_uids is None:
        model_uids = global_config.model_api.default_model_uid
    
    if isinstance(model_uids, list):
        model_uid = random.choice(model_uids)
    elif isinstance(model_uids, str):
        model_uid = model_uids
    else:
        raise HTTPException(detail="Invalid model uid")
    
    response = await runtime.model_info_client.get_models(model_uid)
    if response:
        response_data = response.get_data()
        if response_data is None:
            raise HTTPException(detail="Invalid response data")
        models = response_data.models
    else:
        raise HTTPException(detail=f"Invalid response ({response.code})")
    
    model_urls = {model.url if model.proxy is None else model.proxy for model in models}
    
    ping_details = [
        Detail(
            url = model_url,
            timeout = request.timeout,
            times = request.times,
            size = request.size,
            interval = request.interval,
        )
        for model_url in model_urls
    ]

    tasks = [
        asyncio.create_task(
            send_ping(detail)
        )
        for detail in ping_details
    ]

    responses = await asyncio.gather(*tasks)

    success_count: int = 0
    time_ms: list[float] = []
    details: list[Detail] = []

    for response in responses:
        detail = PingDetail(
            host_names = response.host_names,
            ip = response.ip,
        )
        total_time_ms: float = 0.0
        ping_response = response.responses
        for ping_detail in ping_response:
            ping_detail: Response

            if ping_detail.success:
                success_count += 1
            
            time_ms.append(ping_detail.time_elapsed_ms)
            detail.time.append(ping_detail.time_elapsed_ms)

            total_time_ms += ping_detail.time_elapsed_ms
            if ping_detail.time_elapsed_ms > detail.max_time:
                detail.max_time = ping_detail.time_elapsed_ms
            if ping_detail.time_elapsed_ms < detail.min_time or detail.min_time == 0.0:
                detail.min_time = ping_detail.time_elapsed_ms
        
        detail.avg_time = total_time_ms / len(ping_response)
        detail.packet_loss = ping_response.packet_loss
        details.append(detail)

    return ORJSONResponse(
        content = PingResponse(
            success_count = success_count,
            average_time_spent = sum(time_ms) / len(time_ms) if len(time_ms) > 0 else 0,
            details = details
        ).model_dump()
    )
