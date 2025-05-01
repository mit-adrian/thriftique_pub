

def detectUser(user):
    if user.role == 0 and user.is_superadmin:
        redirectUrl = '/admin'
    elif user.role == 1:
        redirectUrl = 'vendorDashboard'
    elif user.role == 2:
        redirectUrl = 'customerDashboard'
    return redirectUrl
