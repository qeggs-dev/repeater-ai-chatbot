from ....Context_Manager import (
    ContextObject
)
from ....TextBuffer import TextBuffer

def readable_context(context: ContextObject) -> str:
    text_buffer = TextBuffer(separator="\n")
    text_buffer.append("======== Context  ========")
    for item in context.context_list:
        text_buffer.append(f"[{item.role.name}]:")
        if item.reasoning_content:
            text_buffer.append("Reasoning:")
            text_buffer.append(item.reasoning_content)
            text_buffer.append("")
        if item.content:
            text_buffer.append("Content:")
            text_buffer.append(item.content)
            text_buffer.append("")
        
        text_buffer.append("==========================")
        text_buffer.append("")
    return str(text_buffer)