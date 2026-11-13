# GenAI_for_sql
# GenAI for SQL – Text-to-SQL Assistant

## Project Overview
GenAI for SQL is an AI-powered Text-to-SQL application that converts natural language questions into SQL queries using Google Gemini API.

Users can ask questions in simple English, and the application generates SQL queries, executes them on an SQLite database, and displays the results.

## Features
- Converts natural language into SQL queries.
- Uses Google Gemini API for SQL generation.
- Connects to an SQLite database.
- Automatically retrieves database schema.
- Executes SQL queries and displays results.
- Interactive console for continuous questions.
- Supports commands such as `schema`, `quit`, and `exit`.
- Handles errors gracefully.
- Restricts generated queries to SELECT statements.

## Technologies Used
- Python
- Google Gemini API
- SQLite
- Google GenAI SDK
- Python-dotenv
- Tabulate

## Project Structure

```text
GenAI_for_sql/
│
├── create_db.py
├── text_to_sql.py
├── check_models.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Database Schema

**Customers Table**
- id
- name
- email
- city

**Orders Table**
- id
- customer_id
- product
- amount
- order_date

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/HarshiniGanagala/GenAI_for_sql.git
```

2. Navigate to the project folder:

```bash
cd GenAI_for_sql
```

3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate the virtual environment (Windows):

```bash
venv\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Create a `.env` file in the project folder and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

**Important:** Never upload your actual API key to GitHub.

## Run the Project

First, create the sample database:

```bash
python create_db.py
```

Then start the Text-to-SQL assistant:

```bash
python text_to_sql.py
```

## Example Usage

**User Question:**
```text
Show all customers from Hyderabad
```

**Generated SQL:**
```sql
SELECT * FROM customers
WHERE city = 'Hyderabad'
LIMIT 50;
```

**Other Example Questions:**
- Show total sales by customer.
- Count the total number of orders.
- Find customers from Hyderabad.
- Show the most expensive products.

## Future Enhancements
- Develop a web-based user interface.
- Add support for more database systems.
- Improve SQL generation accuracy.
- Add data visualization and analytics.

## Author
**Harshini Ganagala**

GitHub: https://github.com/HarshiniGanagala
