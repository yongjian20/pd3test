import os, hashlib, pyotp, pyqrcode, io, uuid, base64, json, zlib
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from datetime import datetime as dt
from datetime import timedelta
import datetime as dt_mod
from base64 import b64encode
from markupsafe import Markup
from werkzeug.exceptions import abort
from classes.database import SingletonDatabase
import classes.sessionManager as sm
import classes.accessControl as ac
import classes.sanitization as sanitize
import classes.APIsendgrid as SendGrid
from dotenv import load_dotenv
from flask_recaptcha import ReCaptcha

load_dotenv()

app = Flask(__name__)

fake_user = os.environ.get('TEST_USER')
secret_key = os.environ.get('SECRET_KEY')
app.secret_key = secret_key
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
# app.config['SESSION_COOKIE_SECURE'] = True
# app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
# app.config["SESSION_COOKIE_NAME"] = '__Host-SID'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Upload file size limit to 16mb
app.config['RECAPTCHA_SITE_KEY'] = os.environ.get('RECAPTCHA_SITE_KEY')
app.config['RECAPTCHA_SECRET_KEY'] = os.environ.get('RECAPTCHA_SECRET_KEY')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
Pepper = os.environ.get('PEPPER')
databaseIP = os.environ.get('DB_HOST')
databaseUserName = os.environ.get('DB_USER')
databasePassword = os.environ.get('DB_PASS')
databaseName = os.environ.get('DB_NAME')
databasePort = int(os.environ.get('DB_PORT'))
database = SingletonDatabase(app, databaseIP, databaseUserName, databasePassword, databaseName, databasePort)
DatabaseInstance = database.get_instance()
Session(app)
recaptcha = ReCaptcha(app)


