import pytest, os
from classes.database import SingletonDatabase
import classes.sessionManager as sm
from flask import session, request
from app import app as flask_app

fakeUser = os.environ.get('TEST_USER')

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    app.testing = True
    app.app_context().push()
    yield app.test_client()

def test_LoginWithoutReCaptcha(client):
    fake_data = {
            "email": "test@gmail.com",
            "password": "asdasdasd"
        }
    res = client.post("/login", data=fake_data, follow_redirects=True)
    assert res.status_code == 200
    print(res.data)
    assert b"Please fill out the ReCaptcha." in res.data

# def test_LoginlandingPage(client):
#     with client.session_transaction() as sess:
#         DatabaseInstance = SingletonDatabase.get_instance()
#         user = DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeUser)
#         session['trest'] = 'test'
#         sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeUser))
#         sess['loggedIn'] = True
#         sess['role'] = 2
#         #sess['user'] = user
#         res = client.get('/')
#         #print(b"Logout" in b"Logout")
#         assert res.status_code == 200
#         assert b"Logout" in res.data
#         #assert sess['email'] == user[2] 
#         #sess.pop['loggedIn']