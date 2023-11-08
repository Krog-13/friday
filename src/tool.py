from datetime import datetime, timedelta

# final status
_END_STATUS = "Готов"


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


async def set_order(data: dict, user_id, order_id, db):
    """
    Add orders
    """
    values = []
    # prepare param
    for item in [user_id, data["problem"], order_id, "Классификация", datetime.now(), data["category_id"]]:
        values.append(item)
    db.add_orders(tuple(values))


async def get_orders(user_id, active, db):
    """
    Get orders
    """
    all_orders = db.get_orders(values=(user_id, active))
    return all_orders


async def email_update(user_id, email, db):
    """
    Email Update
    """
    all_orders = db.email_update(values=(email, str(user_id)))
    return all_orders


async def update_status_order(order, current_status, db, query_date):
    """
    Update status accept from api (smax)
    """

    if order[3] != current_status:
        if current_status == _END_STATUS:
            db.update_orders(values=(current_status, datetime.fromtimestamp(query_date/1000000), order[0]))
        else:
            db.update_orders(values=(current_status, None, order[0]))
    if order[6]:
        if (datetime.now() - order[6]) > timedelta(days=1):
            db.set_archive_order(values=(False, order[0]))