@app.route('/')
def landing():
    if session.get('user'):
        user = session['user']
        return render_template('index.html', user=user)
    # Access DB using inner join to get the lastest 3 product and display.    
    allProducts = DatabaseInstance.executeSelectMultipleQuery(
        'SELECT itemTable.idItem, itemTable.Name, itemTable.Description, '
        'itemTable.Amount, itemStatusTypeTable.Description, itemCategoryTable.Description, '
        'itemImageTable.Image FROM Item AS itemTable INNER JOIN ItemCategory AS itemCategoryTable ON '
        'itemTable.idItemCategory = itemCategoryTable.idItemCategory INNER JOIN ItemStatusType AS '
        'itemStatusTypeTable ON itemTable.idItemStatus = itemStatusTypeTable.idItemStatusType INNER JOIN '
        'ItemImage AS itemImageTable ON itemTable.idItem = itemImageTable.idItem where itemTable.idItemStatus <> 5 LIMIT 3')

    return render_template('index.html', allProducts=allProducts)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    loginmsg = ''
    if request.method == "POST":
        if recaptcha.verify():
            formEmail = request.form.get('email')
            userData = DatabaseInstance.executeSelectOneQueryWithParameters(
                'SELECT idUser, LoginAttempts, MobileNumber FROM User WHERE Email = %s', [formEmail])
            if userData and int(userData[1]) < 6:
                formPassword = saltPepperHash(userData[2], Pepper, request.form.get('password'))
                result = DatabaseInstance.executeSelectOneQueryWithParameters(
                    'SELECT idUserPass FROM UserPass WHERE Password = %s and idUser = %s', [formPassword, userData[0]])
                ipAdd = request.remote_addr
                if result:
                    session.permanent = True
                    DatabaseInstance.executeUpdateQueryWithParameters(
                        'UPDATE User SET LastLoginDate = %s, LoginAttempts = %s, IPAddress = %s WHERE idUser = %s',
                        [dt.today().strftime('%Y-%m-%d %H:%M:%S'), '0', ipAdd, userData[0]])
                    sm.storeUserDetails(session, DatabaseInstance.getUserDetailsWithoutPicByEmail(formEmail))
                    if session['otpStatus'] == 1:
                        session['process_OTPLogin'] = 1
                        return redirect(url_for('otp_login'))
                    else:
                        return redirect(url_for('create_qrcode'))
                else:
                    DatabaseInstance.executeUpdateQueryWithParameters(
                        'UPDATE User SET LoginAttempts = %s, IPAddress = %s WHERE idUser = %s',
                        [userData[1] + 1, ipAdd, userData[0]])
            loginmsg = 'Please enter a vaild Email and Password. '
        else:
            loginmsg = 'Please fill out the ReCaptcha. '
    return render_template('login.html', loginmsg=loginmsg, timestamp=dt.today().strftime('%d-%b-%y %H:%M:%S'))


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == "POST":
        if request.form['password'] != request.form['confirmPassword']:
            return render_template('create_account.html', errorMsg="Password mismatch. Please try again.")

        if len(request.form['password']) > 128:
            return render_template('create_account.html', errorMsg="Password length over 128 characters.")

        if request.form['email'] != request.form['confirmEmail']:
            return render_template('create_account.html', errorMsg="Email mismatch. Please try again.")

        if os.path.exists('common.txt'):
            with open('common.txt', 'r') as inF:
                for line in inF:
                    if request.form['password'] in line:
                        return render_template('create_account.html', errorMsg="Password used is too common.")

        present = dt.now()
        checkage = dt(present.year - 21, present.month, present.day)
        checkage = checkage
        formDob = dt.strptime(request.form['dob'], '%Y-%m-%d')
        if formDob > present:
            return render_template('create_account.html', errorMsg="You cannot enter future date.")
        if formDob > checkage:
            return render_template('create_account.html', errorMsg="You must be 21 and above to register.")
        if sanitize.MobileNumber(request.form['mobileNumber']) is None:
            return render_template('create_account.html', errorMsg="Invalid Mobile Number.")

        user = DatabaseInstance.executeSelectOneQueryWithParameters(
            'SELECT Email, MobileNumber FROM User WHERE Email = %s OR MobileNumber = %s',
            [request.form['email'], request.form['mobileNumber']])
        entry = DatabaseInstance.executeSelectOneQueryWithParameters('SELECT Email FROM UniqueURL WHERE Email=%s',
                                                                     [request.form.get('email')])
        if user is None and entry is None:
            uniqueId = uuid.uuid4().hex
            DatabaseInstance.executeInsertQueryWithParameters(
                'INSERT INTO UniqueURL (idUniqueURL, ByteData, Email, Type) VALUES (%s, %s, %s, %s)',
                [uniqueId, zlib.compress(json.dumps(request.form).encode()), request.form['email'], "CreateAccount"]
            )
            emailMsg = request.form[
                           'displayName'] + ",\n\nYour account creation link is: " + "dabestteam.sitict.net/process_account/" + uniqueId
            SendGrid.send_email(request.form['email'], "Let's Bid - Account Creation", emailMsg)

        return render_template('email_verification.html')
    return render_template('create_account.html', errorMsg='')


