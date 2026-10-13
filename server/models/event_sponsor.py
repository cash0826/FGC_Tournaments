from extensions import db
from sqlalchemy.orm import validates
from enum import Enum

class SponsorshipTier(Enum):
  community = "community"
  bronze = "bronze"
  silver = "silver"
  gold = "gold"

class EventSponsor(db.Model):
  __tablename__ = "event_sponsors"
  __table_args__ = (
    db.UniqueConstraint("event_id", "sponsor_id", name="uq_event_sponsors_event_sponsor"),
  )
  
  id = db.Column(db.Integer, primary_key=True)
  event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
  sponsor_id = db.Column(db.Integer, db.ForeignKey("sponsors.id"), nullable=False)
  sponsorship_tier = db.Column(db.Enum(SponsorshipTier), default=SponsorshipTier.community)
  amount = db.Column(db.Numeric(10, 2))
  
  # event_sponsors belongs to a single Sponsor
  sponsor = db.relationship("Sponsor", back_populates="sponsored_events")
  
  # event_sponsors belongs to a single Event
  event = db.relationship("Event", back_populates="sponsors")
  
  @validates("event_id", "sponsor_id")
  def validate_ids(self, key, value):
    if not isinstance(value, int):
      raise ValueError(f"{key} must be an integer")
    return value
  
  def to_dict(self):
    return {
      "event_id": self.event_id,
      "sponsor": self.sponsor.to_dict(),
      "sponsorship_tier": self.sponsorship_tier.value,
      "amount": self.amount
    }