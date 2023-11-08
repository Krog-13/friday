INIT_DB = """ create table users (
	id serial PRIMARY KEY,
	personal_uid int NOT null,
	email varchar(128) NOT null,
	phone_number varchar(68),
	full_name varchar(255),
	manager varchar(255),
	user_language varchar(28),
	status boolean NOT null
);
create table service (
	id serial PRIMARY KEY,
	short_name varchar(128),
	description text,
	parent_id int REFERENCES service(id) on delete CASCADE 
)

create table orders(
	id serial PRIMARY KEY not null,
	order_msg text,
	order_number varchar(128),
	order_status varchar(128),
	order_date timestamp not null,
	user_id int,
	service_id int,
	constraint user_order_fk FOREIGN KEY(user_id) REFERENCES users(id),
	constraint service_order_fk FOREIGN KEY(service_id) REFERENCES service(id)
)

"""

user_exist = "SELECT full_name, email, phone_number, manager FROM users WHERE personal_uid=%s"
get_user = "SELECT * FROM users WHERE personal_uid=%s"
user_add = "INSERT INTO users (personal_uid, status, full_name, email, phone_number, manager, user_language) VALUES (%s, %s, %s, %s, %s, %s, %s)"
order_add = "INSERT INTO orders (user_id, order_msg, order_number, order_status, order_date, service_id) VALUES (%s, %s, %s, %s, %s, %s)"

category_parent = "SELECT * FROM service WHERE parent_id is null"
category_child = "SELECT * FROM service WHERE parent_id=%s"

email_update = "UPDATE users SET email=%s where personal_uid=%s"
fullname_update = "UPDATE users SET full_name=%s where personal_uid=%s"
phone_update = "UPDATE users SET phone_number=%s where personal_uid=%s"
manager = "UPDATE users SET manager=%s where personal_uid=%s"

order_update = "UPDATE orders SET order_status=%s, order_date_closed=%s where id=%s"
order_set_archive = "UPDATE orders SET active=%s where id=%s"


get_orders = "select orders.id, order_date, order_number, order_status, order_msg, short_name, order_date_closed from orders left join service on orders.service_id = service.id where user_id in (select id from users where personal_uid=%s and active=%s)"
