from models import UserSocialAccount, Platform
from .base_service import BaseService
from utils.errors import NotFoundError, ValidationError

class SocialAccountService(BaseService):
  model = UserSocialAccount
  
  @classmethod
  def get_social_accounts_by_platform(cls, platform):   # Searches platform from string instead of id
    return cls.model.query.filter_by(platform=platform).first()

  @classmethod
  def create_linked_account(cls, user_id, data):
    if not isinstance(data, dict):
      raise ValidationError("Request body must be a JSON object")

    platform_value = data.get("platform")
    if not isinstance(platform_value, str):
      raise ValidationError("Platform must be a string")
    platform = platform_value.strip().lower()
    if not platform:
      raise ValidationError("Platform is required")

    try:    # Checks that input matches one of the Enum object
      platform_enum = Platform(platform)
    except ValueError as error:
      raise ValidationError(f"{platform} is not a valid platform") from error

    data["user_id"] = user_id
    data["platform"] = platform_enum.name
    return super().create(data)
  
  @classmethod
  def unlink_social(cls, user_id, platform):
    if not isinstance(platform, str) or not platform.strip():
      raise ValidationError("Platform is required")
    
    instance = SocialAccountService.get_social_accounts_by_platform(platform.strip().upper())
    if not instance:
      raise NotFoundError(f"{platform} platform account was not found")
    
    return super().delete(instance.id)