from pydantic import BaseModel

class FastStatisticsConfig(BaseModel):
    title_width: int = 50
    chart_width: int = 50
    chart_height: int = 10