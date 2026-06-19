from pydantic import BaseModel


class SystemIdentificationConfig(BaseModel):
    system_name: str = "Repeater AI System"
    system_ua: str = "Repeater AI System"
    crawler_name: str = "Repeater AI Crawler"