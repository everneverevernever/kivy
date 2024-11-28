from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

from database import get_all_products, add_product, update_product, get_product, get_transactions, register_user, get_product_by_id, reset_user_password, check_credentials


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=(50, 150), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        title = MDLabel(text="Авторизация", font_size=24, size_hint_y=0.8, height=50, )
        layout.add_widget(title)

        self.username_input = MDTextField(hint_text="Имя пользователя", pos_hint={'center_x': 0.5}, size_hint_x=0.8)
        self.password_input = MDTextField(hint_text="Пароль", password=True, pos_hint={'center_x': 0.5}, size_hint_x=0.8)

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)

        self.login_button = MDRaisedButton(text="Войти", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        layout.add_widget(self.login_button)

        self.register_button = MDRaisedButton(text="Зарегистрироваться", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        self.register_button.bind(on_release=self.go_to_registration)
        self.login_button.bind(on_release=self.login)
        layout.add_widget(self.register_button)

        self.add_widget(layout)

    def go_to_registration(self, instance):
        # Переход на экран регистрации
        self.manager.current = "registration_screen"


    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        # Проверяем, если данные введены
        if not username or not password:
            self.show_dialog("Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Проверяем данные в базе данных
        if check_credentials(username, password):
            self.manager.current = "main_screen"  # Переключаем на главный экран
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
        layout = BoxLayout(orientation='vertical', spacing=20, padding=(50, 150), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        title = MDLabel(text="Регистрация", font_size=24, size_hint_y=None, height=50)
        layout.add_widget(title)

        self.username_input = MDTextField(hint_text="Имя пользователя", pos_hint={'center_x': 0.5}, size_hint_x=0.8)
        self.password_input = MDTextField(hint_text="Пароль", password=True, pos_hint={'center_x': 0.5}, size_hint_x=0.8)
        self.email_input = MDTextField(hint_text="Электронная почта", pos_hint={'center_x': 0.5}, size_hint_x=0.8)

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.email_input)

        self.register_button = MDRaisedButton(text="Зарегистрироваться", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        layout.add_widget(self.register_button)

        self.login_button = MDRaisedButton(text="Уже есть аккаунт? Войти", pos_hint={'center_x': 0.5}, size_hint_x=0.6)
        self.login_button.bind(on_release=self.go_to_login)
        layout.add_widget(self.login_button)

        self.add_widget(layout)

    def go_to_login(self, instance):
        # Переход на экран логина
        self.manager.current = "login_screen"

    def register(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text

        # Проверяем, если данные введены
        if not username or not password or not confirm_password:
            self.show_dialog("Ошибка", "Пожалуйста, заполните все поля.")
            return

        # Проверяем, если пароли совпадают
        if password != confirm_password:
            self.show_dialog("Ошибка", "Пароли не совпадают.")
            return

        # Проверяем, если пользователь уже существует
        if self.check_user_exists(username):
            self.show_dialog("Ошибка", "Пользователь с таким именем уже существует.")
            return

        # Сохраняем нового пользователя в базе данных
        self.save_user_to_db(username, password)
        self.show_dialog("Успех", "Регистрация прошла успешно!")
        self.manager.current = "login_screen"  # Переключаем на экран входа

    def check_user_exists(self, username):
        return check_credentials()

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
            print("Инструкции по восстановлению пароля были отправлены на вашу почту.")
        else:
            print("Пользователь с таким email не найден.")



class ProductListScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.add_widget(MDLabel(text="Список товаров", font_size=24, halign='center'))
        self.scroll_view = ScrollView()
        self.product_list = MDList()
        self.scroll_view.add_widget(self.product_list)
        layout.add_widget(self.scroll_view)
        self.load_products()
        self.add_widget(layout)

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




class AddProductScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Добавить товар", font_size=24))

        self.name_input = MDTextField(hint_text="Название товара")
        self.quantity_input = MDTextField(hint_text="Количество", input_filter="int")
        self.location_input = MDTextField(hint_text="Местоположение")
        self.add_button = MDRaisedButton(text="Добавить", on_release=self.add_product)

        self.add_widget(self.name_input)
        self.add_widget(self.quantity_input)
        self.add_widget(self.location_input)
        self.add_widget(self.add_button)

    def add_product(self, instance):
        name = self.name_input.text
        quantity = int(self.quantity_input.text)
        location = self.location_input.text
        add_product(name, quantity, location)
        self.manager.current = 'product_list_screen'


class ProductDetailScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Заголовок экрана
        self.label = MDLabel(halign='center', theme_text_color="Secondary", size_hint_y=None, height=40)
        self.layout.add_widget(self.label)

        # Поле для ввода нового количества
        self.quantity_input = MDTextField(hint_text="Введите новое количество", multiline=False, size_hint_y=None,
                                          height=40)
        self.layout.add_widget(self.quantity_input)

        # Кнопка для сохранения изменений
        self.save_button = MDRaisedButton(text="Сохранить изменения", size_hint=(None, None), size=(200, 50))
        self.save_button.bind(on_release=self.save_changes)
        self.layout.add_widget(self.save_button)

        # Кнопка для возврата назад
        self.back_button = MDRaisedButton(text="Назад", size_hint=(None, None), size=(200, 50))
        self.back_button.bind(on_release=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def display_product(self, product_id):
        """Отображает информацию о продукте на основе его ID"""
        self.product_id = product_id
        product = get_product_by_id(product_id)

        if product:
            # Отображаем название товара и описание, цену
            self.label.text = f"Название: {product[1]}\nОписание: {product[2]}\nЦена: {product[3]}"
            self.quantity_input.text = str(product[2])  # Отображаем текущее количество товара

    def save_changes(self, instance):
        """Сохраняет изменения в количестве товара"""
        new_quantity = self.quantity_input.text

        if new_quantity.isdigit():  # Проверяем, что введено число
            new_quantity = int(new_quantity)
            # Обновляем количество в базе данных
            update_product(self.product_id, new_quantity)
            self.go_back(None)
        else:
            self.label.text = "Введите корректное количество товара."

    def go_back(self, instance):
        """Возвращается на экран списка товаров"""
        self.manager.current = 'product_list_screen'  # Переход на экран списка товаров