@app.route('/process_account/<accId>', methods=['GET'])
def process_account(accId):
    entry = DatabaseInstance.executeSelectOneQueryWithParameters('SELECT * FROM UniqueURL WHERE idUniqueURL=%s',
                                                                 [accId])
    if entry is None or entry[3] != "CreateAccount":
        abort(404)

    byteData = json.loads(zlib.decompress(entry[1]).decode("utf-8"))

    user_id = uuid.uuid4().hex
    DatabaseInstance.executeInsertQueryWithParameters(
        'INSERT INTO User (idUser, idUserType, Email, MobileNumber, DOB, FirstName, LastName, DisplayName, MailingAddress, JoinDate, LoginAttempts, IPAddress) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        [user_id, '2', byteData['email'], byteData['mobileNumber'], byteData['dob'], byteData['firstName'],
         byteData['lastName'], byteData['displayName'],
         byteData['mailingAddress'], dt.today().strftime('%Y-%m-%d %H:%M:%S'), '0', request.remote_addr])

    formPassword = saltPepperHash(byteData['mobileNumber'], Pepper, byteData['password'])

    DatabaseInstance.executeInsertQueryWithParameters(
        'INSERT INTO UserPass (idUser, Password, LastUpdateDate) VALUES (%s, %s, %s)',
        [user_id, formPassword, dt.today().strftime('%Y-%m-%d %H:%M:%S')])

    DatabaseInstance.executeInsertQueryWithParameters(
        'INSERT INTO WalletTranscript(idUser, idWalletTransactionType, Amount, Remarks, DateSubmit)VALUES(%s,%s,%s,%s,%s);',
        [user_id, '2', 0, "Account Initialized", dt.today().strftime('%Y-%m-%d %H:%M:%S')])

    session.permanent = True
    sm.storeUserDetails(session, DatabaseInstance.getUserDetailsWithoutPicByEmail(byteData['email']))

    DatabaseInstance.executeDeleteQueryWithParameters('DELETE FROM UniqueURL WHERE idUniqueURL=%s', [accId])
    return redirect(url_for('create_qrcode'))


@app.route('/create_qrcode', methods=['GET', 'POST'])
def create_qrcode():
    if session.get('otpStatus') is None:
        return abort(404)
    elif session['otpStatus'] == 1:
        return render_template('otp_support.html')

    OTPKey = DatabaseInstance.executeSelectOneQueryWithParameters("SELECT OTPKey FROM UserPass WHERE idUser=%s",
                                                                  [session['id']])[0]
    if OTPKey is None:
        OTPKey = pyotp.random_base32()
        DatabaseInstance.executeUpdateQueryWithParameters('UPDATE UserPass SET OTPKey=%s WHERE idUser=%s',
                                                          [OTPKey, session['id']])
    errorMsg = ""
    if request.method == "POST":
        if pyotp.TOTP(OTPKey).verify(request.form.get('otp_code')):
            session['loggedIn'] = True
            if session['otpStatus'] == 0:
                DatabaseInstance.executeUpdateQueryWithParameters('UPDATE User SET OtpStatus = %s WHERE idUser = %s',
                                                                  [1, session['id']])
                session['otpStatus'] = 1
            return redirect(url_for('profile'))
        else:
            errorMsg = "Invalid OTP"
    # using third party libaray to genrate QR image
    totp_uri = pyotp.totp.TOTP(OTPKey).provisioning_uri(name=session['email'], issuer_name="Let's Bid")
    url = pyqrcode.create(totp_uri)
    stream = io.BytesIO()
    url.svg(stream, scale=4, module_color="white", xmldecl=False)

    return render_template('create_qrcode.html', errorMsg=errorMsg, qr_image=Markup(stream.getvalue().decode('utf-8')))


@app.route('/otp_login', methods=['GET', 'POST'])
def otp_login():
    if session.get('process_OTPLogin') is None:
        return abort(404)

    OTPKey = DatabaseInstance.executeSelectOneQueryWithParameters("SELECT OTPKey FROM UserPass WHERE idUser=%s",
                                                                  [session['id']])[0]
    errorMsg = ""
    if request.method == "POST":
        if pyotp.TOTP(OTPKey).verify(request.form.get('otp_code')):
            session['loggedIn'] = True
            session.pop('process_OTPLogin')
            return redirect(url_for('profile'))
        else:
            errorMsg = "Invalid OTP"

    return render_template('otp_login.html', errorMsg=errorMsg)


