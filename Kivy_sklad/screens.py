from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from database import *
from kivy.uix.dropdown import DropDown
from kivymd.uix.menu import MDDropdownMenu


class UsersTableScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=(50, 150), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Карточка для списка пользователей
        card = MDCard(orientation='vertical', padding=20, spacing=20, size_hint=(0.8, None), height=400, radius=[15,])

        title = MDLabel(text="Список пользователей", font_size=24, halign="center", size_hint_y=None, height=50)
        card.add_widget(title)

        self.scroll_view = ScrollView()
        self.product_list = MDList()
        self.scroll_view.add_widget(self.product_list)
        card.add_widget(self.scroll_view)

        self.add_product_button = MDRaisedButton(text="Назад", pos_hint={'center_x': 0.5}, size_hint_x=0.6, on_release=self.go_back)
        card.add_widget(self.add_product_button)

        layout.add_widget(card)
        self.add_widget(layout)

        self.load_products()

    def go_back(self, instance):
        """Возвращается на экран списка товаров"""
        self.manager.current = 'product_list_screen'  # Переход на экран списка товаров

    def load_products(self):
        products = get_all_users()
        self.product_list.clear_widgets()

        for product in products:
            item = OneLineListItem(text=f"{product[1]} - Пароль: {product[2]}")
            item.bind(on_release=lambda x, product=product: self.show_product_detail(product))
            self.product_list.add_widget(item)

    def show_product_detail(self, product):
        self.manager.get_screen('users_detail_screen').display_product(product[0])
        self.manager.current = "users_detail_screen"

    def refresh_product_list(self):
        self.load_products()


class UsersDetailScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=(50, 150), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Карточка для деталей пользователя
        card = MDCard(orientation='vertical', padding=20, spacing=20, size_hint=(0.8, None), height=350, radius=[15,])

        self.label = MDLabel(halign='center', theme_text_color="Secondary", size_hint_y=None, height=40)
        card.add_widget(self.label)

        self.quantity_input = MDTextField(hint_text="Введите новый пароль", multiline=False, size_hint_y=None, height=40)
        card.add_widget(self.quantity_input)

        self.save_button = MDRaisedButton(text="Сохранить изменения", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        self.save_button.bind(on_release=self.save_changes)
        card.add_widget(self.save_button)

        self.back_button = MDRaisedButton(text="Назад", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        self.back_button.bind(on_release=self.go_back)
        card.add_widget(self.back_button)

        layout.add_widget(card)
        self.add_widget(layout)

    def display_product(self, product_id):
        """Отображает информацию о продукте на основе его ID"""
        self.product_id = product_id

        product = get_user_by_id(product_id)

        if product:
            self.label.text = f"Логин: {product[1]}\nПароль: {product[2]}\n"
            self.quantity_input.text = str(product[2])  # Отображаем текущее количество товара

    def save_changes(self, instance):
        """Сохраняет изменения в количестве товара"""
        new_quantity = self.quantity_input.text

        if new_quantity.isdigit():  # Проверяем, что введено число
            new_quantity = int(new_quantity)
            update_user(self.product_id, new_quantity)
            self.manager.get_screen('users_list_screen').refresh_product_list()  # Обновляем список товаров
            self.go_back(None)
        else:
            self.label.text = "Введите корректный пароль."

    def go_back(self, instance):
        """Возвращается на экран списка товаров"""
        self.manager.current = 'users_list_screen'  # Переход на экран списка товаров


class AdminScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=(50, 150), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Карточка для админского экрана
        card = MDCard(orientation='vertical', padding=20, spacing=20, size_hint=(0.8, None), height=200, radius=[15,])

        title = MDLabel(text="Добро пожаловать, администратор!", halign="center", font_size=24)
        card.add_widget(title)

        btn = MDRaisedButton(text="Управление таблицами", pos_hint={'center_x': 0.5}, size_hint_x=0.6, on_release=self.go_to_tables)
        card.add_widget(btn)

        layout.add_widget(card)
        self.add_widget(layout)

    def go_to_tables(self, instance):
        self.manager.transition.direction = "left"
        self.manager.current = "table_management"


class UserScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=(50, 150), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Карточка для пользовательского экрана
        card = MDCard(orientation='vertical', padding=20, spacing=20, size_hint=(0.8, None), height=200, radius=[15,])

        title = MDLabel(text="Добро пожаловать, пользователь!", halign="center", font_size=24)
        card.add_widget(title)

        btn = MDRaisedButton(text="Просмотр таблиц", pos_hint={'center_x': 0.5}, size_hint_x=0.6, on_release=self.go_to_tables)
        card.add_widget(btn)

        layout.add_widget(card)
        self.add_widget(layout)

    def go_to_tables(self, instance):
        self.manager.transition.direction = "left"
        self.manager.current = "table_management"


class TableManagementScreen(MDScreen):
    def __init__(self, user_role, **kwargs):
        super().__init__(**kwargs)
        self.user_role = user_role
        self.current_table = "products"  # Значение по умолчанию
        self.table_names = ["products", "users", "transactions"]  # Таблицы в БД

        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=(50, 150), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Карточка для управления таблицами
        card = MDCard(orientation='vertical', padding=20, spacing=20, size_hint=(0.8, None), height=400, radius=[15,])

        self.dropdown_button = MDRaisedButton(
            text=self.current_table,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            on_release=self.open_dropdown_menu
        )
        card.add_widget(self.dropdown_button)

        menu_items = [
            {
                "text": table,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=table: self.switch_table(x),
            } for table in self.table_names
        ]

        self.dropdown_menu = MDDropdownMenu(
            caller=self.dropdown_button,
            items=menu_items,
            width_mult=4,
        )

        self.add_product_button = MDRaisedButton(text="Добавить товар", pos_hint={'center_x': 0.5}, size_hint_x=0.6, on_release=self.go_to_add_product_screen)
        card.add_widget(self.add_product_button)

        self.data_table = MDDataTable(
            column_data=[],
            row_data=[]
        )
        card.add_widget(self.data_table)

        layout.add_widget(card)
        self.add_widget(layout)
        self.load_table_data(self.current_table)

    def go_to_add_product_screen(self, instance):
        self.manager.current = 'add_product_screen'

    def open_dropdown_menu(self, *args):
        self.dropdown_menu.open()

    def switch_table(self, table_name):
        self.current_table = table_name
        self.dropdown_button.text = self.current_table
        self.dropdown_menu.dismiss()
        self.load_table_data(self.current_table)

    def load_table_data(self, table_name):
        data = get_table_data(table_name)
        if data["columns"]:
            self.data_table.column_data = [(col, dp(30)) for col in data["columns"]]
        else:
            self.data_table.column_data = []

        if data["rows"]:
            self.data_table.row_data = data["rows"]
        else:
            self.data_table.row_data = []





class UserProfileScreen(MDScreen):
    def __init__(self, username, role, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.role = role

        # Основной макет
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=20)

        # Карточка для профиля пользователя
        card = MDCard(orientation='vertical', padding=20, spacing=20, size_hint=(0.8, None), height=350, radius=[15,])

        # Заголовок
        card.add_widget(MDLabel(
            text="Профиль пользователя",
            halign="center",
            font_style="H4"
        ))

        # Имя пользователя
        card.add_widget(MDLabel(
            text=f"Имя пользователя: {self.username}",
            halign="center",
            font_style="Subtitle1"
        ))

        # Роль пользователя
        card.add_widget(MDLabel(
            text=f"Роль: {self.role}",
            halign="center",
            font_style="Subtitle1"
        ))

        # Кнопка настройки темы
        theme_button = MDRaisedButton(
            text="Переключить тему",
            pos_hint={"center_x": 0.5},
            on_release=self.toggle_theme
        )
        card.add_widget(theme_button)

        # Кнопка выхода
        logout_button = MDRaisedButton(
            text="Выйти из аккаунта",
            pos_hint={"center_x": 0.5},
            on_release=self.logout
        )
        card.add_widget(logout_button)

        layout.add_widget(card)
        self.add_widget(layout)

    def toggle_theme(self, instance):
        """Переключение между светлой и тёмной темой."""
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

    def logout(self, instance):
        """Функция выхода из аккаунта."""
        self.manager.current = "login"  # Переключение на экран входа






class TableDataScreen(MDScreen):
    def __init__(self, table_name, **kwargs):
        super().__init__(**kwargs)
        self.table_name = table_name
        self.data = self.get_table_data(table_name)

        # Таблица для отображения данных
        self.table = MDDataTable(
            column_data=[(col, dp(30)) for col in self.data["columns"]],
            row_data=self.data["rows"]
        )
        self.add_widget(self.table)

class TableSelectionScreen(MDScreen):
    def __init__(self, user_role, **kwargs):
        super().__init__(**kwargs)
        self.user_role = user_role  # 'user' или 'admin'
        self.dropdown = DropDown()

        # Таблицы, доступные пользователю
        if self.user_role == 'admin':
            tables = ['users', 'products', 'orders']
        else:
            tables = ['products', 'orders']

        for table in tables:
            btn = MDRaisedButton(
                text=table,
                on_release=lambda btn: self.select_table(btn.text)
            )
            self.dropdown.add_widget(btn)

        self.main_button = MDRaisedButton(
            text="Выберите таблицу",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            on_release=self.dropdown.open
        )
        self.add_widget(self.main_button)

    def select_table(self, table_name):
        self.dropdown.dismiss()
        self.main_button.text = f"Текущая таблица: {table_name}"
        # Загрузите данные из таблицы и отобразите их
        self.load_table_data(table_name)

    def load_table_data(self, table_name):
        # Здесь логика для отображения данных таблицы
        print(f"Данные из таблицы {table_name} загружаются...")

from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=(50, 150), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Карточка для авторизации
        card = MDCard(orientation='vertical', padding=20, spacing=20, size_hint=(0.8, None), height=400, radius=[15,])

        title = MDLabel(text="Авторизация", font_size=24, halign="center", size_hint_y=None, height=50)
        card.add_widget(title)

        self.username_input = MDTextField(hint_text="Имя пользователя", pos_hint={'center_x': 0.5}, size_hint_x=0.8)
        self.password_input = MDTextField(hint_text="Пароль", password=True, pos_hint={'center_x': 0.5}, size_hint_x=0.8)

        card.add_widget(self.username_input)
        card.add_widget(self.password_input)

        button_layout = MDBoxLayout(spacing=10, size_hint_y=None, height=100)
        self.login_button = MDRaisedButton(text="Войти", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        self.login_button.bind(on_release=self.login)
        button_layout.add_widget(self.login_button)

        self.register_button = MDRaisedButton(text="Зарегистрироваться", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        self.register_button.bind(on_release=self.go_to_registration)
        button_layout.add_widget(self.register_button)

        self.reset_password_button = MDRaisedButton(text="Восстановить пароль", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        self.reset_password_button.bind(on_release=self.go_to_password_reset)
        button_layout.add_widget(self.reset_password_button)

        card.add_widget(button_layout)

        layout.add_widget(card)
        self.add_widget(layout)

    def go_to_registration(self, instance):
        # Переход на экран регистрации
        self.manager.current = "registration_screen"

    def go_to_password_reset(self, instance):
        # Переход на экран восстановления пароля
        self.manager.current = "password_reset_screen"

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        # Проверяем, если данные введены
        if not username or not password:
            self.show_dialog("Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Проверяем данные в базе данных
        if check_credentials(username, password):
            role = check_role(username)
            if role == "admin":
                self.manager.current = "admin_screen"
            else:
                self.manager.current = "user_screen"
                self.manager.get_screen('product_list_screen').hide_button()

            # Передача логина и роли в UserProfileScreen
            user_profile_screen = UserProfileScreen(username=username, role=role, name="user_profile_screen")
            self.manager.add_widget(user_profile_screen)
            self.manager.current = "product_list_screen"  # Переключаем на главный экран
        else:
            self.show_dialog("Ошибка", "Неверное имя пользователя или пароль.")

    def show_dialog(self, title, message):
        """Отображение диалога с ошибкой."""
        self.dialog = MDDialog(
            title=title,
            text=message,
            size_hint=(0.8, 1),
            buttons=[MDRaisedButton(text="OK", on_release=self.close_dialog)]
        )
        self.dialog.open()

    def close_dialog(self, instance):
        """Закрытие диалога."""
        self.dialog.dismiss()








class RegistrationScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=(50, 150), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Карточка для регистрации
        card = MDCard(orientation='vertical', padding=20, spacing=20, size_hint=(0.8, None), height=400, radius=[15,])

        title = MDLabel(text="Регистрация", font_size=24, halign="center", size_hint_y=None, height=50)
        card.add_widget(title)

        self.username_input = MDTextField(hint_text="Имя пользователя", pos_hint={'center_x': 0.5}, size_hint_x=0.8)
        self.password_input = MDTextField(hint_text="Пароль", password=True, pos_hint={'center_x': 0.5}, size_hint_x=0.8)
        self.email_input = MDTextField(hint_text="Электронная почта", pos_hint={'center_x': 0.5}, size_hint_x=0.8)

        card.add_widget(self.username_input)
        card.add_widget(self.password_input)
        card.add_widget(self.email_input)

        self.register_button = MDRaisedButton(text="Зарегистрироваться", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        self.register_button.bind(on_release=self.register)
        card.add_widget(self.register_button)

        self.login_button = MDRaisedButton(text="Уже есть аккаунт? Войти", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        self.login_button.bind(on_release=self.go_to_login)
        card.add_widget(self.login_button)

        layout.add_widget(card)
        self.add_widget(layout)

    def go_to_login(self, instance):
        # Переход на экран логина
        self.manager.current = "login_screen"

    def close_dialog(self, instance):
        if hasattr(self, "dialog") and self.dialog:
            self.dialog.dismiss()
            self.dialog = None

    def register(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        email = self.email_input.text

        # Проверяем, если данные введены
        if not username or not password or not email:
            self.show_dialog("Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Проверяем, если пользователь уже существует
        if self.check_user_exists(username, password):
            self.show_dialog("Ошибка", "Пользователь с таким именем уже существует.")
            return

        # Сохраняем нового пользователя в базе данных
        save_user_to_db(username, password, "user", email)
        self.show_dialog("Успех", "Регистрация прошла успешно!")
        self.manager.current = "login_screen"  # Переключаем на экран входа

    def check_user_exists(self, username, password):
        return check_credentials(username, password)

    def show_dialog(self, title, message):
        """Отображение диалога с сообщением."""
        self.dialog = MDDialog(
            title=title,
            text=message,
            size_hint=(0.8, 1),
            buttons=[MDRaisedButton(text="OK", on_release=self.close_dialog)]
        )
        self.dialog.open()


class PasswordResetScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=(50, 150), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Карточка для восстановления пароля
        card = MDCard(orientation='vertical', padding=20, spacing=20, size_hint=(0.8, None), height=300, radius=[15,])

        title = MDLabel(text="Восстановление пароля", font_size=24, halign="center", size_hint_y=None, height=50)
        card.add_widget(title)

        self.email_input = MDTextField(hint_text="Электронная почта", pos_hint={'center_x': 0.5}, size_hint_x=0.8)
        card.add_widget(self.email_input)

        self.reset_button = MDRaisedButton(text="Восстановить пароль", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        self.reset_button.bind(on_release=self.reset_password)
        card.add_widget(self.reset_button)

        layout.add_widget(card)
        self.add_widget(layout)

    def reset_password(self, instance):
        email = self.email_input.text
        success = reset_user_password(email)

        if success:
            self.show_dialog("Успех", "Инструкции по восстановлению пароля были отправлены на вашу почту.")
            self.manager.current = "password_reset_confirm_screen"  # Переход на экран подтверждения восстановления пароля
        else:
            self.show_dialog("Ошибка", "Пользователь с таким email не найден.")

    def show_dialog(self, title, message):
        """Отображение диалога с сообщением."""
        self.dialog = MDDialog(
            title=title,
            text=message,
            size_hint=(0.8, 1),
            buttons=[MDRaisedButton(text="OK", on_release=self.close_dialog)]
        )
        self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss()


class ProductListScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=(50, 150), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Карточка для списка продуктов
        card = MDCard(orientation='vertical', padding=20, spacing=20, size_hint=(0.8, None), height=400, radius=[15,])

        title = MDLabel(text="Список продуктов", font_size=24, halign="center", size_hint_y=None, height=50)
        card.add_widget(title)

        self.scroll_view = ScrollView()
        self.product_list = MDList()
        self.scroll_view.add_widget(self.product_list)
        card.add_widget(self.scroll_view)

        self.add_product_button = MDRaisedButton(text="Добавить товар", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        self.add_product_button.bind(on_release=self.go_to_add_product_screen)
        card.add_widget(self.add_product_button)

        self.users_button = MDRaisedButton(text="Пользователи", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        self.users_button.bind(on_release=self.go_to_users_table)
        card.add_widget(self.users_button)

        layout.add_widget(card)
        self.add_widget(layout)

        self.load_products()

    def hide_button(self):
        self.users_button.opacity = 0
        self.users_button.disabled = True

    def go_to_users_table(self, instance):
        self.manager.current = 'users_list_screen'

    def go_to_add_product_screen(self, instance):
        self.manager.current = 'add_product_screen'

    def load_products(self):
        products = get_all_products()
        self.product_list.clear_widgets()

        for product in products:
            item = OneLineListItem(text=f"{product[1]} - Кол-во: {product[2]}")
            item.bind(on_release=lambda x, product=product: self.show_product_detail(product))
            self.product_list.add_widget(item)

    def show_product_detail(self, product):
        self.manager.get_screen('product_detail_screen').display_product(product[0])
        self.manager.current = "product_detail_screen"

    def refresh_product_list(self):
        self.load_products()


class AddProductScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=(50, 150), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Карточка для добавления продукта
        card = MDCard(orientation='vertical', padding=20, spacing=20, size_hint=(0.8, None), height=350, radius=[15,])

        title = MDLabel(text="Добавить продукт", font_size=24, halign="center", size_hint_y=None, height=50)
        card.add_widget(title)

        self.name_input = MDTextField(hint_text="Название товара", pos_hint={'center_x': 0.5}, size_hint_x=0.8)
        self.quantity_input = MDTextField(hint_text="Количество", input_filter="int", pos_hint={'center_x': 0.5}, size_hint_x=0.8)
        self.location_input = MDTextField(hint_text="Цена", pos_hint={'center_x': 0.5}, size_hint_x=0.8)

        card.add_widget(self.name_input)
        card.add_widget(self.quantity_input)
        card.add_widget(self.location_input)

        self.add_button = MDRaisedButton(text="Добавить", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        self.add_button.bind(on_release=self.add_product)
        card.add_widget(self.add_button)

        layout.add_widget(card)
        self.add_widget(layout)

    def add_product(self, instance):
        name = self.name_input.text
        quantity = int(self.quantity_input.text)
        location = self.location_input.text
        add_product(name, quantity, location)
        self.manager.current = 'product_list_screen'
        self.manager.get_screen('product_list_screen').load_products()  # Обновляем список товаров


class ProductDetailScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=(50, 150), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Карточка для деталей продукта
        card = MDCard(orientation='vertical', padding=20, spacing=20, size_hint=(0.8, None), height=350, radius=[15,])

        self.label = MDLabel(halign='center', theme_text_color="Secondary", size_hint_y=None, height=40)
        card.add_widget(self.label)

        self.quantity_input = MDTextField(hint_text="Введите новое количество", multiline=False, size_hint_y=None, height=40)
        card.add_widget(self.quantity_input)

        self.save_button = MDRaisedButton(text="Сохранить изменения", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        self.save_button.bind(on_release=self.save_changes)
        card.add_widget(self.save_button)

        self.back_button = MDRaisedButton(text="Назад", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        self.back_button.bind(on_release=self.go_back)
        card.add_widget(self.back_button)

        layout.add_widget(card)
        self.add_widget(layout)

    def display_product(self, product_id):
        """Отображает информацию о продукте на основе его ID"""
        self.product_id = product_id
        product = get_product_by_id(product_id)

        if product:
            self.label.text = f"Название: {product[1]}\nОписание: {product[2]}\nЦена: {product[3]}"
            self.quantity_input.text = str(product[2])  # Отображаем текущее количество товара

    def save_changes(self, instance):
        """Сохраняет изменения в количестве товара"""
        new_quantity = self.quantity_input.text

        if new_quantity.isdigit():  # Проверяем, что введено число
            new_quantity = int(new_quantity)
            update_product(self.product_id, new_quantity)
            self.manager.get_screen('product_list_screen').refresh_product_list()  # Обновляем список товаров
            self.go_back(None)
        else:
            self.label.text = "Введите корректное количество товара."

    def go_back(self, instance):
        """Возвращается на экран списка товаров"""
        self.manager.current = 'product_list_screen'  # Переход на экран списка товаров


class PasswordResetScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=(50, 150), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        title = MDLabel(text="Восстановление пароля", font_size=24, size_hint_y=None, height=50)
        layout.add_widget(title)

        self.email_input = MDTextField(hint_text="Электронная почта", pos_hint={'center_x': 0.5}, size_hint_x=0.8)
        layout.add_widget(self.email_input)

        self.reset_button = MDRaisedButton(text="Восстановить пароль", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        self.reset_button.bind(on_release=self.reset_password)
        layout.add_widget(self.reset_button)

        self.add_widget(layout)

    def reset_password(self, instance):
        email = self.email_input.text
        success = reset_user_password(email)

        if success:
            self.show_dialog("Успех", "Инструкции по восстановлению пароля были отправлены на вашу почту.")
            self.manager.current = "password_reset_confirm_screen"  # Переход на экран подтверждения восстановления пароля
        else:
            self.show_dialog("Ошибка", "Пользователь с таким email не найден.")

    def show_dialog(self, title, message):
        """Отображение диалога с сообщением."""
        self.dialog = MDDialog(
            title=title,
            text=message,
            size_hint=(0.8, 1),
            buttons=[MDRaisedButton(text="OK", on_release=self.close_dialog)]
        )
        self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss()


class PasswordResetConfirmScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=(50, 150), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Карточка для подтверждения восстановления пароля
        card = MDCard(orientation='vertical', padding=20, spacing=20, size_hint=(0.8, None), height=350, radius=[15,])

        title = MDLabel(text="Сброс пароля", font_size=24, halign="center", size_hint_y=None, height=50)
        card.add_widget(title)

        self.code_input = MDTextField(hint_text="Код восстановления", pos_hint={'center_x': 0.5}, size_hint_x=0.8)
        card.add_widget(self.code_input)

        self.new_password_input = MDTextField(hint_text="Новый пароль", password=True, pos_hint={'center_x': 0.5}, size_hint_x=0.8)
        card.add_widget(self.new_password_input)

        self.confirm_button = MDRaisedButton(text="Подтвердить", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        self.confirm_button.bind(on_release=self.confirm_reset)
        card.add_widget(self.confirm_button)

        layout.add_widget(card)
        self.add_widget(layout)

    def confirm_reset(self, instance):
        code = self.code_input.text
        new_password = self.new_password_input.text
        success = confirm_password_reset(code, new_password)

        if success:
            self.show_dialog("Успех", "Ваш пароль был успешно изменен.")
            self.manager.current = "login_screen"
        else:
            self.show_dialog("Ошибка", "Неверный код восстановления или другие ошибки.")

    def show_dialog(self, title, message):
        """Отображение диалога с сообщением."""
        self.dialog = MDDialog(
            title=title,
            text=message,
            size_hint=(0.8, 1),
            buttons=[MDRaisedButton(text="OK", on_release=self.close_dialog)]
        )
        self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss()

