import pytest, os 
from classes.database import SingletonDatabase
from app import app as flask_app

fakeUser = os.environ.get('TEST_USER')
databaseIP = os.environ.get('DB_HOST')
databaseUserName = os.environ.get('DB_USER')
databasePassword = os.environ.get('DB_PASS')
databaseName = os.environ.get('DB_NAME')
databasePort = int(os.environ.get('DB_PORT'))

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def DatabaseInstance():
    DatabaseInstance = SingletonDatabase.get_instance()
    return DatabaseInstance

@pytest.fixture
def FakeUserDetails(DatabaseInstance):
    user = DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeUser)
    return user

def test_SingletonCannotBeInstantiatedTwice(app):
    with pytest.raises(Exception) as re:
        database = SingletonDatabase(app, databaseIP, databaseUserName, databasePassword, databaseName, databasePort)
    assert str(re.value) == "You cannot create another SingletonDatabase class"

def test_DBGetUserDetailsWithoutPicByEmail(DatabaseInstance):
    res = DatabaseInstance.getUserDetailsWithoutPicByEmail(fakeUser)
    assert len(res) == 15

def test_DBGetUserDetailsByEmail(DatabaseInstance):
    res = DatabaseInstance.getUserDetailsByEmail(fakeUser)
    assert len(res) == 16

def test_DBGetUserWalletBalance(FakeUserDetails, DatabaseInstance):
    res = DatabaseInstance.getUserWalletBalance(FakeUserDetails[0])
    assert res[0] > 0

def test_DBExecuteInsertQueryWithParameters(DatabaseInstance):
    res = DatabaseInstance.executeInsertQueryWithParameters("INSERT INTO 123 (1,2,3) VALUES (%s,%s,%s)",['test', 'test', 'test'])
    assert res == False

def test_DBExecuteUpdateQueryWithParameters(DatabaseInstance):
    res = DatabaseInstance.executeInsertQueryWithParameters('UPDATE test SET test1 = %s, test2 = %s WHERE idUser = %s',['test', 'test', 'test'])
    assert res == False

def test_DBExecuteDeleteQueryWithParameters(DatabaseInstance):
    res = DatabaseInstance.executeInsertQueryWithParameters('DELETE FROM test WHERE test=%s', ['test'])
    assert res == False