import base64

from loguru import logger

from ...Global_Config_Manager import ConfigManager
    
def fname_b64_encode(user_id: str) -> str:
    if ConfigManager.get_configs().user_data.b64_encode_path:
        encoded = base64.urlsafe_b64encode(
            user_id.encode("utf-8")
        ).decode("utf-8")
        return "b64_" + encoded
    else:
        return user_id

def fname_b64_decode(user_id: str) -> str:
    if ConfigManager.get_configs().user_data.b64_encode_path:
        decoded = base64.urlsafe_b64decode(
            user_id[4:].encode("utf-8")
        ).decode("utf-8")
        return decoded
    else:
        return user_id