import csv
import sqlite3

# # User
# con = sqlite3.connect('/Users/valentinabelezak/Dev/API YaMBL/db.sqlite3')
# cursor = con.cursor()
#
# r_file = open("/Users/valentinabelezak/Dev/API YaMBL/data/users.csv")
# file_reader = csv.DictReader(r_file, delimiter=',')
# to_db = [(i['id'], i['username'], i['email'], i['role'], i['description'], i['first_name'], i['last_name']) for i in
#          file_reader]
#
# cursor.executemany(
#     'INSERT INTO "api_user" ("id", "username", "email", "role", "bio", "first_name", "last_name", "password", '
#     '"is_superuser", "is_active", "is_staff", "confirmation_code") VALUES(?, ?, ?, ?, ?, ?, ?, "qw123", "0", '
#     '"1", "0", NULL);', to_db)
#
# cursor.execute("SELECT * FROM api_user")
# print(cursor.fetchall())
# con.commit()
# con.close()

# Category
# con = sqlite3.connect('/Users/valentinabelezak/Dev/API YaMBL/db.sqlite3')
# cursor = con.cursor()
#
# r_file = open("/Users/valentinabelezak/Dev/API YaMBL/data/category.csv")
# file_reader = csv.DictReader(r_file, delimiter=',')
# to_db = [(i['id'], i['name'], i['slug']) for i in file_reader]
#
# cursor.executemany(
#     'INSERT INTO api_category (id, name, slug) VALUES (?, ?, ?);', to_db)
#
# cursor.execute("SELECT * FROM api_category")
# print(cursor.fetchall())
# con.commit()
# con.close()


# Genre
# con = sqlite3.connect('/Users/valentinabelezak/Dev/API YaMBL/db.sqlite3')
# cursor = con.cursor()
#
# r_file = open("/Users/valentinabelezak/Dev/API YaMBL/data/genre.csv")
# file_reader = csv.DictReader(r_file, delimiter=',')
# to_db = [(i['id'], i['name'], i['slug']) for i in file_reader]
#
# cursor.executemany(
#     'INSERT INTO api_genre (id, name, slug) VALUES (?, ?, ?);', to_db)
#
# cursor.execute("SELECT * FROM api_genre")
# print(cursor.fetchall())
# con.commit()
# con.close()


# # Titles
# con = sqlite3.connect('/Users/valentinabelezak/Dev/API YaMBL/db.sqlite3')
# cursor = con.cursor()
#
# r_file = open("/Users/valentinabelezak/Dev/API YaMBL/data/titles.csv")
# file_reader = csv.DictReader(r_file, delimiter=',')
# to_db = [(i['id'], i['name'], i['year'], i['category']) for i in file_reader]
#
# cursor.executemany(
#     'INSERT INTO api_titles (id, name, year, category_id) VALUES (?, ?, ?, ?);', to_db)
#
# cursor.execute("SELECT * FROM api_titles")
# print(cursor.fetchall())
# con.commit()
# con.close()


# # GenreTitle
# con = sqlite3.connect('/Users/valentinabelezak/Dev/API YaMBL/db.sqlite3')
# cursor = con.cursor()
#
# r_file = open("/Users/valentinabelezak/Dev/API YaMBL/data/genre_title.csv")
# file_reader = csv.DictReader(r_file, delimiter=',')
# to_db = [(i['id'], i['title_id'], i['genre_id']) for i in file_reader]
#
# cursor.executemany(
#     'INSERT INTO api_titles_genre (id, titles_id, genre_id) VALUES (?, ?, ?);', to_db)
#
# cursor.execute("SELECT * FROM api_titles_genre")
# print(cursor.fetchall())
# con.commit()
# con.close()


# # GenreTitle
# con = sqlite3.connect('/Users/valentinabelezak/Dev/API YaMBL/db.sqlite3')
# cursor = con.cursor()
#
# r_file = open("/Users/valentinabelezak/Dev/API YaMBL/data/review.csv")
# file_reader = csv.DictReader(r_file, delimiter=',')
# to_db = [(i['id'], i['title_id'], i['text'], i['author'], i['score'], i['pub_date']) for i in file_reader]
#
# cursor.executemany(
#     'INSERT INTO api_review (id, title_id_id, text, author_id, score, pub_date) VALUES (?, ?, ?, ?, ?, ?);', to_db)
#
# cursor.execute("SELECT * FROM api_review")
# print(cursor.fetchall())
# con.commit()
# con.close()

# Comments
con = sqlite3.connect('/Users/valentinabelezak/Dev/API YaMBL/db.sqlite3')
cursor = con.cursor()

r_file = open("/Users/valentinabelezak/Dev/API YaMBL/data/comments.csv")
file_reader = csv.DictReader(r_file, delimiter=',')
to_db = [(i['id'], i['review_id'], i['text'], i['author'], i['pub_date']) for i in file_reader]

cursor.executemany(
    'INSERT INTO api_comments (id, review_id_id, text, author_id, pub_date) VALUES (?, ?, ?, ?, ?);', to_db)

cursor.execute("SELECT * FROM api_comments")
print(cursor.fetchall())
con.commit()
con.close()