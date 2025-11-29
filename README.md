Pair Programming API – Backend Prototype

This repository contains a small FastAPI backend built for a real-time pair-programming prototype.
The idea is simple: two users can join the same room and edit code at the same time, and the changes sync live through WebSockets. A mocked autocomplete endpoint is also included as part of the assignment.

This is not meant to be a production-ready system — just a working prototype that covers the required functionality.

## What’s Included

Create and join rooms

Real-time code updates using WebSockets

Basic mocked autocomplete endpoint

PostgreSQL storage for room state

Clean and minimal FastAPI structure

## Tech Used

Python / FastAPI

WebSockets

PostgreSQL

SQLAlchemy

Pydantic

Nothing fancy — just the essentials to make the backend work.

## Project Structure (Simplified)
backend/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── websocket_handler.py
├── init_db.py
├── routers/
│   ├── rooms.py
│   └── autocomplete.py
└── services/
    ├── room_service.py
    └── autocomplete_service.py


Everything is broken into API routes and small service files to keep things readable.

## How to Run It
1. Create a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

2. Install dependencies
pip install -r requirements.txt

3. Set up PostgreSQL

Create a database:

CREATE DATABASE pairprogramming_db;


Update your .env:

DATABASE_URL=postgresql://user:password@localhost:5432/pairprogramming_db

4. Initialize DB
python init_db.py

5. Start the server
uvicorn main:app --reload


Runs on:
http://localhost:8000

Swagger docs:
http://localhost:8000/docs

## API Overview
Create Room

POST /rooms

Returns a new room ID.

Autocomplete

POST /autocomplete

Returns a static/mock suggestion.
Used only for demo purposes.

WebSocket Collaboration

ws://localhost:8000/ws/{room_id}

Connect from two different clients and both will see each other's updates immediately.

I tested this using Postman's WebSocket client.

## How the System Works (Short Explanation)

When a room is created, it’s inserted into the DB.

Users join via WebSocket using the room ID.

Every edit is broadcast to all other active connections.

Room state is also stored in the database for persistence.

The autocomplete endpoint returns a simple rule-based suggestion — nothing fancy.

## Current Limitations

This is a prototype, so it has a few intentional limitations:

No authentication

Last-write-wins (no conflict resolution)

In-memory WebSocket connection tracking

Autocomplete is mocked

No reconnect logic or typing indicators

These are known constraints and would be the first things to improve if this were extended.

## Possible Enhancements

If I had more time, I would improve:

Better sync algorithm (OT or CRDT)

Real AI autocomplete

Persistent user identities

Multiple files per room

Undo/redo or code history

Redis-based WebSocket scaling

Cleaner UI demo

## Notes

This backend is built only for assignment/demo purposes.

The focus was on clarity, basic functionality, and structure.

PostgreSQL credentials should always be stored securely.

## Author

Abhinay — Tredence Assignment