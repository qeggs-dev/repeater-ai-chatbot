from pydantic import BaseModel

class SegmentPricing(BaseModel):
  up_to: int | None = None
  price: str | None = None