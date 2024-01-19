from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.app import App
import mysql.connector
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color
from kivy.uix.spinner import SpinnerOption, Spinner



# Función para ejecutar consultas SQL
def execute_query(query):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='colombia123',
        database='escalas'
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


# Clase para las opciones personalizadas del Spinner
class CustomSpinnerOption(Button):
    pass


# Clase principal del Spinner personalizado
class CustomSpinner(Spinner):
    pass


# Clase para los indicadores luminosos circulares
class IndicatorWidget(Widget):
    def __init__(self, **kwargs):
        super(IndicatorWidget, self).__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 1)  # Color blanco (puedes ajustarlo)
            self.indicator = Ellipse(pos=self.pos, size=(20, 20))  # Ajusta el tamaño según tus necesidades


# Pantalla principal
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'
        self.image = Image(source='C:\\Users\\Josed\\OneDrive\\Escritorio\\Proyecto\\Proyecto\\IMG.jpg')
        self.add_widget(self.image)
        self.username_input = TextInput(multiline=False, size_hint=(0.5, 0.05), pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.add_widget(self.username_input)
        self.password_input = TextInput(multiline=False, size_hint=(0.5, 0.05), pos_hint={'center_x': 0.5, 'center_y': 0.6}, password=True)
        self.add_widget(self.password_input)
        self.login_button = Button(text='Login', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.login_button.bind(on_press=self.login)
        self.add_widget(self.login_button)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        if self.verify_login(username, password):
            App.get_running_app().root.switch_screen('logged_in', username)
        else:
            print("Nombre de usuario o contraseña incorrectos")

    def verify_login(self, username, password):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='colombia123',
            database='usuarios'
        )
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None
    
class LoggedInScreen(Screen):
    def __init__(self, username, **kwargs):
        super(LoggedInScreen, self).__init__(**kwargs)
        self.name = 'logged_in'
        self.orientation = 'vertical'
        
        title_label = Label(text=f'Sistema de Entrenamiento para el Aprendizaje Lúdico de la Trompeta\nBienvenido, {username}', size_hint=(1, 0.2))
        self.add_widget(title_label)
        
        scales_block = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))
        scales_label = Label(text='Escalas:')
        escalas_mayores = ["Do Mayor", "Re Mayor", "Mi Mayor", "Fa Mayor", "Sol Mayor", "La Mayor", "Si Mayor"]
        self.scales_spinner = Spinner(text='Seleccione una escala', values=escalas_mayores, size_hint=(0.6, 1))
        scales_block.add_widget(scales_label)
        scales_block.add_widget(self.scales_spinner)
        self.add_widget(scales_block)
        
        self.scales_spinner.bind(on_text=self.handle_spinner_selection)

    def handle_spinner_selection(self, instance, value):
        selected_scale = value
        print(f"Debug: Selected Scale: {selected_scale}")
        self.switch_to_escalas_screen(selected_scale)

    def switch_to_escalas_screen(self, selected_scale):
        print(f"Debug: Switching to Escalas Screen with Scale: {selected_scale}")
        screen_manager = App.get_running_app().root
        screen_manager.current = 'escalas'


class EscalasScreen(Screen):
    def __init__(self, username, selected_scale, **kwargs):
        super().__init__(**kwargs)
        self.name = 'escalas'
        self.username = username
        self.selected_scale = selected_scale
        escalas_layout = BoxLayout(orientation='vertical')
        username_label = Label(text=f'Usuario: {username}')
        escalas_layout.add_widget(username_label)
        selected_scale_label = Label(text=f'Opción seleccionada: {selected_scale}')
        escalas_layout.add_widget(selected_scale_label)
        indicators_layout = BoxLayout(orientation='horizontal')
        for _ in range(3):
            indicator = IndicatorWidget()
            indicators_layout.add_widget(indicator)
        escalas_layout.add_widget(indicators_layout)
        self.add_widget(escalas_layout)


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

        self.login_screen = Screen(name='login')
        self.logged_in_screen = Screen(name='logged_in')

        self.login_screen.add_widget(LoginScreen())
        self.logged_in_screen.add_widget(LoggedInScreen(username=''))

        self.add_widget(self.login_screen)
        self.add_widget(self.logged_in_screen)

    def switch_screen(self, screen_name, username='', selected_scale=''):
        if screen_name == 'escalas':
            # Crea la instancia de EscalasScreen con la escala seleccionada y el nombre de usuario
            escalas_screen = EscalasScreen(name='escalas', username=username, selected_scale=selected_scale)
            
            # Cambia a la pantalla de escalas
            self.switch_to(escalas_screen)
        elif screen_name == 'logged_in':
            # Para otras pantallas, simplemente agrega el widget correspondiente
            self.current = screen_name

class LoginApp(App):
    def build(self):
        return ScreenManagement()


if __name__ == '__main__':
    LoginApp().run()
