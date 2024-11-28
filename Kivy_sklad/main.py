from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from screens import LoginScreen, ProductListScreen, AddProductScreen, ProductDetailScreen, RegistrationScreen
from database import create_db, add_user

class MyApp(MDApp):
    def build(self):
        self.screen_manager = ScreenManager()

        # Создание базы данных и пользователя по умолчанию
        create_db()
        add_user("admin", "admin", "admin", "admin@example.com")

        # Добавление экранов

        self.screen_manager.add_widget(LoginScreen(name="login_screen"))
        self.screen_manager.add_widget(RegistrationScreen(name="registration_screen"))
        self.screen_manager.add_widget(ProductListScreen(name="product_list_screen"))
        self.screen_manager.add_widget(ProductDetailScreen(name="product_detail_screen"))
        self.screen_manager.add_widget(AddProductScreen(name="add_product_screen"))
        self.screen_manager.add_widget(ProductDetailScreen(name="product_detail_screen"))

        return self.screen_manager

if __name__ == "__main__":
    MyApp().run()
