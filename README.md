# CineList – Movie Watchlist App

## How to run

1. Unzip and open terminal in the `CineList/` folder.
2. Create a virtual environment and install dependencies:
   - `python -m venv venv`
   - `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)
   - `pip install -r requirements.txt`
3. Make sure MySQL is running and your `core/settings.py` is configured for MySQL.
4. Run: `python manage.py runserver`
5. Go to http://127.0.0.1:8000/ in the browser.