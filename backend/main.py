from fastapi import FastAPI 
import sqlite3

app = FastAPI()

def get_db():
    conn=sqlite3.connect("test.db")
    return conn 
@app.get("/")
def get_data():
    return {"message": "FastAPI CI Project is running"}

@app.post("/users/{user}")
def post_data(user:str):
    conn=get_db()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (name TEXT)")
    cursor.execute("INSERT INTO users VALUES (?)", (name,))
    conn.commit()
    conn.close()
    return {"user": name}