@app.route('/profile_page', methods=['GET', 'POST'])
def profile():
    if sm.isLoggedIn(session) is False:
        return redirect(url_for('landing'))
    if not ac.hasAccess(session['role'], "profile"):
        return abort(404)

    errorMsg = ''
    userPic = DatabaseInstance.getUserDetailsByEmail(str(session['email']))[8]
    userbalance = DatabaseInstance.getUserWalletBalance(session['id'])[0]
    if request.method == "POST":
        if request.form.get('save'):
            formFirstName = request.form.get('firstName')
            formLastName = request.form.get('lastName')
            formMailAdd = request.form.get('mailingAddress')
            formDeliAdd = request.form.get('deliveryAddress')
            BinaryPicture = ""
            uploaded_file = request.files['image_file']
            password = request.form.get('password')
            confirmPassword = request.form.get('confirmPassword')
            if uploaded_file.filename != '':
                BinaryPicture = uploaded_file.read()

            if password != '' and request.form.get('oldPassword') != '':
                formOldPassword = saltPepperHash(session['mobile'], Pepper, request.form.get('oldPassword'))
                result = DatabaseInstance.executeSelectOneQueryWithParameters(
                    'SELECT idUserPass FROM UserPass WHERE Password = %s and idUser = %s',
                    [formOldPassword, session['id']])
                if result:
                    if password != confirmPassword:
                        return render_template('profile_page.html', userbalance=userbalance, userPic=userPic,
                                               errorMsg="Password mismatch. Please try again.")
                    else:
                        if BinaryPicture:
                            formPassword = saltPepperHash(session['mobile'], Pepper, request.form.get('password'))
                            DatabaseInstance.executeUpdateQueryWithParameters(
                                'UPDATE UserPass SET idUser = %s, Password = %s, LastUpdateDate = %s WHERE idUser = %s',
                                [session['id'], formPassword, dt.today().strftime('%Y-%m-%d %H:%M:%S'), session['id']])

                            DatabaseInstance.executeUpdateQueryWithParameters(
                                'UPDATE User SET FirstName = %s, LastName = %s, ProfilePicture = %s, MailingAddress=%s, DeliveryAddress=%s WHERE idUser = %s',
                                [formFirstName, formLastName, BinaryPicture, formMailAdd, formDeliAdd, session['id']])

                            sm.storeUserDetails(session,
                                                DatabaseInstance.getUserDetailsWithoutPicByEmail(session['email']))

                        else:
                            formPassword = saltPepperHash(session['mobile'], Pepper, request.form.get('password'))
                            DatabaseInstance.executeUpdateQueryWithParameters(
                                'UPDATE UserPass SET idUser = %s, Password = %s, LastUpdateDate = %s WHERE idUser = %s',
                                [session['id'], formPassword, dt.today().strftime('%Y-%m-%d %H:%M:%S'), session['id']])

                            DatabaseInstance.executeUpdateQueryWithParameters(
                                'UPDATE User SET FirstName = %s, LastName = %s, MailingAddress=%s, DeliveryAddress=%s WHERE idUser = %s',
                                [formFirstName, formLastName, formMailAdd, formDeliAdd, session['id']])

                            sm.storeUserDetails(session,
                                                DatabaseInstance.getUserDetailsWithoutPicByEmail(session['email']))
                            return render_template('profile_page.html', userbalance=userbalance, userPic=userPic,
                                                   errorMsg="Password updated.")
                return render_template('profile_page.html', userbalance=userbalance, userPic=userPic,
                                       errorMsg="Old Password mismatch. Please try again.")
            if BinaryPicture:
                DatabaseInstance.executeUpdateQueryWithParameters(
                    'UPDATE User SET FirstName = %s, LastName = %s, ProfilePicture = %s, MailingAddress=%s, DeliveryAddress=%s WHERE idUser = %s',
                    [formFirstName, formLastName, BinaryPicture, formMailAdd, formDeliAdd, session['id']])
                sm.storeUserDetails(session, DatabaseInstance.getUserDetailsWithoutPicByEmail(session['email']))
            else:
                DatabaseInstance.executeUpdateQueryWithParameters(
                    'UPDATE User SET FirstName = %s, LastName = %s, MailingAddress=%s, DeliveryAddress=%s WHERE idUser = %s',
                    [formFirstName, formLastName, formMailAdd, formDeliAdd, session['id']])
                sm.storeUserDetails(session, DatabaseInstance.getUserDetailsWithoutPicByEmail(session['email']))
            return redirect(url_for('profile'))
    return render_template('profile_page.html', userbalance=userbalance, userPic=userPic, errorMsg=errorMsg)


