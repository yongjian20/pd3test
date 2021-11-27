
def storeUserDetails(session, details):
    session['id'] = details[0]
    session['role'] = details[1]
    session['email'] = details[2]
    session['mobile'] = details[3]
    session['birthDate'] = details[4]
    session['firstName'] = details[5]
    session['lastName'] = details[6]
    session['displayName'] = details[7]
    session['mailingAddress'] = details[8]
    session['deliveryAddress'] = details[9]
    session['joinDate'] = details[10]
    session['lastLoginDate'] = details[11]
    session['loginAttempts'] = details[12]
    session['ipAddress'] = details[13]
    session['otpStatus'] = details[14]

def isLoggedIn(session):
    if session.get('loggedIn'):
        return session['loggedIn']
    session.clear()
    return False

