import base64

from ...Global_Config_Manager import ConfigManager
    
def fname_b64_encode(text: str) -> str:
    if ConfigManager.get_configs().user_data.b64_encode_path:
        encoded = base64.urlsafe_b64encode(
            text.encode("utf-8")
        ).decode("utf-8")
        return "b64_" + encoded
    else:
        return text

def fname_b64_decode(text: str) -> str:
    if ConfigManager.get_configs().user_data.b64_encode_path:
        decoded = base64.urlsafe_b64decode(
            text[4:].encode("utf-8")
        ).decode("utf-8")
        return decoded
    else:
        return text