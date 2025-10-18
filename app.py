import streamlit as st
import sqlite3
import pandas as pd

# Database setup
conn = sqlite3.connect('library.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                year INTEGER,
                status TEXT)''')
conn.commit()

st.title("📚 Library Management System")

menu = ["Add Book", "View Books", "Update Status", "Delete Book"]
choice = st.sidebar.selectbox("Menu", menu)

# Add a book
if choice == "Add Book":
    st.subheader("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author Name")
    year = st.number_input("Year Published", min_value=1900, max_value=2100, step=1)
    status = st.selectbox("Status", ["Available", "Issued"])
    if st.button("Add Book"):
        c.execute("INSERT INTO books (title, author, year, status) VALUES (?, ?, ?, ?)", 
                  (title, author, year, status))
        conn.commit()
        st.success(f"Book '{title}' added successfully!")

# View books
elif choice == "View Books":
    st.subheader("View All Books")
    data = pd.read_sql("SELECT * FROM books", conn)
    st.dataframe(data)

# Update book status
elif choice == "Update Status":
    st.subheader("Update Book Status")
    book_id = st.number_input("Enter Book ID", min_value=1)
    new_status = st.selectbox("New Status", ["Available", "Issued"])
    if st.button("Update"):
        c.execute("UPDATE books SET status=? WHERE id=?", (new_status, book_id))
        conn.commit()
        st.success(f"Book ID {book_id} status updated to {new_status}!")

# Delete book
elif choice == "Delete Book":
    st.subheader("Delete a Book Record")
    book_id = st.number_input("Enter Book ID to Delete", min_value=1)
    if st.button("Delete"):
        c.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
        st.warning(f"Book ID {book_id} deleted!")

conn.close()
