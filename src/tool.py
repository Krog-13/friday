from datetime import datetime

async def exist_user(user_uid, db):
    """
    Check exist user
    """
    personal_user = db.user_exists(user_uid)
    return personal_user if personal_user else False


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
    Get children category
    """
    cat_child = db.category_children(parent_id)
    return cat_child


async def get_user(uuid, db):
    """
    Get a user
    """
    user = db.get_user(uuid)
    return user


async def set_order(data: dict, user_id, db):
    """
    Add orders
    """
    values = []
    # prepare param
    for item in [user_id, data["problem"], "В обработке", datetime.now(), data["category_id"]]:
        values.append(item)
    db.add_orders(tuple(values))


async def get_orders(user_id, db):
    """
    Get orders
    """
    all_orders = db.get_orders(user_id)
    return all_orders
