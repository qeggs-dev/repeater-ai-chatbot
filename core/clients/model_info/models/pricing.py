from pydantic import BaseModel
from .segment_pricing import SegmentPricing

class Pricing(BaseModel):
  prompt: str | SegmentPricing | None = None
  image: str | SegmentPricing | None = None
  audio: str | SegmentPricing | None = None
  completion: str | SegmentPricing | None = None
  internal_reasoning: str | SegmentPricing | None = None
  web_search: str | SegmentPricing | None = None
  input_cache_read: str | SegmentPricing | None = None
  input_cache_write: str | SegmentPricing | None = None