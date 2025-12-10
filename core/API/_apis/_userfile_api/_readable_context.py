from ....Context_Manager import (
    ContextObject
)

def readable_context(context: ContextObject) -> str:
    text = "======== Context  ========\n"
    for item in context.context_list:
        text += f"[{item.role}]: \n{item.content}\n\n"
        text += "==========================\n\n"
    return text