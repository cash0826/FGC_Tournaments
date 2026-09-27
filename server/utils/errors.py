class AppError(Exception):
  def __init__(self, message, status_code=400):
    super().__init__(message)
    self.message = message
    self.status_code = status_code
    
class ValidationError(AppError):
  def __init__(self, message):
    super().__init__(message, 400)

class AuthenticationError(AppError):
  def __init__(self, message="Invalid email or password"):
    super().__init__(message, 401)
  
class AuthorizationError(AppError):
  def __init__(self, message="Unauthorized"):
    super().__init__(message, 403)

class NotFoundError(AppError):
  def __init__(self, message="Resource not found"):
    super().__init__(message, 404)

class ConflictError(AppError):
  def __init__(self, message):
    super().__init__(message, 409)

