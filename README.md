Authentication API Documentation
    This is a complete authentication system implemented in FastAPI , alembic, jwt, sqlite and many more..

GETTING STARTED:
    
    1. Clone the repo  $ git clone https://github.com/kabin007/authyy.git'

    2. Install libraries $ pip install -r requirements.txt

    3.Make a .env file in the root dir with your details looking at the env.example file

    4.Make migrations $ alemebic revision --autogenerate -m "make sql models"

    5.Apply migration $ alembic upgrade head

    6. Run the server $ python3 run.py

    7. Go the 0.0.0.0:8000/docs and test the endpoints


Base URL:

/auth

Overview

This set of endpoints handles user authentication and account management, including:

    User registration (signup)

    Login and JWT token issuance

    Fetching current user details

    Listing all registered users

    Refreshing tokens

    Password reset workflow

1. Register a New User

POST /auth/users
Description

Registers a new user with the provided username, email, and password.
Request Body

Schema: UserCreate

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "strongpassword123"
}

Validation:

    username: Required, string, unique in DB.

    email: Required, valid email format, unique in DB.

    password: Required, string, should meet password policy (min length, complexity).

Response

201 Created

{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2025-08-08T10:30:00Z"
}

409 Conflict

{
  "detail": "Email already registered"
}

2. Login

POST /auth/login
Description

Authenticates the user and returns access and refresh tokens.
Request Body

Schema: UserLogin

{
  "email": "john@example.com",
  "password": "strongpassword123"
}

Response

200 OK

{
  "tokens": {
    "access": {
      "access_token": "eyJhbGciOiJIUzI1NiIs...",
      "token_type": "bearer"
    },
    "refresh": {
      "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
      "jti": "abcd1234",
      "expiry": "2025-08-09T10:30:00Z"
    }
  },
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}

401 Unauthorized

{
  "detail": "Invalid email or password"
}

3. Get Current User Info

GET /auth/me
Description

Retrieves information about the currently authenticated user (requires a valid access token).
Headers

Authorization: Bearer <access_token>

Response

200 OK

{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2025-08-08T10:30:00Z"
}

401 Unauthorized

{
  "detail": "Not authenticated"
}

4. Get All Users

GET /auth/users
Description

Fetches a list of all registered users.
Requires admin-level permissions (if implemented).
Response

200 OK

[
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2025-08-08T10:30:00Z"
  },
  {
    "id": 2,
    "username": "jane_smith",
    "email": "jane@example.com",
    "created_at": "2025-08-08T11:00:00Z"
  }
]

5. Refresh Tokens

POST /auth/tokens
Description

Generates a new access token using a valid refresh token.
Headers

Authorization: Bearer <refresh_token>

Response

200 OK

{
  "tokens": {
    "access": {
      "access_token": "newAccessToken123",
      "token_type": "bearer"
    },
    "refresh": {
      "refresh_token": "newRefreshToken456",
      "jti": "efgh5678",
      "expiry": "2025-08-09T10:30:00Z"
    }
  },
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}

401 Unauthorized

{
  "detail": "Missing or invalid refresh token"
}

6. Forgot Password

POST /auth/forgot-password
Description

Sends a password reset link to the provided email if the account exists.
Request Body

Schema: ForgotPasswordRequest

{
  "email": "john@example.com"
}

Response

200 OK

{
  "message": "If that email exists, Password reset link has been sent."
}

7. Reset Password

POST /auth/reset-password
Description

Resets the user's password using a valid reset token.
Request Body

Schema: ResetPasswordRequest

{
  "token": "secureToken123",
  "password": "newStrongPassword456"
}

Response

200 OK

{
  "message": "Password successfully reset."
}

400 Bad Request

{
  "detail": "Invalid or expired token."
}

Authentication Flow

    Signup → /auth/users to create an account.

    Login → /auth/login to get access & refresh tokens.

    Access Protected Routes → Use Authorization: Bearer <access_token>.

    Refresh Access Token → /auth/tokens with refresh token.

    Forgot Password → /auth/forgot-password to request reset link.

    Reset Password → /auth/reset-password with valid token
