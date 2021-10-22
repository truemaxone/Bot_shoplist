import psycopg2
import config


class DB:
    def __init__(self):
        self.connection = psycopg2.connect(dbname=config.dbname, user=config.user, password=config.password)
        self.connection.autocommit = True
        self.cur = self.connection.cursor()

    def check_existence(self, user_id, user_name):
        with self.connection:
            self.cur.execute(""" SELECT user_id FROM products_data """)
            records = self.cur.fetchall()
            check_list = [record[0] for record in records]
            if user_id in check_list:
                # Достаем список из БД
                self.cur.execute(""" SELECT list_of_products FROM products_data WHERE user_id = %s""", (user_id,))
                list_of_products = list(self.cur.fetchone()[0].split(', '))
                return list_of_products
            else:
                self.cur.execute(""" INSERT INTO products_data (user_id, user_name) VALUES(%s, %s) """,
                                 (user_id, user_name))

    def db_recourse(self, message):
        with self.connection:
            self.cur.execute(""" SELECT list_of_products FROM products_data WHERE user_id = %s""",
                             (message.from_user.id,))
            list_of_products = list(self.cur.fetchone()[0].split(', '))
            return list_of_products

    def db_recourse_call(self, call):
        with self.connection:
            self.cur.execute(""" SELECT list_of_products FROM products_data WHERE user_id = %s""",
                             (call.from_user.id,))
            list_of_products = list(self.cur.fetchone()[0].split(', '))
            return list_of_products

    def db_update(self, message, list_of_products):
        with self.connection:
            self.cur.execute(""" UPDATE products_data SET list_of_products = %s WHERE user_id = %s """, (
                ', '.join(list_of_products), message.from_user.id))

    def db_update_call(self, call, list_of_products):
        with self.connection:
            self.cur.execute(""" UPDATE products_data SET list_of_products = %s WHERE user_id = %s """, (
                ', '.join(list_of_products), call.from_user.id))
