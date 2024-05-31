from datetime import datetime, timezone
from flask import Flask, request, jsonify
import os
import psycopg2
import json
from dotenv import load_dotenv
import requests
from psycopg2 import pool

create_songs_table = (" CREATE TABLE IF NOT EXISTS songs (id SERIAL PRIMARY KEY, song TEXT, composer TEXT, writer TEXT, artist TEXT);")
insert_song = "INSERT INTO songs (song, writer,composer, artist) VALUES (%s, %s,%s, %s) RETURNING id;"
get_songee= "select * from songs where song = %s"

load_dotenv()

app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")

#conn = psycopg2.connect(database_url)
db_pool = psycopg2.pool.SimpleConnectionPool(1, 20, database_url)

@app.post("/myapi/songs")
def create_song():
    data = request.get_json()
    song = data['song']
    writer = data['writer']
    composer = data['artist']
    artist = "محمد عبده"
    conn = db_pool.getconn()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(create_songs_table)
                cur.execute(insert_song, (song,writer, composer,artist))
                song_id = cur.fetchone()[0]
        return {"id": song_id, "song": song, "writer": writer,"composer":composer, "artist": artist}, 201
    finally:
        db_pool.putconn(conn)

@app.get("/myapi/songs")
def get_song():
    song = request.args.get('song')
    conn = db_pool.getconn()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(get_songee, (song,))
                song = cur.fetchone()
        if song is None:
            return {"message": "Song not found"}, 404
        return {"id": song[0], "song": song[1], "writer": song[3], "composer": song[2], "artist": song[4]}, 200
    finally:
        db_pool.putconn(conn)

if __name__ == '__main__':
    app.run(debug=True)
