async def exist_user(user_uid, db):
    """
    Check exist user
    """
    personal_uid = db.user_exists(user_uid)
    return True if personal_uid else False


async def add_user(data, user_uid, db):
    """
    Add new user
    """
    personal_data = (str(user_uid), True)
    order_key = ["fullname", "email", "phone", "manager", "user_language"]
    for key in order_key:
        personal_data += tuple((data[key],))
    db.add_user(personal_data)


async def cat_child(parent_id, db):
    """
    Check exist user
    """
    cat_child = db.category_children(parent_id)
    return cat_child


async def get_user(uuid, db):
    """
    Check exist user
    """
    user = db.get_user(uuid)
    return user