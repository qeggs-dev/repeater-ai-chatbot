import base64

from ...global_config_manager import ConfigManager
    
def fname_b64_encode(text: str) -> str:
    """
    Encodes the text to base64 if the config is set to true

    :param text: Text to encode
    """
    if ConfigManager.get_configs().user_data.b64_encode_path:
        encoded = base64.urlsafe_b64encode(
            text.encode("utf-8")
        ).decode("utf-8")
        return "b64_" + encoded
    else:
        return text

def fname_b64_decode(text: str) -> str:
    """
    Decodes the text from base64 if the config is set to true

    :param text: Text to decode
    """
    if ConfigManager.get_configs().user_data.b64_encode_path:
        decoded = base64.urlsafe_b64decode(
            text.removeprefix(
                "b64_"
            ).encode("utf-8")
        ).decode("utf-8")
        return decoded
    else:
        return text