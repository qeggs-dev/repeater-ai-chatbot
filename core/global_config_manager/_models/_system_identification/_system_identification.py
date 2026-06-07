from pydantic import BaseModel


class SystemIdentificationConfig(BaseModel):
    system_ua: str = "Repeater AI System"
    crawler_name: str = "Repeater AI Crawler"