import streamlit as st
import json
import time
import pandas as pd
import random

# Load library from file (if available)
def load_library():
    try:
        with open("library.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save library to file
def save_library(library):
    with open("library.json", "w") as file:
        json.dump(library, file, indent=4)

# Load books
library = load_library()

# Get recommendations based on genre
def get_recommendations(genre):
    recommendations = {
        "Fiction": ["The Great Gatsby", "1984", "To Kill a Mockingbird"],
        "Non-Fiction": ["Sapiens", "Educated", "The Wright Brothers"],
        "Fantasy": ["Harry Potter", "The Hobbit", "The Name of the Wind"],
        "Mystery": ["Gone Girl", "Sherlock Holmes", "The Girl with the Dragon Tattoo"],
        "Science Fiction": ["Dune", "Ender's Game", "The Martian"]
    }
    return recommendations.get(genre, ["No recommendations available."])

# Sidebar navigation
st.sidebar.title("📚 Library Manager")
option = st.sidebar.radio("Navigate", ["🏠 Home", "➕ Add Book", "❌ Remove Book", "🔍 Search Book", "📖 View Library", "📊 Statistics", "🎯 Reading Goal", "📑 Export Library", "🚪 Exit"])

# Home Page
if option == "🏠 Home":
    st.title("📖 Welcome to Your Library Manager!")
    st.subheader("Your personal digital bookshelf, now smarter and easier to manage!")
    st.write("🔹 Effortlessly add, remove, and search for books.\n")
    st.write("🔹 Track your reading progress and set goals.\n")
    st.write("🔹 Get personalized book recommendations.\n")
    st.write("📚 Start managing your library now and never lose track of your favorite reads again!")

# Add Book
elif option == "➕ Add Book":
    st.header("➕ Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1900, max_value=3000, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Read")
    progress = st.slider("Reading Progress (%)", 0, 100, 0)
    rating = st.slider("Rate this book (1-5 stars)", 1, 5, 3)
    
    if genre:
        st.subheader("📚 Recommended Books for this Genre:")
        recommendations = get_recommendations(genre)
        for book in recommendations:
            st.write(f"- {book}")
    
    if st.button("Add Book"):
        if title and author and genre:
            library.append({"Title": title, "Author": author, "Year": year, "Genre": genre, "Read": read_status, "Progress": progress, "Rating": rating})
            save_library(library)
            st.success(f"✅ '{title}' added successfully!")
        else:
            st.error("❌ Please fill all fields.")

# Remove Book
elif option == "❌ Remove Book":
    st.header("🗑 Remove a Book")
    titles = [book["Title"] for book in library]
    if titles:
        book_to_remove = st.selectbox("Select a book to remove", titles)
        if st.button("Remove Book"):
            library = [book for book in library if book["Title"] != book_to_remove]
            save_library(library)
            st.success(f"✅ '{book_to_remove}' removed!")
    else:
        st.info("📌 No books available.")

# Search Book
elif option == "🔍 Search Book":
    st.header("🔍 Search a Book")
    query = st.text_input("Enter book title or author")
    if st.button("Search"):
        results = [book for book in library if query.lower() in book["Title"].lower() or query.lower() in book["Author"].lower()]
        if results:
            for book in results:
                st.write(f"📖 **{book['Title']}** by {book['Author']} ({book['Year']}) - {book['Genre']} - {'✔ Read' if book['Read'] else '❌ Unread'} - {book['Progress']}% Completed - ⭐ {book['Rating']}/5")
        else:
            st.warning("❌ No books found.")

# View Library
elif option == "📖 View Library":
    st.header("📚 Your Book Collection")
    if library:
        df = pd.DataFrame(library)
        sort_by = st.selectbox("Sort by", ["Title", "Author", "Year", "Rating"])
        df_sorted = df.sort_values(by=sort_by).reset_index(drop=True)
        df_sorted.index += 1  # Start serial number from 1
        df_sorted.index.name = "S.No"  # Label the index column
        st.dataframe(df_sorted)
    else:
        st.info("📌 No books available.")


# Statistics
elif option == "📊 Statistics":
    st.header("📊 Library Statistics")
    total_books = len(library)
    read_books = len([book for book in library if book["Read"]])
    avg_progress = sum(book["Progress"] for book in library) / total_books if total_books > 0 else 0
    most_read_genre = max(set([book["Genre"] for book in library]), key=[book["Genre"] for book in library].count) if library else "N/A"
    st.metric("Total Books", total_books)
    st.metric("Books Read", read_books)
    st.metric("Average Reading Progress", f"{avg_progress:.2f}%")
    st.metric("Most Read Genre", most_read_genre)

# Reading Goal
elif option == "🎯 Reading Goal":
    st.header("🎯 Set Your Reading Goal")
    goal = st.number_input("Set a yearly reading goal", min_value=0, step=1)
    books_read = len([book for book in library if book["Read"]])
    st.metric("Goal Progress", f"{books_read}/{goal} books read")

# Export Library
elif option == "📑 Export Library":
    st.header("📑 Export Your Library")
    if st.button("Download as CSV"):
        df = pd.DataFrame(library)
        df.to_csv("library_export.csv", index=False)
        st.download_button(label="Download CSV", data=df.to_csv(index=False), file_name="library_export.csv", mime="text/csv")
        st.success("✅ Library exported successfully!")

# Exit
elif option == "🚪 Exit":
    st.header("🚪 Exit Library")
    if st.button("Exit"):
        save_library(library)
        st.success("✅ Library saved. Goodbye! 👋")
        st.rerun()

st.sidebar.write("📌 Use the sidebar to navigate different sections.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: ;'>© 2025 Library Manager | Developed by Usman Naseem❤️</p>", unsafe_allow_html=True)