@app.route('/products')
def products():
    if sm.isLoggedIn(session) is False:
        return redirect(url_for('landing'))
    if not ac.hasAccess(session['role'], "products"):
        return abort(404)

    allProducts = DatabaseInstance.executeSelectMultipleQuery(
        'SELECT itemTable.idItem, itemTable.Name, itemTable.Description, itemTable.Amount, itemStatusTypeTable.Description, itemCategoryTable.Description, itemImageTable.Image FROM Item AS itemTable INNER JOIN ItemCategory AS itemCategoryTable ON itemTable.idItemCategory = itemCategoryTable.idItemCategory INNER JOIN ItemStatusType AS itemStatusTypeTable ON itemTable.idItemStatus = itemStatusTypeTable.idItemStatusType INNER JOIN ItemImage AS itemImageTable ON itemTable.idItem = itemImageTable.idItem')

    return render_template('products.html', allProducts=allProducts)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if sm.isLoggedIn(session) is False:
        return redirect(url_for('landing'))
    if not ac.hasAccess(session['role'], "add_product"):
        return abort(404)

    db_cat = DatabaseInstance.executeSelectMultipleQuery('SELECT * FROM ItemCategory')
    categoryOption = [i[1] for i in db_cat]

    if request.method == "POST":
        item_id = uuid.uuid4().hex
        uploaded_file = request.files['image_file']

        for i in db_cat:
            if request.form.get('category') == i[1]:
                selected_category = i[0]

        BinaryPicture = ""
        if uploaded_file.filename != '':
            BinaryPicture = uploaded_file.read()
        if BinaryPicture:
            time_today = dt.today()
            time_change = dt_mod.timedelta(days=int(request.form.get('days')), hours=int(request.form.get('hours')))
            new_time = time_today + time_change
            DatabaseInstance.executeInsertQueryWithParameters(
                'INSERT INTO Item (idItem, idSeller, idItemStatus, idItemCategory, Name, Description, Amount, BidStartDate, BidEndDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                [item_id, session['id'], 1, selected_category, request.form.get('name'), request.form.get('desc'),
                 request.form.get('value'), time_today.strftime('%Y-%m-%d %H:%M:%S'),
                 new_time.strftime('%Y-%m-%d %H:%M:%S')])
            DatabaseInstance.executeInsertQueryWithParameters(
                'INSERT INTO ItemImage (idItem, Image) VALUES (%s, %s)',
                [item_id, BinaryPicture])
        return redirect(url_for('products'))
    return render_template('add_product.html', categoryOption=categoryOption)


