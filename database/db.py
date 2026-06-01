import sqlite3

# Connect database
conn = sqlite3.connect("fitness.db")

# Create cursor
c = conn.cursor()

# Create users table
c.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT
)
""")

# Create BMI history table
c.execute("""
CREATE TABLE IF NOT EXISTS bmi_history(
    username TEXT,
    bmi REAL,
    goal TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS workouts(
    username TEXT,
    exercise TEXT,
    sets INTEGER,
    reps INTEGER,
    duration INTEGER
)
""")

# Save changes
conn.commit()

# Close connection
conn.close()

print("Database Created Successfully")