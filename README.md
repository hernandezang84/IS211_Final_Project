
# Blog Application

## Overview

This Blog Application is a web-based platform that allows users to create, edit, and delete blog posts. The application is built using the Flask framework for Python and uses SQLite as its database backend.

## How it Works

Users can log in to the application with a username and password. If the user does not exist in the database, the application automatically creates a new user with the provided credentials. This feature is intended for demonstration purposes and simplifies the process of user management. In a production environment, you would want to implement a more secure user registration process.

Once logged in, users can access the dashboard where they can see a list of their posts displayed in reverse chronological order. Users can add new posts, edit existing ones, or delete them.

## Model Details

The application uses a simple model with two tables: `users` and `posts`. The `users` table contains user information, including usernames and passwords. The `posts` table contains the blog posts, each associated with a user through a foreign key.

Passwords are currently stored in plain text for simplicity. This is not a secure practice, and a real-world application would need to implement hashed passwords and possibly other security measures.

The Flask app establishes a connection to the SQLite database on each request and uses parameterized SQL queries to prevent SQL injection attacks. Upon closing the application or ending the session, the database connection is properly terminated.

### Application Structure

- `blogapp.py`: The main Flask application file.
- `blog.db`: SQLite database containing the `users` and `posts` tables.
- `templates`: Folder containing HTML templates for rendering views.

To run the application, use the following command:
```
python blogapp.py
```
Please note that this application is intended for educational purposes and should not be used as-is in a production environment.