@app.route('/products/<itemId>', methods=['GET', 'POST'])
def product_page(itemId):
    if sm.isLoggedIn(session) is False:
        return redirect(url_for('landing'))
    if not ac.hasAccess(session['role'], "product_page"):
        return abort(404)

    errorMsg = ''
    if request.method == "POST":
        item = DatabaseInstance.executeSelectOneQueryWithParameters(
            'SELECT Amount, idSeller FROM Item WHERE idItem=%s', [itemId])
        if item[1] != session['id']:
            OTPKey = DatabaseInstance.executeSelectOneQueryWithParameters("SELECT OTPKey FROM UserPass WHERE idUser=%s",
                                                                          [session['id']])[0]
            if pyotp.TOTP(OTPKey).verify(request.form.get('otp_code')):
                walletBal = DatabaseInstance.getUserWalletBalance(session['id'])[0]

                value = sanitize.PositiveDollar(request.form.get('value'))
                if value is not None:
                    if walletBal >= value:
                        if item[0] < value:
                            DatabaseInstance.executeInsertQueryWithParameters(
                                'UPDATE Item SET Amount=%s WHERE idItem=%s and (Amount <= %s)',
                                [value, itemId, value]
                            )
                            DatabaseInstance.executeInsertQueryWithParameters(
                                'INSERT INTO AuctionTranscript (idInventory, idBidder, Amount, DateSubmit) VALUES (%s, %s, %s, %s)',
                                [itemId, session['id'], value, dt.today().strftime('%Y-%m-%d %H:%M:%S')]
                            )
                        else:
                            errorMsg = "Bid is lower than highest bid!"
                    else:
                        errorMsg = "Insufficient wallet balance!"
                else:
                    errorMsg = "Invalid amount input!"
            else:
                errorMsg = "Invalid OTP!"
        else:
            errorMsg = "Seller cannot bid own product!"

    item = DatabaseInstance.executeSelectOneQueryWithParameters(
        'SELECT Name, Description, Amount, BidStartDate, BidEndDate FROM Item WHERE idItem=%s', [itemId])
    item_image = DatabaseInstance.executeSelectOneQueryWithParameters('SELECT Image FROM ItemImage WHERE idItem=%s',
                                                                      [itemId])
    decoded_image = base64.b64encode(item_image[0]).decode("utf-8")

    bids = DatabaseInstance.executeSelectMultipleQueryWithParameters(
        'SELECT idBidder, Amount, DateSubmit FROM AuctionTranscript WHERE idInventory=%s', [itemId])

    return render_template('product_page.html', name=item[0], desc=item[1], value=item[2],
                           image_picture=decoded_image,
                           time_left=item[4].strftime('%Y-%m-%d %H:%M:%S'), bids=bids, item_id=itemId,
                           errorMsg=errorMsg)


@app.route('/report/<itemId>', methods=['GET', 'POST'])
def report_product(itemId):
    if sm.isLoggedIn(session) is False:
        return redirect(url_for('landing'))
    if not ac.hasAccess(session['role'], "report_product"):
        return abort(404)

    item_status = DatabaseInstance.executeSelectOneQueryWithParameters(
        'SELECT idItemStatus FROM Item WHERE idItem = %s', [itemId])
    if item_status[0] == 1:
        DatabaseInstance.executeUpdateQueryWithParameters('UPDATE Item SET idItemStatus = %s WHERE idItem = %s',
                                                          [4, itemId])
    return redirect(url_for('products'))


@app.route('/e_wallet', methods=['GET', 'POST'])
def e_wallet():
    if sm.isLoggedIn(session) is False:
        return redirect(url_for('landing'))
    if not ac.hasAccess(session['role'], "e_wallet"):
        return abort(404)

    if request.method == "POST":
        if request.form.get('creditBtn'):
            Remark = str(request.form.get('creditBank')) + ": " + str(request.form.get('creditCard'))
            amount = request.form.get('creditAmount')
            DatabaseInstance.executeInsertQueryWithParameters(
                'INSERT INTO WalletTranscript(idUser, idWalletTransactionType, Amount, Remarks, DateSubmit)VALUES(%s,%s,%s,%s,%s);',
                [session['id'], '2', amount, Remark, dt.today().strftime('%Y-%m-%d %H:%M:%S')])
        elif request.form.get('debitBtn'):
            Remark = str(request.form.get('debitBank')) + ": " + str(request.form.get('debitCard'))
            amount = request.form.get('debitAmount')
            DatabaseInstance.executeInsertQueryWithParameters(
                'INSERT INTO WalletTranscript(idUser, idWalletTransactionType, Amount, Remarks, DateSubmit)VALUES(%s,%s,%s,%s,%s);',
                [session['id'], '1', -abs(float(amount)), Remark, dt.today().strftime('%Y-%m-%d %H:%M:%S')])

    userbalance = DatabaseInstance.getUserWalletBalance(session['id'])[0]
    walletTranscript = DatabaseInstance.executeSelectMultipleQueryWithParameters(
        'SELECT WT.Amount,  WTT.Description, WT.Remarks, WT.DateSubmit from WalletTranscript as WT INNER JOIN WalletTransactionType AS WTT ON WT.idWalletTransactionType = WTT.idWalletTransactionType WHERE idUser = %s ORDER BY WT.DateSubmit DESC;',
        [session['id']])

    return render_template('e_wallet.html', userbalance=userbalance, walletTranscript=walletTranscript)


