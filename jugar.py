import numpy as np
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from docx import Document
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivymd.uix.dialog import MDDialog
from bimatrix_games import MensajeDeError
from main import VentanaLayout, MasInfoVentana, WrappedLabel

Builder.load_file('jugar.kv')


class SelectPlayer(MDDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.referencia = App.get_running_app().root.ids.jugarid

    def selection1(self):
        self.referencia.player2 = NPCNash('images/johnnash.jpg',
                                          ['''"[...]Pero, después de una vida de búsqueda me digo, ¿Qué es la lógica?\
 ¿Quién decide la razón?"''',
                                           '''"Caballeros, debo recordarles que, mis probabilidades de éxito, aumentan\
 en cada nuevo intento"''',
                                           '"No, no creo en la suerte, pero sí en asignar valor a las cosas"'])
        self.dismiss()
        self.referencia.inicio_juego()

    def selection2(self):
        self.referencia.player2 = NPCMurray('images/rothbard.jpg',
                                            ['''"El Estado obtiene su renta mediante el uso de la compulsión, es decir,\
 la amenaza de la cárcel y la bayoneta"''',
                                             '''"Si los humanos son tan malos, ¿cómo podemos esperar que un gobierno\
 coercitivo, compuesto por humanos, mejore la situación?"''',
                                             '''"La contribución es, pura y simplemente, un robo, un robo a grande\
 y colosal escala"'''])
        self.dismiss()
        self.referencia.inicio_juego()

    def selection3(self):
        self.referencia.player2 = NPCMarx('images/karlmarx.jpg',
                                          ['"¡Proletarios de todos los países, uníos!"',
                                           '''"La historia de todas las sociedades hasta el día de hoy es historia\
 de luchas de clases"''',
                                           '"¡De cada cual según sus capacidades, a cada cual según sus necesidades!"'])
        self.dismiss()
        self.referencia.inicio_juego()


class ConfirmationScreen(MDDialog):
    pass


# Para mostrar los resultados en pantalla
class Popup_resultado(Popup):
    pass


class ResetGame(MDDialog):

    @staticmethod
    def exportar_resultados(resultados):
        # Método para exportar los resultados a Word
        # Create a new Word document
        document = Document()

        # Añadimos nuestros datos al documento
        for key, value in resultados.items():
            document.add_paragraph('ETAPA: ' + f'{key}')
            document.add_paragraph('MODELO: ' + f'{value[0]}')
            document.add_paragraph('Función de demanda del mercado: ' + f'p(X) = {value[1]} - {value[2]}X')
            document.add_paragraph('Costes totales de la empresa 1: ' + f'{value[3]}x\u2081')
            document.add_paragraph('Costes totales de la empresa 2: ' + f'{value[3]}x\u2082')
            document.add_paragraph()
            document.add_paragraph('RESPUESTAS: ')
            document.add_paragraph('Tu empresa: ')
            document.add_paragraph('Producción: ' + f'{value[6]} uds')
            document.add_paragraph('Beneficio: ' + f'{value[7]} €')
            document.add_paragraph()
            document.add_paragraph('Empresa del NPC: ')
            document.add_paragraph('Producción: ' + f'{value[8]} uds')
            document.add_paragraph('Beneficio: ' + f'{value[9]} €')
            document.add_paragraph()
            document.add_paragraph('Datos del mercado: ')
            document.add_paragraph('Precio: ' + f'{value[4]}')
            document.add_paragraph('Cantidad: ' + f'{value[5]}')
            # Siguiente página
            [document.add_paragraph() for i in range(8)]

        document.add_paragraph('RESULTADOS GLOBALES:')
        document.add_paragraph('Tu beneficio total: ' + f'{resultados[1][7] + resultados[2][7] + resultados[3][7]} €')
        document.add_paragraph('Beneficio total NPC: ' + f'{resultados[1][9] + resultados[2][9] + resultados[3][9]} €')

        # Save the Word document
        document.save('vsNPC_output.docx')

        alerta = MensajeDeError("Se ha creado el documento 'vsNPC_output.docx' exitosamente")
        alerta.open()

        # Creamos el output a mostrar en pantalla
        scroll = ScrollView()
        popup = Popup_resultado(content=scroll)
        grid = GridLayout(cols=3, size_hint=(1, None), padding='5dp')
        scroll.add_widget(grid)
        grid.bind(minimum_height=grid.setter('height'))

        for key, value in resultados.items():
            text_list = [
                '[b]ETAPA: ' + f'{key}[/b]',
                '\n[u]MODELO:[/u] ' + f'{value[0]}',
                '\n[u]Datos[/u]',
                f'p(X) = {value[1]} - {value[2]}X',
                'CT[sub]1[/sub]: ' + f'{value[3]}x[sub]1[/sub]',
                'CT[sub]2[/sub]: ' + f'{value[3]}x[sub]2[/sub]',
                '\n[u]RESPUESTAS:[/u] ',
                '\n[u]Tu empresa:[/u] ',
                'Producción: ' + f'{value[6]} uds',
                'Beneficio: ' + f'{value[7]} €',
                '\n[u]Empresa del NPC:[/u] ',
                'Producción: ' + f'{value[8]} uds',
                'Beneficio: ' + f'{value[9]} €',
                '\n[u]Datos del mercado:[/u] ',
                'Precio: ' + f'{value[4]} €',
                'Cantidad: ' + f'{value[5]} uds',
            ]

            grid2 = GridLayout(cols=1, size_hint=(1, None), padding='5dp')
            grid2.bind(minimum_height=grid2.setter('height'))
            for text in text_list:
                grid2.add_widget(
                    WrappedLabel(text=text, color=(0, 0, 0, 1), size_hint=(1, None), markup=True))
            grid.add_widget(grid2)

        '''text_list2 = [
        'RESULTADOS GLOBALES:',
        'Tu beneficio total: ' + f'{historial[1][7] + historial[2][7] + historial[3][7]} €',
        'Beneficio total NPC: ' + f'{historial[1][9] + historial[2][9] + historial[3][9]} €'
        ]
        for text in text_list2:
            grid.add_widget(
                WrappedLabel(text=text, color=(0, 0, 0, 1), font_size=grid.height * 0.022, size_hint=(1, None)))'''

        popup.open()


class JugarVentana(VentanaLayout):
    player2 = None
    prod1 = 0
    prod2 = 0
    precio = 0
    beneficio1 = 0
    beneficio2 = 0
    cantidad_total = 0
    evento = 0
    historial = {}
    model = 0
    precio2 = 0
    modelos = {1: 'COURNOT', 2: 'STACKELBERG (NPC=líder)', 3: 'STACKELBERG (NPC=seguidora)', 4: 'BERTRAND'}

    # Asignamos valores aleatorios al inicio del juego
    a = 0
    b = 0
    c = 0

    # Valores a mostrar en pantalla
    comentario = StringProperty('')
    modelo = StringProperty('')
    narrativa = StringProperty('')
    demanda_mercado = StringProperty(f'{a} - {b}x')
    costes_totales = StringProperty(f'{c}x')
    imagen = StringProperty('')
    rival = None
    stage = NumericProperty(0)
    stage1 = StringProperty('')
    stage2 = StringProperty('')
    stage3 = StringProperty('')

    def on_enter(self, *args):
        if self.stage == 0:
            selector = SelectPlayer()
            selector.open()
        else:
            pass

    @staticmethod
    def reiniciar():
        dialog = ConfirmationScreen()
        dialog.open()

    def inicio_juego(self):
        # Asignamos valores aleatorios al inicio del juego
        self.a = np.random.randint(250, 500)
        self.b = np.random.randint(2, 25)
        self.c = np.random.randint(21, 40)

        self.imagen = str(self.player2.img)
        self.comentario = self.player2.frases[np.random.randint(0, 3)]
        self.update_screen()
        self.selecciona_modelo()
        self.stage += 1

    def update_screen(self):
        self.demanda_mercado = f'{self.a} - {self.b}x'
        self.costes_totales = f'{self.c}x'

    def selecciona_modelo(self):
        self.model = np.random.randint(1, 5)

        # Cournot
        if self.model == 1:
            self.modelo = 'MODELO DE COURNOT'
            self.prod2 = np.around(self.player2.cournot(self.a, self.b, self.c), 3)

        # NPC Stackelberg líder
        elif self.model == 2:
            self.prod2 = round(self.player2.stackelberg1(self.a, self.b, self.c), 3)
            self.modelo = f'MODELO DE STACKELBERG. TÚ ERES LA EMPRESA SEGUIDORA. {self.player2.name} produjo {self.prod2} unidades.'

        # NPC Stackelberg seguidor
        elif self.model == 3:
            self.modelo = 'MODELO DE STACKELBERG. TÚ ERES LA EMPRESA LÍDER'

        # Bertrand
        else:
            self.modelo = 'MODELO DE BERTRAND'
            self.precio2 = self.player2.bertrand(self.c)

    def reset_parametros(self):
        self.historial = {}
        self.stage = 0
        self.ids.respuesta.text = ''
        self.stage1 = ''
        self.stage2 = ''
        self.stage3 = ''
        self.imagen = ''
        self.comentario = ''
        self.modelo = ''
        self.narrativa = ''
        self.demanda_mercado = ''
        self.costes_totales = ''
        NPCMurray.tax = 0

    def evento_aleatorio(self):
        # Selección aleatoria del evento y la cuantía
        self.evento = np.random.randint(1, 5)
        cuantia = np.random.randint(3, 10)

        # Si el evento afecta a la demanda, modificamos la demanda (y viceversa)
        if self.evento == 1:
            self.narrativa = '''Recientemente se publicaron los resultados de un estudio llevado a cabo por la\
 universidad de Massachusetts que resaltan los beneficios del uso de tu producto. Esto ha producido un aumento\
 de la demanda de mercado. Los cambios se han registrado en la función de demanda.'''
            self.a = self.a + cuantia

        elif self.evento == 2:
            self.narrativa = '''Como consecuencia de una pandemia mundial, el número de personas que\
 pueden acceder y utilizar tu producto se ha reducido considerablemente. Los cambios se han introducido\
 en la función de demanda del mercado.'''
            self.a = self.a - cuantia

        elif self.evento == 3:
            self.c = self.c + cuantia
            NPCMurray.tax = NPCMurray.tax - cuantia
            self.narrativa = f'''El Gobierno introdujo un impuesto de {cuantia} u.m. sobre la producción.\
 El aumento aumento de costes asociado se ha introducido en tu función de costes.'''

        elif self.evento == 4:
            self.c = self.c - cuantia
            NPCMurray.tax = NPCMurray.tax + cuantia
            self.narrativa = f'''El Gobierno introdujo una subvención de {cuantia} u.m. por cada unidad producida.\
 Los cambios se han introducido en tu función de costes.'''

        self.update_screen()

    def confirma(self):

        # Comprobamos si el usuario introdujo un valor admitido
        try:
            respuesta = np.around(float(self.ids.respuesta.text), 3)
            if respuesta == 0:
                raise ValueError
        except ValueError:
            alerta = MensajeDeError('Introduzca parámetros válidos')
            alerta.open()
            return

        # Si es modelo de Bertrand, la variable de decisión cambia
        if self.model == 4:
            self.precio2 = self.precio2

            if self.precio2 > respuesta:
                self.precio = respuesta
                self.prod1 = np.around((self.a - self.precio) / self.b, 3)
                self.prod2 = 0

            elif self.precio2 < respuesta:
                self.precio = self.precio2
                self.prod1 = 0
                self.prod2 = np.around((self.a - self.precio) / self.b, 3)

            # Por defecto, a igual precio suponemos los clientes se distribuyen equitativamente
            else:
                self.precio = respuesta
                self.prod1 = np.around((self.a - self.precio) / (2 * self.b), 3)
                self.prod2 = np.around((self.a - self.precio) / (2 * self.b), 3)

        # Si el NPC es seguidor, debe conocer nuestra producción
        elif self.model == 3:
            self.prod1 = respuesta
            self.prod2 = np.around(self.player2.stackelberg2(self.a, self.b, self.c, respuesta), 3)
            self.precio = np.around(self.a - (self.b * (self.prod1 + self.prod2)), 3)

        else:
            self.prod1 = respuesta
            self.precio = np.around(self.a - (self.b * (self.prod1 + self.prod2)), 3)

        # Si el precio resultante en el mercado es negativo, se establece un precio igual a 0.001
        if self.precio <= 0:
            self.precio = .001

        self.cantidad_total = np.around(self.prod1 + self.prod2, 3)
        self.beneficio1 = np.around((self.precio - self.c) * self.prod1, 3)
        self.beneficio2 = np.around((self.precio - self.c) * self.prod2, 3)

        # Rellenamos el historial
        self.historial[self.stage] = [self.modelos.get(self.model, self.model), self.a, self.b, self.c, self.precio, self.cantidad_total,
                                      self.prod1, self.beneficio1, self.prod2, self.beneficio2]

        stage_dict = {1: 'stage1', 2: 'stage2', 3: 'stage3'}
        stage_key = stage_dict.get(self.stage)
        setattr(self, stage_key, f'Beneficio_{self.stage}:  {self.beneficio1}')

        # Pasamos de etapa
        self.ids.respuesta.text = ''
        self.stage += 1

        # Comprobamos si el juego se ha acabado
        if self.stage > 3:
            reseteo = ResetGame()
            reseteo.open()
            return

        else:
            self.evento_aleatorio()
            self.selecciona_modelo()

    def obtenermasinfo(self):
        self.manager.current = 'JugarMasInfoScreen'


class NPCNash:
    def __init__(self, img, frases):
        self.img = img
        self.frases = frases
        self.name = 'John Forbes Nash'

    # Cournot
    @staticmethod
    def cournot(a, b, c):
        return (a - c) / (3 * b)

    # Líder
    @staticmethod
    def stackelberg1(a, b, c):
        return (a - c) / (2 * b)

    # Seguidora
    @staticmethod
    def stackelberg2(a, b, c, x1):
        result = ((a - c) / (2 * b)) - (x1 / 2)
        if result > 0:
            return result
        else:
            return 0

    # Bertrand
    @staticmethod
    def bertrand(c):
        return c


class NPCMurray:
    # Variable que (des)informará al NPCMurray sobre los impuestos del Gobierno
    tax = 0

    def __init__(self, img, frases):
        self.img = img
        self.frases = frases
        self.name = 'Murray Rothbard'

    # Cournot
    @staticmethod
    def cournot(a, b, c):
        return (a - (c + NPCMurray.tax)) / (3 * b)

    # Líder
    @staticmethod
    def stackelberg1(a, b, c):
        return (a - (c + NPCMurray.tax)) / (2 * b)

    # Seguidora
    @staticmethod
    def stackelberg2(a, b, c, x1):
        result = ((a - (c + NPCMurray.tax)) / (2 * b)) - (x1 / 2)
        if result > 0:
            return result
        else:
            return 0

    # Bertrand
    @staticmethod
    def bertrand(c):
        return c + NPCMurray.tax


class NPCMarx:
    def __init__(self, img, frases):
        self.img = img
        self.frases = frases
        self.name = 'Karl Marx'

    # Cournot
    @staticmethod
    def cournot(a, b, c):
        return (a - (1.2 * c)) / (3 * b)

    # Líder
    @staticmethod
    def stackelberg1(a, b, c):
        return (a - (1.2 * c)) / (2 * b)

    # Seguidora
    @staticmethod
    def stackelberg2(a, b, c, x1):
        result = ((a - (1.2*c)) / (2 * b)) - (x1 / 2)
        if result > 0:
            return result
        else:
            return 0

    # Bertrand
    @staticmethod
    def bertrand(c):
        return 1.2 * c


class JugarMasInfoScreen(MasInfoVentana):
    a = '''El juego consiste en 3 etapas en las que tú, dueño de una empresa, competirás con uno de los tres NPCs\
 disponibles, dueño de la empresa rival. Cada uno de estos jugadores tiene un comportamiento predefinido distinto,\
 cambiando la facilidad con la que podrás obtener beneficios en cada periodo:
    - John Nash: siempre tomará las decisiones más adecuadas, teniendo en cuenta la teoría existente al respecto.

    - Murray Rothbard: responderá generalmente de forma acertada pero tiene una debilidad: la intervención estatal.\
 Ignorará los impuestos establecidos y las subvenciones concedidas por el Gobierno. Lo ignorará de cara a su decisión\
 de producción, sin embargo, sus costes reales serán igual a los tuyos por lo que puedes aprovecharte de esta\
 circunstancia. Ten en cuenta que su desaprobación de la intervención estatal es permanente, por lo que “acumulará”\
 la ignorancia sobre las intervenciones pasadas, así que es recomendable ir apuntándolo para optimizar tus\
 decisiones, por ejemplo:

CT = 10x
Etapa 1:
“El Gobierno introduce un impuesto sobre la producción de 2 u.m.”
Rothbard producirá como si siguiera teniendo CT = 10x, cuando en realidad sus costes son mayores (12x).
Etapa 2:
“El Gobierno concede una subvención sobre la producción de 4 u.m.”
Rothbard producirá como si siguiera teniendo CT = 10x (ignora tanto el impuesto del anterior periodo como la\
 subvención de este), cuando en realidad sus costes reales son de 8x.

    -Karl Marx: sobreestima sus costes con la intención de no extraer plusvalía de sus trabajadores. En concreto,\
 producirá como si tuviera unos costes un 20% mayores a los reales. En este caso, el NPC tiene en cuenta todos los\
 eventos que sucedan. Además, ese 20% no es acumulativo, es decir, en cada periodo actuará como si sus costes fueran\
 un 20% superiores a los tuyos para ese mismo periodo:

CT = 10x
Karl Marx producirá como si tuviera CT = 12x . 

Cabe recordar que el enfrentamiento con el ordenador no es siempre rigurosamente equitativo puesto que, a pesar de\
 tener los mismos costes totales en todo momento, en el modelo de Stackelberg el orden de entrada en el mercado\
 desequilibra la balanza (favorece a la empresa líder considerablemente).

A lo largo del juego deberás decidir la cantidad a producir (modelos de Cournot y Stackelberg) o el precio que vas\
 a establecer (modelo de Bertrand) teniendo en cuenta la personalidad del NPC, el modelo a tratar en la etapa y, por\
 supuesto, las funciones de demanda del mercado y costes totales.

Al final de la partida podrás exportar los resultados obtenidos por etapa a un documento Word.
'''
