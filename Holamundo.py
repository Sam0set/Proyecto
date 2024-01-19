from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.app import App
from kivy.uix.image import Image
import mysql.connector
from kivy.uix.spinner import Spinner

def execute_query(query):
    # Función para ejecutar consultas SQL
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
# Pantalla de inicio
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'

        self.image = Image(source='C:\\Users\\Josed\\OneDrive\\Escritorio\\Proyecto\\IMG.jpg')
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
        # Conectar a la base de datos MySQL (phpMyAdmin en este ejemplo)
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='colombia123',
            database='usuarios'
        )
        cursor = connection.cursor()

        # Verificar el login
        cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
        result = cursor.fetchone()

        # Cerrar la conexión a la base de datos
        cursor.close()
        connection.close()

        return result is not None

# Define the screen manager
sm = ScreenManager()
sm.add_widget(LoginScreen())

class LoggedInScreen(BoxLayout):
    def __init__(self, username, **kwargs):
        super(LoggedInScreen, self).__init__(**kwargs)

        self.orientation = 'vertical'

        # Primer Bloque
        title_label = Label(text=f'Sistema de Entrenamiento para el Aprendizaje Lúdico de la Trompeta\nBienvenido, {username}', size_hint=(1, 0.2))
        self.add_widget(title_label)

        scales_block = BoxLayout(orientation='horizontal', size_hint=(1, 0.4))

# Etiqueta para el menú desplegable
        scales_label = Label(text='Escalas:')

# Lista de escalas mayores
        escalas_mayores = ["Do Mayor", "Re Mayor", "Mi Mayor", "Fa Mayor", "Sol Mayor", "La Mayor", "Si Mayor"]

# Menú desplegable (Spinner) con las escalas mayores
        scales_spinner = Spinner(text='Seleccione una escala', values=escalas_mayores, size_hint=(0.6, 1))
        scales_block.add_widget(scales_label)
        scales_block.add_widget(scales_spinner)

        self.add_widget(scales_block)
        # Pantalla de escalas
class EscalasScreen(Screen):
    def __init__(self, selected_scale, **kwargs):
        super().__init__(**kwargs)
        self.name = 'escalas'
        self.selected_scale = selected_scale

        # Lógica para mostrar las notas según la escala seleccionada
        escalas_layout = BoxLayout(orientation='vertical')

        # Agrega aquí la lógica para mostrar las notas según la escala seleccionada
        notas_label = Label(text=f'Notas para la escala {selected_scale}:')
        notas_content = Label(text=get_notas_for_escala(selected_scale))

        # Agrega las etiquetas al diseño
        escalas_layout.add_widget(notas_label)
        escalas_layout.add_widget(notas_content)

        # Agrega el diseño al widget de la pantalla
        self.add_widget(escalas_layout)

def get_notas_for_escala(escala):
    # Agrega aquí la lógica para obtener las notas según la escala seleccionada
    # Puedes consultar la base de datos y recuperar las notas y posiciones de dedos.

    # Ejemplo: Notas para las escalas mayores
    # Debes modificar esta consulta para adaptarla a tu estructura de base de datos
    query = f"SELECT n.nota, n.posicion_dedos FROM escalas_notas en JOIN notas n ON en.id_nota = n.id WHERE en.id_escala = (SELECT id FROM escalas WHERE nombre = '{escala}')"

    # Realiza la consulta a la base de datos y obtén las notas y posiciones de dedos
    result = execute_query(query)

    # Formatea el resultado para mostrarlo en la pantalla
    notas_formatted = "\n".join([f"{nota}: {posicion}" for nota, posicion in result])

    return notas_formatted
class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)

        self.login_screen = Screen(name='login')
        self.logged_in_screen = Screen(name='logged_in')

        self.login_screen.add_widget(LoginScreen())
        self.logged_in_screen.add_widget(LoggedInScreen(username=''))

        self.add_widget(self.login_screen)
        self.add_widget(self.logged_in_screen)

    def switch_screen(self, screen_name, username=''):
        screen = self.get_screen(screen_name)
        if screen_name == 'logged_in':
            # Limpia los widgets existentes
            screen.clear_widgets()

            if screen_name == 'escalas':
                # Agrega la lógica para mostrar las escalas según el nombre seleccionado
                escalas_layout = BoxLayout(orientation='vertical')
                # Agrega aquí la lógica para mostrar las escalas según el nombre seleccionado
                escalas_label = Label(text=f'Datos para la escala {username}:')
                escalas_content = Label(text=get_data_for_escala(username))
                # Agrega las etiquetas al diseño
                escalas_layout.add_widget(escalas_label)
                escalas_layout.add_widget(escalas_content)
                # Agrega el diseño al widget de la pantalla
                screen.add_widget(escalas_layout)
            else:
                # Para otras pantallas, simplemente agrega el widget correspondiente
                screen.add_widget(LoggedInScreen(username=username))

        self.current = screen_name

# Luego, debes crear la función get_data_for_escala en algún lugar del código
    def get_data_for_escala(escala):
    # Agrega aquí la lógica para obtener los datos según la escala seleccionada
    # Puedes consultar la base de datos y recuperar los datos específicos de la escala.
    # Ejemplo:
        query = f"SELECT * FROM escalas WHERE nombre = '{escala}'"
        result = execute_query(query)
    # Formatea el resultado para mostrarlo en la pantalla
        data_formatted = "\n".join([f"{column}: {value}" for column, value in result.items()])
        return data_formatted
# Asegúrate de llamar a la función execute_query con tu lógica específica de conexión a la base de datos.

class LoginApp(App):
    def build(self):
        return ScreenManagement()

if __name__ == '__main__':
    LoginApp().run()