import base64

from loguru import logger

from ...Global_Config_Manager import ConfigManager
    
def user_id_encode(user_id: str) -> str:
    if ConfigManager.get_configs().user_data.b64_encode_path:
        encoded = base64.urlsafe_b64encode(
            user_id.encode("utf-8")
        ).decode("utf-8")
        logger.info(
            "Encoded user_id: {user_id} -> {encoded}",
            user_id=user_id,
            encoded=encoded
        )
        return "b64_" + encoded
    else:
        return user_id

def user_id_decode(user_id: str) -> str:
    if ConfigManager.get_configs().user_data.b64_encode_path:
        decoded = base64.urlsafe_b64decode(
            user_id[4:].encode("utf-8")
        ).decode("utf-8")
        logger.debug(
            "Decoded user_id: {user_id} -> {decoded}",
            user_id=user_id,
            decoded=decoded
        )
        return decoded
    else:
        return user_id