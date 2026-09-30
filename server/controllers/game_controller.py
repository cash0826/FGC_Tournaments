from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from services import GameService
from utils.errors import AppError
from utils.require import require_admin

# /games
class GameController(Resource):
  def get(self):
    try:
      games = GameService.get_all()
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return [game.to_dict() for game in games]
  
  @jwt_required()
  @require_admin
  def post(self):
    data = request.get_json()
    
    try:
      new_game = GameService.create(data)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    
    return new_game.to_dict()
  
# /games/<int:game_id>
class GameInstanceController(Resource):
  def get(self, game_id):
    try:
      game = GameService.get_by_id(game_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return game.to_dict()
  
  @jwt_required
  @require_admin
  def patch(self, game_id):
    data = request.get_json()
    
    try:
      updated_game = GameService.update(game_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return updated_game.to_dict()
  
  @jwt_required()
  @require_admin
  def delete(self, game_id):
    try:
      delete = GameService.delete(game_id)
    except AppError as error:
      return {"error": str(error)}, error.status_code
    return {"message": "Game deleted successfully"}, 200