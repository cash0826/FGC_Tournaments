from extensions import db

class Role(db.Model):
  __tablename__ = "roles"
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), default='viewer', nullable=False)
  description = db.Column(db.Text)
  is_system_role = db.Column(db.Boolean, nullable=False, default=False)
  
  # TODO: relationships
  
  # TODO: name and is_system_role validations
  
  def to_dict(self):
    return {
      "name": self.name,
      "description": self.description,
      "is_system_role": self.is_system_role
    }
    