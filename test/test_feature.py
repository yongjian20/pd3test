import base64
from datetime import datetime
import pytest, os 

from app import app as flask_app, saltPepperHash, formatDT, decodePic
Pepper = os.environ.get('PEPPER')
@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_saltPepperHash():
    assert saltPepperHash('123', Pepper, '123') == '7ce6b2884808cf31ee47668f1b59bdee5b823f07db4bd007a6fd955c64a4b676'

def test_dateFormatEmpty():
    assert formatDT('') == ''

def test_decodePicEmpty():
    assert decodePic('') == ''

def test_dateFormat():
    assert formatDT(datetime(2021,1,1)) == '01-Jan-2021'
