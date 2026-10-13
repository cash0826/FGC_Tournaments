from models import EventSponsor, SponsorshipTier, Sponsor, Event
from .base_service import BaseService
from utils.errors import AppError, ConflictError, NotFoundError, ValidationError

class EventSponsorService(BaseService):
  model = EventSponsor
  
  @classmethod
  def assign_sponsor(cls, event_id, data):
    cls._get_event(event_id)
    sponsor_name = data.get("sponsor")
    sponsorship_tier = data.get("sponsorship_tier")
    amount = data.get("amount")
    if not isinstance(sponsor_name, str) or not sponsor_name.strip():
      raise ValidationError("Sponsor is required.")
    
    sponsor = Sponsor.query.filter_by(name=sponsor_name.strip().lower()).first()
    if not sponsor:
      raise NotFoundError("Sponsor not found.")
    
    existing = EventSponsor.query.filter_by(event_id=event_id, sponsor_id=sponsor.id).first()
    if existing:
      raise ConflictError(f"{sponsor_name} is already backing this event.")

    event_sponsor_data.pop("sponsor")
    unsupported_fields = data.keys() - {"sponsor_id", "sponsorship_tier", "amount"}
    if unsupported_fields:
      raise ValidationError(
        f"Event Sponsor fields cannot be set: {', '.join(sorted(unsupported_fields))}."
      )
      
    event_sponsor_data = dict(data)
    return super().create(event_sponsor_data)
  
  @classmethod
  def remove_sponsor(event_id, sponsor_name):
    cls._get_event(event_id)
    if not isinstance(sponsor_name, str) or not sponsor_name.strip():
      raise ValidationError("Sponsor is required.")
    
    sponsor = Sponsor.query.filter_by(name=sponsor_name.strip().lower()).first()
    if not sponsor:
      raise NotFoundError("Sponsor not found.")

    instance = EventSponsor.query.filter_by(event_id=event_id, sponsor_id=sponsor.id).first()
    if not instance:
      raise NotFoundError(f"{sponsor} is not assigned to this event.")
    
    return super().delete(instance.id)
    