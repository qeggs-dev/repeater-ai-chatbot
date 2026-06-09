from pydantic import BaseModel
from .segment_pricing import SegmentPricing

class Pricing(BaseModel):
  prompt: str | list[SegmentPricing] | None = None
  image: str | list[SegmentPricing] | None = None
  audio: str | list[SegmentPricing] | None = None
  completion: str | list[SegmentPricing] | None = None
  internal_reasoning: str | list[SegmentPricing] | None = None
  web_search: str | list[SegmentPricing] | None = None
  input_cache_read: str | list[SegmentPricing] | None = None
  input_cache_write: str | list[SegmentPricing] | None = None