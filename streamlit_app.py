import streamlit as st
import requests

# Configuration
FASTAPI_BASE_URL = "http://localhost:8000"  # Assuming your FastAPI app runs on port 8000

st.set_page_config(page_title="Library Management System", layout="centered")

st.title("📚 Library Management System")

# --- Helper Functions ---
def signup_user(name, email, password, role):
    url = f"{FASTAPI_BASE_URL}/users/signup"
    data = {
        "name": name,
        "email": email,
        "password": password,
        "role": role
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get("detail")
            st.error(f"Signup failed: {detail}")
        except (ValueError, AttributeError):
            st.error(f"Signup failed with status code {e.response.status_code}. Please try again.")
        return None
    except requests.exceptions.RequestException:
        st.error("Could not connect to the server. Please ensure the backend is running.")
        return None

def login_user(email, password):
    url = f"{FASTAPI_BASE_URL}/users/login"
    data = {"email": email, "password": password}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get("detail", "Invalid credentials or server error.")
            st.error(f"Login failed: {detail}")
        except (ValueError, AttributeError):
            st.error(f"Login failed with status code {e.response.status_code}. Please try again.")
        return None
    except requests.exceptions.RequestException:
        st.error("Could not connect to the server. Please ensure the backend is running.")
        return None

def logout_user():
    st.session_state.clear()
    st.success("Logged out successfully!")
    st.rerun()

def get_auth_headers():
    """Returns the authorization headers for API requests."""
    return {"Authorization": f"Bearer {st.session_state['access_token']}"}

def get_all_books():
    """Fetches all books from the library."""
    url = f"{FASTAPI_BASE_URL}/books"
    try:
        response = requests.get(url, headers=get_auth_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch books: {e}")
        return []

def request_book(book_id):
    """Sends a request to book a specific book."""
    url = f"{FASTAPI_BASE_URL}/bookings/"
    data = {"book_id": book_id}
    try:
        response = requests.post(url, json=data, headers=get_auth_headers())
        response.raise_for_status()
        st.success("Book requested successfully! It is now pending approval.")
        return response.json()
    except requests.exceptions.HTTPError as e:
        detail = e.response.json().get("detail", "Failed to request book.")
        st.error(detail)
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to request book: {e}")
        return None

def get_my_bookings():
    """Fetches the current user's booking history."""
    url = f"{FASTAPI_BASE_URL}/bookings/me"
    try:
        response = requests.get(url, headers=get_auth_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch your bookings: {e}")
        return []

def get_all_bookings():
    """Fetches all bookings (incharge only)."""
    url = f"{FASTAPI_BASE_URL}/bookings/"
    try:
        response = requests.get(url, headers=get_auth_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch all bookings: {e}")
        return []

def update_booking_status(booking_id, status):
    """Updates the status of a booking (incharge only)."""
    url = f"{FASTAPI_BASE_URL}/bookings/{booking_id}/status"
    data = {"status": status}
    try:
        response = requests.put(url, json=data, headers=get_auth_headers())
        response.raise_for_status()
        st.success(f"Booking {booking_id} has been {status}.")
        return response.json()
    except requests.exceptions.HTTPError as e:
        detail = e.response.json().get("detail", "Failed to update booking status.")
        st.error(detail)
        return None

def add_book(title, author):
    """Adds a new book to the library (incharge only)."""
    url = f"{FASTAPI_BASE_URL}/books/"
    data = {"title": title, "author": author}
    try:
        response = requests.post(url, json=data, headers=get_auth_headers())
        response.raise_for_status()
        st.success(f"Book '{title}' added successfully.")
        return response.json()
    except requests.exceptions.HTTPError as e:
        detail = e.response.json().get("detail", "Failed to add book.")
        st.error(detail)

def delete_book(book_id):
    """Deletes a book from the library (incharge only)."""
    url = f"{FASTAPI_BASE_URL}/books/{book_id}"
    try:
        response = requests.delete(url, headers=get_auth_headers())
        response.raise_for_status()
        st.success(f"Book {book_id} deleted successfully.")
        return True
    except requests.exceptions.HTTPError as e:
        detail = e.response.json().get("detail", "Failed to delete book.")
        st.error(detail)
        return False

# --- Main UI Logic ---
if "access_token" not in st.session_state:
    st.sidebar.header("Login / Signup")
    choice = st.sidebar.radio("Choose an option:", ["Login", "Signup"])

    if choice == "Signup":
        st.sidebar.subheader("Create a New Account")
        with st.sidebar.form("signup_form"):
            new_name = st.text_input("Name")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            new_role = st.selectbox("Role", ["student", "incharge"])
            signup_button = st.form_submit_button("Signup")

            if signup_button:
                if not (new_name and new_email and new_password and new_role and confirm_password):
                    st.warning("Please fill in all fields for signup.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    user_data = signup_user(new_name, new_email, new_password, new_role)
                    if user_data:
                        st.success(f"Account created for {user_data['name']}! Please login.")
                        st.balloons()

    elif choice == "Login":
        st.sidebar.subheader("Login to Your Account")
        with st.sidebar.form("login_form"):
            login_email = st.text_input("Email")
            login_password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")

            if login_button:
                if login_email and login_password:
                    token_data = login_user(login_email, login_password)
                    if token_data:
                        st.session_state["access_token"] = token_data["access_token"]
                        st.session_state["token_type"] = token_data["token_type"]
                        st.session_state["user_name"] = token_data["user_name"]
                        st.session_state["user_role"] = token_data["user_role"]
                        st.success("Logged in successfully!")
                        st.rerun()
                else:
                    st.warning("Please enter both email and password.")

else:
    # --- Logged-in View ---
    st.sidebar.success(f"Welcome, {st.session_state['user_name']}!")
    st.sidebar.write(f"Role: **{st.session_state['user_role'].capitalize()}**")
    if st.sidebar.button("Logout", use_container_width=True):
        logout_user()

    # --- STUDENT DASHBOARD ---
    if st.session_state["user_role"] == "student":
        st.header("Student Dashboard")
        tab1, tab2 = st.tabs(["📚 All Books", "📖 My Bookings"])

        with tab1:
            st.subheader("Request a Book")
            all_books = get_all_books()
            if all_books:
                # Header
                c1, c2, c3, c4 = st.columns([1, 4, 3, 2])
                c1.write("**ID**")
                c2.write("**Title**")
                c3.write("**Author**")
                c4.write("**Action**")
                st.divider()

                for book in all_books:
                    col1, col2, col3, col4 = st.columns([1, 4, 3, 2])
                    with col1:
                        st.write(book['id'])
                    with col2:
                        st.write(book['title'])
                    with col3:
                        st.write(book['author'])
                    with col4:
                        if book['is_available']:
                            if st.button("Request", key=f"request_{book['id']}", use_container_width=True):
                                if request_book(book['id']):
                                    st.rerun()
                        else:
                            st.info("Booked", icon="🔒")
            else:
                st.info("No books found in the library.")

        with tab2:
            st.subheader("Your Booking History")
            my_bookings = get_my_bookings()
            all_books = get_all_books()  # Fetch all books to map IDs to titles

            if my_bookings and all_books:
                book_map = {book['id']: book for book in all_books}
                display_bookings = []
                for booking in my_bookings:
                    book_info = book_map.get(booking['book_id'])
                    display_bookings.append({
                        "Booking ID": booking['id'],
                        "Book Title": book_info['title'] if book_info else "N/A",
                        "Status": booking['status'],
                        "Requested At": booking['booked_at']
                    })
                st.dataframe(display_bookings, use_container_width=True)
            elif my_bookings:
                st.dataframe(my_bookings, use_container_width=True) # Fallback
            else:
                st.info("You have no booking history.")

    # --- INCHARGE DASHBOARD ---
    elif st.session_state["user_role"] == "incharge":
        st.header("Library Incharge Dashboard")
        tab1, tab2 = st.tabs(["📖 Manage Bookings", "📚 Manage Books"])

        with tab1:
            st.subheader("All User Bookings")
            all_bookings = get_all_bookings()
            if all_bookings:
                c1, c2, c3, c4, c5 = st.columns([1, 2, 3, 2, 3])
                c1.write("**ID**")
                c2.write("**User**")
                c3.write("**Book Title**")
                c4.write("**Status**")
                c5.write("**Actions**")
                st.divider()

                for b in sorted(all_bookings, key=lambda x: x['id'], reverse=True):
                    col1, col2, col3, col4, col5 = st.columns([1, 2, 3, 2, 3])
                    with col1:
                        st.write(b['id'])
                    with col2:
                        st.write(b['user']['name'])
                    with col3:
                        st.write(b['book']['title'])
                    with col4:
                        if b['status'] == 'pending': st.warning("Pending")
                        elif b['status'] == 'approved': st.success("Approved")
                        elif b['status'] == 'returned': st.info("Returned")
                        else: st.error("Rejected")
                    with col5:
                        action_cols = st.columns(3)
                        if b['status'] == 'pending':
                            if action_cols[0].button("Approve", key=f"approve_{b['id']}", use_container_width=True):
                                if update_booking_status(b['id'], "approved"): st.rerun()
                            if action_cols[1].button("Reject", key=f"reject_{b['id']}", use_container_width=True):
                                if update_booking_status(b['id'], "rejected"): st.rerun()
                        elif b['status'] == 'approved':
                            if action_cols[0].button("Return", key=f"return_{b['id']}", use_container_width=True):
                                if update_booking_status(b['id'], "returned"): st.rerun()
            else:
                st.info("No bookings have been made yet.")

        with tab2:
            with st.expander("➕ Add a New Book"):
                with st.form("add_book_form", clear_on_submit=True):
                    new_book_title = st.text_input("Title")
                    new_book_author = st.text_input("Author")
                    if st.form_submit_button("Add Book"):
                        if new_book_title and new_book_author:
                            if add_book(new_book_title, new_book_author): st.rerun()
                        else:
                            st.warning("Please provide both title and author.")

            st.divider()
            st.subheader("Delete a Book")
            all_books = get_all_books()
            if all_books:
                book_to_delete_str = st.selectbox("Select a book to delete:", options=[f"{b['title']} (ID: {b['id']})" for b in all_books])
                if st.button("Delete Book", type="primary"):
                    book_id = int(book_to_delete_str.split('(ID: ')[1][:-1])
                    if delete_book(book_id):
                        st.rerun()
            else:
                st.info("No books found to delete.")