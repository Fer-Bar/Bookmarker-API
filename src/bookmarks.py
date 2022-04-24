import validators
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.constants.http_status_codes import (HTTP_200_OK, HTTP_201_CREATED,
                                             HTTP_204_NO_CONTENT,
                                             HTTP_400_BAD_REQUEST,
                                             HTTP_404_NOT_FOUND,
                                             HTTP_409_CONFLICT)
from src.database import Bookmark, db
from flasgger import swag_from


bookmarks = Blueprint('bookmarks', __name__,
                    url_prefix='/api/v1/bookmarks')

@bookmarks.route('/', methods=['GET', 'POST'])
@jwt_required()
@swag_from('./docs/bookmarks/bookmarks_get.yaml', methods=['GET'])
@swag_from('./docs/bookmarks/bookmarks_post.yaml', methods=['POST'])
def handle_bookmarks():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        body = request.get_json().get('body', '')
        url = request.get_json().get('url', '')
        if not validators.url(url):
            return jsonify({
                'error': 'Enter a valid url'
                }), HTTP_400_BAD_REQUEST

        if Bookmark.query.filter_by(url=url).first():
            return jsonify({
                'error': 'URL already exists'
            }), HTTP_409_CONFLICT

        bookmark = Bookmark(
            url=url,
            body=body,
            user_id=current_user
        )
        
        db.session.add(bookmark)
        db.session.commit()

        return jsonify({
            'id': bookmark.id,
            'body': bookmark.body,
            'url': bookmark.url,
            'short_url': bookmark.generate_short_character,
            'visits': bookmark.visits,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at
        }), HTTP_201_CREATED

    if request.method == 'GET': 

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        """ 
        Return a Paginate Object who have an atributte items that
        contains the list of items in the requested page 
        """
        bookmarks = Bookmark.query.filter_by(user_id=current_user).paginate (page=page, per_page=per_page)

        data = []
         
        for bookmark in bookmarks.items:
            data.append({
                'id': bookmark.id,
                'body': bookmark.body,
                'url': bookmark.url,
                'short_url': bookmark.generate_short_character,
                'visits': bookmark.visits,
                'created_at': bookmark.created_at,
                'updated_at': bookmark.updated_at
            })

        meta = {
            'page': bookmarks.page,
            'pages': bookmarks.pages,
            'total_count': bookmarks.total,
            'next_page': bookmarks.next_num,
            'prev_page': bookmarks.prev_num,
            'has_next': bookmarks.has_next,
            'has_prev': bookmarks.has_prev
        }

        return jsonify({
            'data': data,
            'meta': meta
            }), HTTP_200_OK

@bookmarks.get('/<int:id>')
@jwt_required()
@swag_from('./docs/bookmarks/bookmark_get.yaml', methods=['GET'])
def get_bookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({
            'message': 'Item not found'
        }), HTTP_404_NOT_FOUND
    
    return jsonify({
        'id': bookmark.id,
        'body': bookmark.body,
        'url': bookmark.url,
        'short_url': bookmark.generate_short_character,
        'visits': bookmark.visits,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at
    }), HTTP_200_OK

@bookmarks.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@swag_from('./docs/bookmarks/bookmark_put_patch.yaml', methods=['PUT', 'PATCH'])
def edit_bookmark(id):
    current_user = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({
            'message': 'Item not found'
        }), HTTP_404_NOT_FOUND

    body = request.get_json().get('body', '')
    url = request.get_json().get('url', '')
    if not validators.url(url):
        return jsonify({
            'error': 'Enter a valid url'
            }), HTTP_400_BAD_REQUEST

    bookmark.body = body
    bookmark.url = url
    db.session.commit()
    return jsonify({
        'id': bookmark.id,
        'body': bookmark.body,
        'url': bookmark.url,
        'short_url': bookmark.generate_short_character,
        'visits': bookmark.visits,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at
    }), HTTP_200_OK

@bookmarks.delete('/<int:id>')
@jwt_required()
@swag_from('./docs/bookmarks/bookmark_del.yaml', methods=['DELETE'])
def delete_bookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({
            'message': 'Item not found'
        }), HTTP_404_NOT_FOUND

    db.session.delete(bookmark)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT

@bookmarks.get('/stats')
@jwt_required()
@swag_from('./docs/bookmarks/stats.yaml')
def get_stats():
    current_user = get_jwt_identity()

    items = Bookmark.query.filter_by(user_id=current_user).all()

    data = []

    for item in items:
        new_item = {
            'id': item.id,
            'url': item.url,
            'short_url': item.generate_short_character,
            'visits': item.visits
        }
        data.append(new_item)

    return jsonify({'data': data}), HTTP_200_OK