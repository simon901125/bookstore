# Froggy Bookstore - Project Overview

A web-based bookstore application featuring a "Curated Archive" design aesthetic, localized for Traditional Chinese and Japanese audiences.

## Project Structure

- **`server.py`**: The main backend server implemented using Python's `http.server`. It serves static files and provides a JSON API for member registration and wishlist management.
- **`python/`**: Serves as the database layer, containing JSON files for books, members, and user-saved items.
- **`bookstore_JS/`**: Contains the frontend business logic, including authentication (`auth.js`) and book-related interactions.
- **`window/`**: The primary frontend directory containing Traditional Chinese (TC) HTML pages.
- **`window_jp/`**: The Japanese (JP) localized frontend directory.
- **`bookstore_DB/`**: Contains SQL schema definitions (`bookstoreDB.sql`) and book cover assets. Note that the current implementation uses JSON storage, but the SQL files define the intended relational structure.
- **`archival_modern/DESIGN.md`**: Documentation for "The Curated Archive" design system, detailing the project's typography, color palette, and UI philosophy.

## Technology Stack

- **Backend**: Python 3 (Standard Library: `http.server`, `json`, `pathlib`).
- **Frontend**: HTML5, Vanilla JavaScript, CSS.
- **Data Storage**: JSON-based flat files (located in `/python`).
- **Design System**: Custom "Editorial" style focusing on typography and whitespace.

## Building and Running

### Prerequisites
- Python 3.x

### Running the Application
To start the backend server and serve the frontend:
```bash
python server.py
```
The application will be available at `http://localhost:8000/`.

### Development Notes
- **API Endpoints**: 
  - `POST /api/register`: Register a new member.
  - `POST /api/saving-books`: Add a book to a member's wishlist.
  - `DELETE /api/saving-books`: Remove a book from the wishlist.
- **Authentication**: Current authentication is a prototype implementation where credentials are validated client-side against `member.json` for simplicity.
- **Internationalization**: The project maintains two separate directory trees for TC (`/window`) and JP (`/window_jp`).

## Coding Conventions

- **Design First**: Adhere to the "No-Line Rule" described in `DESIGN.md`—use background shifts instead of 1px borders for sectioning.
- **Data Integrity**: When modifying `server.py`, ensure that JSON updates are performed atomically using temporary files (as currently implemented in `save_members`).
- **Naming**: Frontend assets and directories use the `froggy_` prefix for consistency.
