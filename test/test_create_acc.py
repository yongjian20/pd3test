import pytest, os 

from app import app as flask_app, saltPepperHash
Pepper = os.environ.get('PEPPER')
@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_email_mismatch(client):
    fake_data = {
            "firstName": "test",
            "lastName": "test",
            "email": "test@gmail.com",
            "confirmEmail": "testtest@gmail.com",
            "displayName": "test User",
            "mobileNumber": "91234567",
            "dob": "2000-01-01",
            "mailingAddress": "Blk 123 ABC Road",
            "password": "123123123",
            "confirmPassword": "123123123"
        }
    res = client.post("/create_account", data=fake_data, follow_redirects=True)
    assert res.status_code == 200
    assert b"Email mismatch. Please try again." in res.data

def test_password_mismatch(client):
    fake_data = {
            "firstName": "test",
            "lastName": "test",
            "email": "test@gmail.com",
            "confirmEmail": "test@gmail.com",
            "displayName": "test User",
            "mobileNumber": "91234567",
            "dob": "2000-01-01",
            "mailingAddress": "Blk 123 ABC Road",
            "password": "123123123",
            "confirmPassword": "asdasdasd"
        }
    res = client.post("/create_account", data=fake_data, follow_redirects=True)
    assert res.status_code == 200
    assert b"Password mismatch. Please try again." in res.data

def test_futureDOB(client):
    fake_data = {
            "firstName": "test",
            "lastName": "test",
            "email": "test@gmail.com",
            "confirmEmail": "test@gmail.com",
            "displayName": "test User",
            "mobileNumber": "91234567",
            "dob": "9999-12-12",
            "mailingAddress": "Blk 123 ABC Road",
            "password": "123!@#asd321",
            "confirmPassword": "123!@#asd321"
        }
    res = client.post("/create_account", data=fake_data, follow_redirects=True)
    print(res.data)
    assert res.status_code == 200
    assert b"You cannot enter future date." in res.data

def test_DOB_less_21(client):
    fake_data = {
            "firstName": "test",
            "lastName": "test",
            "email": "test@gmail.com",
            "confirmEmail": "test@gmail.com",
            "displayName": "test User",
            "mobileNumber": "91234567",
            "dob": "2021-01-01",
            "mailingAddress": "Blk 123 ABC Road",
            "password": "123!@#asd321",
            "confirmPassword": "123!@#asd321"
        }
    res = client.post("/create_account", data=fake_data, follow_redirects=True)
    assert res.status_code == 200
    assert b"You must be 21 and above to register." in res.data

def test_Common_Password(client):
    fake_data = {
            "firstName": "test",
            "lastName": "test",
            "email": "test@gmail.com",
            "confirmEmail": "test@gmail.com",
            "displayName": "test User",
            "mobileNumber": "91234567",
            "dob": "2021-01-01",
            "mailingAddress": "Blk 123 ABC Road",
            "password": "123123123",
            "confirmPassword": "123123123"
        }
    res = client.post("/create_account", data=fake_data, follow_redirects=True)
    assert res.status_code == 200
    assert b"Password used is too common." in res.data

def test_CreateAcc(client):
    fake_data = {
            "firstName": "test",
            "lastName": "test",
            "email": "test@gmail.com",
            "confirmEmail": "test@gmail.com",
            "displayName": "test User",
            "mobileNumber": "91234567",
            "dob": "2000-01-01",
            "mailingAddress": "Blk 123 ABC Road",
            "password": "123!@#asd321",
            "confirmPassword": "123!@#asd321"
        }
    res = client.post("/create_account", data=fake_data, follow_redirects=True)
    assert res.status_code == 200
    assert b"An email verification link has been sent to your registered email address." in res.data