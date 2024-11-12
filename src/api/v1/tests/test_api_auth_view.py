import unittest

from fastapi import HTTPException
from database.database import get_db
from src.api.v1.schemas import user_schemas as _US
from src.api.v1.views import api_user_auth_view as _AV
from src.api.v1.models.user_models import user_info as _UI
from src.api.v1.models.department_models.department_info import Department
from unittest import IsolatedAsyncioTestCase
class TestApiAuthView(IsolatedAsyncioTestCase):

    # For setting up the database in test
    def setUp(self):
        # Get the session by consuming the generator
        self.db = next(get_db())  # This will give you the actual Session object

    def tearDown(self):
        # Close the session explicitly after the test is done
        self.db.close()

    # def test_create_user(self):
    #     # Create a new user
    #     user = _US.UserCreate(username="testuser", email="5oJ4H@example.com", password="testpassword")

    #     # Call the create_user function
    #     _AV.create_user(user, self.db)

    #     # Check if the user was created in the database
    #     user = self.db.query(_UI.User).filter(_UI.User.email == "5oJ4H@example.com").first()
    #     self.assertIsNotNone(user)
    #     self.assertEqual(user.email, "5oJ4H@example.com")

    #     # Clean up after the test
    #     self.db.query(_UI.User).filter(_UI.User.email == "5oJ4H@example.com").delete()
    #     self.db.commit()

    #     # Check if the user was deleted from the database
    #     user = self.db.query(_UI.User).filter(_UI.User.email == "5oJ4H@example.com").first()
    #     self.assertIsNone(user)

    # async def test_login(self):
    #     # Create a new user
    #     user = _US.UserCreate(username="testuser", email="5oJ4H@example.com", password="testpassword")
    #     _AV.create_user(user, self.db)

    #     # Login with the user
    #     user = _US.UserLogin(username="testuser", email="5oJ4H@example.com", password="testpassword")
    #     token = await _AV.login(user, self.db)

    #     # Check if the token was generated
    #     self.assertIsNotNone(token)

    #     # Clean up after the test
    #     self.db.query(_UI.User).filter(_UI.User.email == "5oJ4H@example.com").delete()
    #     self.db.commit()

    #     # Check if the user was deleted from the database
    #     user = self.db.query(_UI.User).filter(_UI.User.email == "5oJ4H@example.com").first()
    #     self.assertIsNone(user)

    # # To test duplicate email
    # def test_create_user_duplicate_email(self):
    #     # First, create a user
    #     user = _US.UserCreate(username="testuser", email="5oJ4H@example.com", password="testpassword")
    #     _AV.create_user(user, self.db)

    #     # Try creating another user with the same email
    #     user2 = _US.UserCreate(username="another_user", email="5oJ4H@example.com", password="another_password")
        
    #     # Expect an HTTPException to be raised due to the duplicate email
    #     with self.assertRaises(HTTPException) as context:
    #         _AV.create_user(user2, self.db)
        
    #     self.assertEqual(context.exception.status_code, 400)
    #     self.assertEqual(context.exception.detail, "Email already registered")

    #     # Clean up after the test
    #     self.db.query(_UI.User).filter(_UI.User.email == "5oJ4H@example.com").delete()
    #     self.db.commit()

    #     # Check if the user was deleted from the database
    #     user = self.db.query(_UI.User).filter(_UI.User.email == "5oJ4H@example.com").first()
    #     self.assertIsNone(user)
    
    # #Test for valid user creation
    # def test_create_user_valid_data(self):
    #     # Create a new user
    #     user = _US.UserCreate(username="newuser", email="newuser@example.com", password="password123")

    #     # Call the create_user function
    #     _AV.create_user(user, self.db)

    #     # Retrieve the user from the database and check the data
    #     db_user = self.db.query(_UI.User).filter(_UI.User.email == "newuser@example.com").first()
    #     self.assertIsNotNone(db_user)
    #     self.assertEqual(db_user.username, "newuser")
    #     self.assertEqual(db_user.email, "newuser@example.com")
    #     self.assertNotEqual(db_user.hashed_password, "password123")  # Ensure the password is hashed

    #     # Clean up after the test
    #     self.db.query(_UI.User).filter(_UI.User.email == "newuser@example.com").delete()
    #     self.db.commit()

    #     # Check if the user was deleted from the database
    #     db_user = self.db.query(_UI.User).filter(_UI.User.email == "newuser@example.com").first()
    #     self.assertIsNone(db_user)


    # #Test for missing required fields 
    def test_create_user_missing_field(self):
        # Try creating a user without a password
        user = _US.UserCreate(username="missing_password", email="missingpassword@example.com", password="")

        with self.assertRaises(HTTPException) as context:
            _AV.create_user(user, self.db)

        self.assertEqual(context.exception.status_code, 422)
        self.assertIn("password", context.exception.detail)

    def test_create_user_missing_email(self):
        # Try creating a user without an email
        user = _US.UserCreate(username="missing_email", email="", password="password123")

        with self.assertRaises(HTTPException) as context:
            _AV.create_user(user, self.db)

        self.assertEqual(context.exception.status_code, 422)
        self.assertIn("email", context.exception.detail)

    def test_create_user_missing_username(self):
        # Try creating a user without a username
        user = _US.UserCreate(username="", email="no_username@example.com", password="password123")

        with self.assertRaises(HTTPException) as context:
            _AV.create_user(user, self.db)

        self.assertEqual(context.exception.status_code, 422)
        self.assertIn("username", context.exception.detail)
