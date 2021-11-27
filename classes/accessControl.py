
rightsProfile = {
    # Admin
    1: [
        "profile",
        "admin",
        "admin_products",
        "admin_report",
        "admin_ban"
    ],
    # User
    2: [
        "profile",
        "products",
        "add_product",
        "product_page",
        "report_product",
        "e_wallet",
    ]
}


def hasAccess(userType, rights):
    return rights in rightsProfile[userType]

