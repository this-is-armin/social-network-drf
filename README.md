# Social Network API

This project is a backend API for a social network application. It is built with Django and Django REST Framework and provides endpoints for user accounts, posts, comments, and follow relationships.

The API is versioned (`v1`) to support multiple clients (e.g. web frontend, mobile apps) independently. This makes it scalable and adaptable for future versions or different platforms.

---

## 📦 Installing

### Run the following commands:

    pip install -r requirements.txt

    python manage.py migrate

    python manage.py runserver

### Open your browser and go to:

    localhost:8000

---

## 🔗 API Endpoints

### Token Authentication

- POST /api/token/ – Get access and refresh tokens
- POST /api/token/refresh/ – Refresh access token

### Accounts (/api/v1/accounts/)

- GET / – List all users
- POST /register/ – Register a new user
- GET /```<username>```/ – View user profile
- POST /```<username>```/follow/ – Follow a user
- DELETE /```<username>```/unfollow/ – Unfollow a user
- GET /```<username>```/followers/ – List followers
- GET /```<username>```/following/ – List following
- GET /```<username>```/posts/ – List user's posts

### Posts (/api/v1/posts/)

- GET / – List all posts
- POST / – Create a new post
- GET /```<pk>```/ – View post detail
- PUT /```<pk>```/ Update a post
- PATCH /```<pk>```/ Partially update a post
- DELETE /```<pk>```/ Delete a post
- GET/POST /```<pk>```/comments/ – List or create comments on a post
- GET /```<post_pk>/comments```/```<comment_pk>```/ – View comment detail
