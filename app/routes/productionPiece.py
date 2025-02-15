from flask import Blueprint, request, jsonify
from app import db
from app.models import ProductionPiece
from app.utils import token_required

production_piece_bp = Blueprint('production_piece', __name__)

# Create Production Piece
@production_piece_bp.route('/api/production-pieces', methods=['POST'])
@token_required
def create_production_piece(user_id):
    data = request.get_json()

    # Validate required fields
    required_fields = ['piece_number', 'piece_name', 'price_levels']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return jsonify({'message': f'Missing fields: {", ".join(missing_fields)}'}), 400

    try:
        piece = ProductionPiece(
            piece_number=data['piece_number'],
            piece_name=data['piece_name'],
            price_levels=data['price_levels']
        )
        db.session.add(piece)
        db.session.commit()

        return jsonify({
            'message': 'Production piece created',
            'piece': {
                'id': piece.id,
                'piece_number': piece.piece_number,
                'piece_name': piece.piece_name
            }
        }), 201

    except Exception as e:
        return jsonify({'message': 'Error creating production piece', 'error': str(e)}), 500

# Get All Production Pieces
@production_piece_bp.route('/api/production-pieces', methods=['GET'])
@token_required
def get_all_production_pieces(user_id):
    pieces = ProductionPiece.query.all()
    return jsonify([
        {
            'id': piece.id,
            'piece_number': piece.piece_number,
            'piece_name': piece.piece_name,
            'price_levels': piece.price_levels,
            'created_at': piece.created_at.isoformat(),
            'updated_at': piece.updated_at.isoformat()
        } for piece in pieces
    ]), 200

# Get Production Pieces List (Simplified)
@production_piece_bp.route('/api/production-pieces/list', methods=['GET'])
@token_required
def get_list_production_pieces(user_id):
    pieces = ProductionPiece.query.all()
    return jsonify([
        {
            'id': piece.id,
            'piece_name': piece.piece_name,
            'piece_number': piece.piece_number
        } for piece in pieces
    ]), 200

# Get Production Piece by ID
@production_piece_bp.route('/api/production-pieces/<int:id>', methods=['GET'])
@token_required
def get_production_piece(user_id, id):
    piece = ProductionPiece.query.get(id)

    if not piece:
        return jsonify({'message': 'Production piece not found'}), 404

    return jsonify({
        'id': piece.id,
        'piece_number': piece.piece_number,
        'piece_name': piece.piece_name,
        'price_levels': piece.price_levels,
        'created_at': piece.created_at.isoformat(),
        'updated_at': piece.updated_at.isoformat()
    }), 200

# Update Production Piece
@production_piece_bp.route('/api/production-pieces/<int:id>', methods=['PUT'])
@token_required
def update_production_piece(user_id, id):
    piece = ProductionPiece.query.get(id)

    if not piece:
        return jsonify({'message': 'Production piece not found'}), 404

    data = request.get_json()

    try:
        if 'piece_number' in data:
            piece.piece_number = data['piece_number']
        if 'piece_name' in data:
            piece.piece_name = data['piece_name']
        if 'price_levels' in data:
            piece.price_levels = data['price_levels']

        db.session.commit()

        return jsonify({
            'message': 'Production piece updated',
            'piece': {
                'id': piece.id,
                'piece_number': piece.piece_number,
                'piece_name': piece.piece_name
            }
        }), 200

    except Exception as e:
        return jsonify({'message': 'Error updating production piece', 'error': str(e)}), 500

# Delete Production Piece
@production_piece_bp.route('/api/production-pieces/<int:id>', methods=['DELETE'])
@token_required
def delete_production_piece(user_id, id):
    piece = ProductionPiece.query.get(id)

    if not piece:
        return jsonify({'message': 'Production piece not found'}), 404

    try:
        db.session.delete(piece)
        db.session.commit()
        return jsonify({'message': 'Production piece deleted'}), 200

    except Exception as e:
        return jsonify({'message': 'Error deleting production piece', 'error': str(e)}), 500

# Get Production Piece By Number
@production_piece_bp.route('/api/production-pieces/number/<string:number>', methods=['GET'])
@token_required
def get_production_piece_by_number(user_id, number):
    piece = ProductionPiece.query.filter_by(piece_number=number).first()

    if not piece:
        return jsonify({'message': 'Production piece not found'}), 404

    return jsonify({
        'id': piece.id,
        'piece_number': piece.piece_number,
        'piece_name': piece.piece_name,
        'price_levels': piece.price_levels
    }), 200