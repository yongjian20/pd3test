import pytest, os 

from app import app as flask_app, saltPepperHash
Pepper = os.environ.get('PEPPER')
@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_LandingPage(app, client):
    #del app
    res = client.get('/')
    assert res.status_code == 200
    assert b"Welcome To Let's Bid!" in res.data

def test_ProductPage(client):
    res = client.get('/products', follow_redirects=True)
    assert res.status_code == 200
    
def test_LoginPage(client):
    res = client.get('/login')
    assert res.status_code == 200
    assert b"Please enter your login and password" in res.data

def test_LogOutPage(client):
    res = client.get('/logout', follow_redirects=True)
    assert res.status_code == 200
    assert b"Welcome To Let's Bid!" in res.data

def test_CreateAccPage(client):
    res = client.get('/create_account')
    assert res.status_code == 200
    assert b"Register Your Account" in res.data

def test_ForgetPasswordPage(client):
    res = client.get('/forget_password')
    assert res.status_code == 200
    assert b"Please enter your email address" in res.data

def test_AdminPageWithURl(client):
    res = client.get('/admin', follow_redirects=True)
    assert res.status_code == 404
    assert b"ERROR 404  - Page not found" in res.data

def test_CreateQRcodeWithURl(client):
    res = client.get('/create_qrcode', follow_redirects=True)
    assert res.status_code == 404
    assert b"ERROR 404  - Page not found" in res.data

def test_OTPWithURl(client):
    res = client.get('/otp_login', follow_redirects=True)
    assert res.status_code == 404
    assert b"ERROR 404  - Page not found" in res.data

def test_ResetPasswordWithUrl(client):
    res = client.get('/new_password/', follow_redirects=True)
    assert res.status_code == 404
    assert b"ERROR 404  - Page not found" in res.data

def test_HTML405(client):
    res = client.post('/process_account/1', follow_redirects=True)
    assert res.status_code == 405
    assert b"ERROR 405 - Method Not Allowed" in res.data
