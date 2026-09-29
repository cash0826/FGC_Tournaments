from models import UserSocialAccount
from .base_service import BaseService
from utils.errors import NotFoundError, ValidationError

class SocialAccountService(BaseService):
  model = UserSocialAccount
  
  @classmethod
  def get_social_accounts_by_platform(cls, platform):
    return cls.model.query.filter_by(platform=platform).first()

  @classmethod
  def create_linked_account(cls, user_id, data):
    data["user_id"] = user_id
    return super().create(data)
  
  @classmethod
  def unlink_social(cls, user_id, platform):
    if not isinstance(platform, str) or not platform.strip():
      raise ValidationError("Platform is required")
    
    instance = SocialAccountService.get_social_accounts_by_platform(platform)
    if not instance:
      raise NotFoundError("Platform not found")
    
    return super().delete(instance.id)