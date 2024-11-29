from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from screens import LoginScreen, ProductListScreen, AddProductScreen, ProductDetailScreen, RegistrationScreen, \
    TableSelectionScreen, UserProfileScreen, TableManagementScreen, AdminScreen, UserScreen, UsersTableScreen, \
    UsersDetailScreen, PasswordResetScreen, PasswordResetConfirmScreen
from database import create_db, add_user
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout

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
        self.screen_manager.add_widget(UsersTableScreen(name="users_list_screen"))
        self.screen_manager.add_widget(UsersDetailScreen(name="users_detail_screen"))
        self.screen_manager.add_widget(AddProductScreen(name="add_product_screen"))
        self.screen_manager.add_widget(AdminScreen(name="admin_screen"))
        self.screen_manager.add_widget(UserScreen(name="user_screen"))
        self.screen_manager.add_widget(PasswordResetScreen(name="password_reset_screen"))
        self.screen_manager.add_widget(PasswordResetConfirmScreen(name="password_reset_confirm_screen"))
        # self.screen_manager.add_widget(TableManagementScreen(user_role="admin", name="table_management"))

        # Добавление кнопки профиля и переключателя темы
        self.add_profile_and_theme_switcher()

        return self.screen_manager

    def add_profile_and_theme_switcher(self):
        for screen in self.screen_manager.screens:
            layout = MDBoxLayout(orientation="horizontal", size_hint=(1, None), height=50, pos_hint={'top': 1})

            # Создание переключателя темы с иконкой
            theme_switcher = MDIconButton(
                icon="theme-light-dark",
                pos_hint={"center_x": 0.9, "center_y": 0.5},
                on_release=self.toggle_theme
            )

            layout.add_widget(theme_switcher)

            # Добавляем кнопку профиля только на экраны, кроме логина и регистрации
            if screen.name not in ["login_screen", "registration_screen", "password_reset_screen", "password_reset_confirm_screen"]:
                profile_button = MDIconButton(
                    icon="account",
                    pos_hint={"center_x": 0.8, "center_y": 0.5},
                    on_release=self.show_profile
                )
                layout.add_widget(profile_button)

            screen.add_widget(layout)

    def show_profile(self, instance):
        # Показать информацию о профиле
        self.screen_manager.current = "user_profile_screen"

    def toggle_theme(self, instance):
        # Переключение между светлой и тёмной темой
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

if __name__ == "__main__":
    MyApp().run()