@app.route('/admin')
def admin():
    if sm.isLoggedIn(session) is False:
        return abort(404)
    if not ac.hasAccess(session['role'], "admin"):
        return abort(404)

    return render_template('admin_home.html')


@app.route('/admin_products')
def admin_products():
    if sm.isLoggedIn(session) is False:
        return redirect(url_for('landing'))
    if not ac.hasAccess(session['role'], "admin_products"):
        return abort(404)

    allProducts = DatabaseInstance.executeSelectMultipleQuery(
        'SELECT itemTable.idItem, itemTable.Name, itemTable.Description, itemTable.Amount, itemStatusTypeTable.Description, itemCategoryTable.Description FROM Item AS itemTable INNER JOIN ItemCategory AS itemCategoryTable ON itemTable.idItemCategory = itemCategoryTable.idItemCategory INNER JOIN 3X03.ItemStatusType AS itemStatusTypeTable ON itemTable.idItemStatus = itemStatusTypeTable.idItemStatusType')
    item_image = DatabaseInstance.executeSelectMultipleQuery('SELECT Image FROM ItemImage')

    return render_template('admin_products.html', allProducts=allProducts, item_image=item_image)


@app.route('/admin_report')
def admin_report():
    if sm.isLoggedIn(session) is False:
        return redirect(url_for('landing'))
    if not ac.hasAccess(session['role'], "admin_report"):
        return abort(404)

    allProducts = DatabaseInstance.executeSelectMultipleQuery(
        'SELECT itemTable.idItem, itemTable.Name, itemTable.Description, itemTable.Amount, itemStatusTypeTable.Description, itemCategoryTable.Description FROM Item AS itemTable INNER JOIN ItemCategory AS itemCategoryTable ON itemTable.idItemCategory = itemCategoryTable.idItemCategory INNER JOIN 3X03.ItemStatusType AS itemStatusTypeTable ON itemTable.idItemStatus = itemStatusTypeTable.idItemStatusType')
    item_image = DatabaseInstance.executeSelectMultipleQuery('SELECT Image FROM ItemImage')

    return render_template('admin_report.html', allProducts=allProducts, item_image=item_image)


@app.route('/ban/<itemId>', methods=['GET', 'POST'])
def admin_ban(itemId):
    if sm.isLoggedIn(session) is False:
        return redirect(url_for('landing'))
    if not ac.hasAccess(session['role'], "admin_ban"):
        return abort(404)

    item_status = DatabaseInstance.executeSelectOneQueryWithParameters(
        'SELECT idItemStatus FROM Item WHERE idItem = %s', [itemId])
    if item_status[0] == 4:
        DatabaseInstance.executeUpdateQueryWithParameters('UPDATE Item SET idItemStatus = %s WHERE idItem = %s',
                                                          [5, itemId])
    return redirect(url_for('admin_report'))


@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    errorMsg = ''
    if request.method == "POST":
        if recaptcha.verify():
            user = DatabaseInstance.executeSelectOneQueryWithParameters(
                'SELECT idUser, Email, MobileNumber, DisplayName FROM User WHERE Email=%s', [request.form.get('email')])
            entry = DatabaseInstance.executeSelectOneQueryWithParameters('SELECT * FROM UniqueURL WHERE Email=%s',
                                                                         [request.form.get('email')])
            if user is not None and entry is None:
                uniqueId = uuid.uuid4().hex
                byteData = {"id": user[0], "mobile": user[2]}
                DatabaseInstance.executeInsertQueryWithParameters(
                    'INSERT INTO UniqueURL (idUniqueURL, ByteData, Email, Type) VALUES (%s, %s, %s, %s)',
                    [uniqueId, zlib.compress(json.dumps(byteData).encode()), request.form.get('email'),
                     "ForgetPassword"]
                )
                emailMsg = user[
                               3] + ",\n\nYour password reset link is: " + "dabestteam.sitict.net/new_password/" + uniqueId
                SendGrid.send_email(user[1], "Let's Bid - Forget Password", emailMsg)
            return render_template('email_verification.html')
        else:
            errorMsg = 'Please fill out the ReCaptcha.'

    return render_template('forget_password.html', errorMsg=errorMsg)


