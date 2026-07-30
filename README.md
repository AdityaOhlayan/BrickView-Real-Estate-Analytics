# BrickView – Real Estate Analytics Platform
BrickView is a mini project developed using Python and Streamlit to analyze real estate data through interactive dashboards, SQL queries, CRUD operations, and advanced filtering.

## Features
- Interactive analytics dashboard
- Property sales and listing insights
- SQL query execution
- CRUD operations for database management
- Property filtering and search
- Interactive Plotly visualizations
- SQLite database integration

## Tech Stack
- Python
- Streamlit
- SQLite
- Pandas
- Plotly

## Dataset

The application includes sample data consisting of:

- 500 Property Listings
- 380 Property Sales
- 380 Buyers
- 15 Real Estate Agents

Project Structure
BrickView/
│── app.py
│── load_db.py
│── generate_data.py
│── queries.py
│── requirements.txt
│── README.md
│── brickview.db


Installation


pip install -r requirements.txt
python load_db.py
python -m streamlit run app.py

Author Aditya Ohlayan

Git Commit Message

Initial commit: BrickView Real Estate Analytics Platform
