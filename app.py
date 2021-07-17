from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
from tinydb import TinyDB, Query
from habanero import Crossref
import json

# configuration
DEBUG = True

# a plain file database for the books
db = TinyDB('books_db.json')
db_idx = Query()

# # a fast way to create the database
# db.truncate() # clean the database file
# print(db.all())
# db.insert({'id': uuid.uuid4().hex, 'title': 'On the Road',
#           'author': 'Jack Kerouac', 'read': True})
# db.insert({'id': uuid.uuid4().hex, 'title': 'Harry Potter and the Philosopher\'s Stone',
#           'author': 'J. K. Rowling', 'read': False})
# db.insert({'id': uuid.uuid4().hex, 'title': 'Green Eggs and Ham',
#           'author': 'Dr. Seuss', 'read': True})

# # predefined list of book
# BOOKS = []
# for item in db:
#     BOOKS.append(item)
#     print(item)

# print(db.all())

# predefined list of papers
SEARCHPAPERS = []

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/ping', methods=['GET'])
# sanity check route
def ping_pong():
    return jsonify('pong!')


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        db.insert({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        # BOOKS.append({
        #     'id': uuid.uuid4().hex,
        #     'title': post_data.get('title'),
        #     'author': post_data.get('author'),
        #     'read': post_data.get('read')
        # })
        response_object['message'] = 'Book added!'
    else:
        BOOKS = []
        for item in db:
            BOOKS.append(item)
            # print(item)
        response_object['books'] = BOOKS
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        db.update({
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        }, db_idx.id == book_id)
        # remove_book(book_id)
        # db.insert({
        #     'id': uuid.uuid4().hex,
        #     'title': post_data.get('title'),
        #     'author': post_data.get('author'),
        #     'read': post_data.get('read')
        # })

        # BOOKS.append({
        #     'id': uuid.uuid4().hex,
        #     'title': post_data.get('title'),
        #     'author': post_data.get('author'),
        #     'read': post_data.get('read')
        # })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


def remove_book(book_id):
    db.remove(db_idx.id == book_id)
    # for book in BOOKS:
    #     if book['id'] == book_id:
    #         BOOKS.remove(book)
    #         return True
    return False


def search_crossref(stxt):
    cr = Crossref()
    # possible error due to network problem
    try:
        xcr = cr.works(query=stxt)
    except:
        return
    # now we fetch the essential data from each item and return them as a json string
    papers = []
    SEARCHPAPERS.clear()
    for npaper in range(xcr['message']['items-per-page']):
        # for each item, we only fetch
        #    the first author
        #    doi (primary key)
        #    title
        #    journal
        #    year
        xitem = xcr['message']['items'][npaper]
        paper = {}
        paper['doi'] = xitem['DOI']
        paper['title'] = xitem['title'][0]
        try:
            xauthors = xitem['author']
            paper['au1'] = xauthors[0]['given'] + " " + xauthors[0]['family']
        except:
            paper['au1'] = 'NA'
        try:
            paper['journal'] = xitem['container-title'][0]
        except:
            paper['journal'] = 'NA'
        try:
            paper['year'] = xitem['published']['date-parts'][0][0]
        except:
            paper['year'] = 'NA'
        papers.append(paper)
        SEARCHPAPERS.append(paper)
    # set the global list SEARCHPAPERS
    # SEARCHPAPERS = papers
    # debug
    print(json.dumps(SEARCHPAPERS, indent=4))
    # return a list of search results
    return papers


@app.route('/search_paper', methods=['POST', 'GET'])
def search_paper():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        stxt = post_data.get('search_string')
        papers = search_crossref(stxt)
        response_object['papers'] = papers
    else:
        response_object['papers'] = SEARCHPAPERS
        # debug
        print(json.dumps(SEARCHPAPERS, indent=4))
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