@app.route('/new_password/<pwId>', methods=['GET', 'POST'])
def new_password(pwId):
    entry = DatabaseInstance.executeSelectOneQueryWithParameters('SELECT * FROM UniqueURL WHERE idUniqueURL=%s', [pwId])
    if entry is None or entry[3] != "ForgetPassword":
        abort(404)

    byteData = json.loads(zlib.decompress(entry[1]).decode("utf-8"))
    errorMsg = ''
    if request.method == "POST":
        OTPKey = DatabaseInstance.executeSelectOneQueryWithParameters("SELECT OTPKey FROM UserPass WHERE idUser=%s",
                                                                      [byteData["id"]])[0]
        if pyotp.TOTP(OTPKey).verify(request.form.get('otp_code')):
            password = request.form.get('newPassword')
            confirmPassword = request.form.get('confirmNewPassword')
            if password != confirmPassword:
                errorMsg = "Password and Confirm Password does not match!"
            else:
                formPassword = saltPepperHash(byteData["mobile"], Pepper, password)
                DatabaseInstance.executeUpdateQueryWithParameters(
                    'UPDATE UserPass SET Password = %s, LastUpdateDate = %s WHERE idUser = %s',
                    [formPassword, dt.today().strftime('%Y-%m-%d %H:%M:%S'), byteData["id"]])
                DatabaseInstance.executeDeleteQueryWithParameters('DELETE FROM UniqueURL WHERE idUniqueURL=%s', [pwId])
                return redirect(url_for('login'))
        else:
            errorMsg = "OTP Invalid!"
    return render_template('new_password.html', errorMsg=errorMsg)


@app.errorhandler(404)
def page_not_found(e):
    errorMsg = 'ERROR 404  - Page not found'
    errorDetails = 'The page you are looking for might have been removed or had its name changed or temporary unavailable.'
    if request.path.startswith('/admin/'):
        return render_template('error_page.html', errorMsg=errorMsg, errorDetails=errorDetails), 404
    else:
        return render_template('error_page.html', errorMsg=errorMsg, errorDetails=errorDetails), 404


@app.errorhandler(405)
def method_not_allowed(e):
    errorMsg = 'ERROR 405 - Method Not Allowed'
    errorDetails = 'The request method POST is inappropriate for the URL.'
    if request.path.startswith('/api/'):
        return render_template('error_page.html', errorMsg=errorMsg, errorDetails=errorDetails), 405
    else:
        return render_template('error_page.html', errorMsg=errorMsg), 405


@app.errorhandler(500)
def internal_server_error(e):
    errorMsg = 'ERROR 500 - Internal Server Error'
    errorDetails = 'The server encountered an internal error or misconfiguration, and was unable to complete your request.'
    return render_template('error_page.html', errorMsg=errorMsg, errorDetails=errorDetails), 500


def saltPepperHash(salt, pepper, text):
    return hashlib.sha256((str(pepper) + str(salt) + str(text)).encode()).hexdigest()


def fakeUser():
    return DatabaseInstance.getUserDetailsWithoutPicByEmail(fake_user)


def decodePic(pic64):
    if pic64:
        return b64encode(pic64).decode("utf-8")
    else:
        return ""


def formatDT(date):
    if date:
        return date.strftime('%d-%b-%Y')
    else:
        return ""


app.jinja_env.filters['formatDT'] = formatDT
app.jinja_env.filters['decodePic'] = decodePic

if __name__ == '__main__':
    app.run(host=os.environ.get('HOST_IP'), port=int(os.environ.get('HOST_PORT')), debug=os.environ.get('DEBUG'))
