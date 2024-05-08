from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Books, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'title': 'Gone with  the wind'}

# @api.route('/data')
# def viewdata():
#     data = get_contact()
#     response = jsonify(data)
#     print(response)
#     return render_template('index.html', data = data)

@api.route('/books', methods = ['POST'])
@token_required
def add_book(current_user_token):
    title = request.json['title']
    author = request.json['author']
    publisher = request.json['publisher']
    language = request.json['language']
    genre = request.json['genre']
    print_length = request.json['print_length']
    year = request.json['year']
    isbn = request.json['isbn']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Books(title, author, publisher, language, genre, print_length, year, isbn, user_token = user_token )

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books', methods = ['GET'])
@token_required
def get_book(current_user_token):
    a_user = current_user_token.token
    books = Books.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_book_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        book = Books.query.get(id)
        response = book_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE endpoint
@api.route('/books/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
    book = Books.query.get(id) 
    book.title = request.json['title']
    book.author = request.json['author']
    book.publisher = request.json['publisher']
    book.language = request.json['language']
    book.genre = request.json['genre']
    book.print_length = request.json['print_length']
    book.year = request.json['year']
    book.isbn = request.json['isbn']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)


# DELETE car ENDPOINT
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Books.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)