import pytest, os
from app import app as flask_app
import classes.accessControl as ac
from classes.database import SingletonDatabase
import classes.sessionManager as sm

fakeUser = os.environ.get('TEST_USER')
fakeAdmin = os.environ.get('TEST_ADMIN')

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    app.testing = True
    app.app_context().push()
    yield app.test_client()

def test_ACUserProfile(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeUser))
        assert ac.hasAccess(sess['role'],"profile")

def test_ACUserProducts(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeUser))
        assert ac.hasAccess(sess['role'],"products")

def test_ACUserAddProduct(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeUser))
        assert ac.hasAccess(sess['role'],"add_product")

def test_ACUserProductPage(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeUser))
        assert ac.hasAccess(sess['role'],"product_page")
    
def test_ACUserReportproduct(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeUser))
        assert ac.hasAccess(sess['role'],"report_product")

def test_UserACAdminPage(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeUser))
        assert ac.hasAccess(sess['role'],"admin") == False 

def test_UserACAdminProduct(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeUser))
        assert ac.hasAccess(sess['role'],"admin_products") == False 

def test_UserACAdminReport(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeUser))
        assert ac.hasAccess(sess['role'],"admin_report") == False 
    
def test_UserACAdminBan(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeUser))
        assert ac.hasAccess(sess['role'],"admin_ban") == False 
        
def test_ACAdminProfile(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeAdmin))
        assert ac.hasAccess(sess['role'],"profile")

def test_ACAdminPage(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeAdmin))
        assert ac.hasAccess(sess['role'],"admin")

def test_ACAdminProduct(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeAdmin))
        assert ac.hasAccess(sess['role'],"admin_products")

def test_ACAdminReport(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeAdmin))
        assert ac.hasAccess(sess['role'],"admin_report")
    
def test_ACAdminBan(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeAdmin))
        assert ac.hasAccess(sess['role'],"admin_ban")

def test_AdminACUserProducts(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeAdmin))
        assert ac.hasAccess(sess['role'],"products") == False 

def test_AdminACUserAddProduct(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeAdmin))
        assert ac.hasAccess(sess['role'],"add_product") == False 

def test_AdminACUserProductPage(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeAdmin))
        assert ac.hasAccess(sess['role'],"product_page") == False 
    
def test_AdminACUserReportproduct(client):
    with client.session_transaction() as sess:
        DatabaseInstance = SingletonDatabase.get_instance()
        sm.storeUserDetails(sess, DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeAdmin))
        assert ac.hasAccess(sess['role'],"report_product") == False 