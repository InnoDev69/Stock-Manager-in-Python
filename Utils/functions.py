import customtkinter as ctk
from PIL import Image  # Importa Image desde PIL
from Utils.placeholders import *
from Utils.database import *
import io
import concurrent.futures

def dynamic_thread_executor(functions_with_args):
    """
    Crea hilos dinámicamente para ejecutar una o múltiples funciones con argumentos.
    
    Args:
        functions_with_args (tuple or list): Una función con sus argumentos o una lista de tuplas donde
                                             cada tupla contiene una función y sus argumentos.
                                             Ejemplo para una función: (func1, (arg1, arg2))
                                             Ejemplo para múltiples funciones: [(func1, (arg1, arg2)), (func2, (arg1,))]
    
    Returns:
        list: Resultados de las funciones que retornan valores. Si una función no retorna nada, su valor será None.
    """
    results = []
    
    # Se asegura de que el argumento es una lista, aunque sea una única función
    if isinstance(functions_with_args, tuple):
        functions_with_args = [functions_with_args]
    
    # Usa ThreadPoolExecutor para manejar los hilos
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Creación de futuros (futuros son los resultados que los hilos devolverán eventualmente)
        futures = [executor.submit(func, *args) for func, args in functions_with_args]
        
        # Recolecta los resultados de cada hilo
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()  # Obtiene el valor retornado
                results.append(result)
            except Exception as e:
                print(f"Error en el hilo: {e}")
                results.append(None)  # Si hay un error, lo maneja y continua
    
    return results
color_p = "#fafafa"
color_s = "#efefef"
grey = "#EDEBE9"
blue = "#0080ff"
black = "#131313"

def create_scrollable_frame(manager, color_p, branch_user, fg_color="black", font=('Plus Jakarta Sans', 20, 'bold')):
    # Crea el CTkScrollableFrame
    main_fr = ctk.CTkScrollableFrame(manager, fg_color=color_p, height=530, width=780)
    main_fr.place(relx=0.5, y=341, anchor="center")

    # Crea el frame de la sucursal dentro del scrollable frame
    sucursal_fr = ctk.CTkFrame(main_fr, fg_color=color_p, height=70, width=780)
    sucursal_fr.grid(row=0, column=0, columnspan=4)

    if manager.get_variable('user_role') in ['Normal User', 'Admin']:
        sucursal_lb = ctk.CTkLabel(sucursal_fr, text_color=fg_color, text=f'Sucursal {branch_user}', font=font)
        sucursal_lb.place(x=(sucursal_lb.winfo_width()) // 2 + 115, rely=0.5, anchor="center")

    elif manager.get_variable('user_role') == 'General Admin' and manager.current_scene_name=='Men_p_admin':
        sucursal_lb = ctk.CTkLabel(sucursal_fr, text_color=fg_color, text="Sucursales", font=font)
        sucursal_lb.place(x=(sucursal_lb.winfo_width()) // 2 + 75, rely=0.5, anchor="center")
        crear_sucursal = ctk.CTkButton(sucursal_fr, text_color=fg_color, text="+ Sucursal", font=('Plus Jakarta Sans', 16, 'bold'), fg_color= grey,
                                        hover_color= color_s, width=150, height= 40, corner_radius= 20)
        crear_sucursal.place(relx = 0.88, rely = 0.5, anchor = "center")
        
    else:
        sucursal_lb = None
    return main_fr, sucursal_fr, sucursal_lb

def header(manager) -> any:
    menu_user = None  # Variable para el menu desplegable
    
    def toggle_menu():
        nonlocal menu_user
        if menu_user is None or not menu_user.is_active:
            # Abre el menu si no está activo
            menu_user = Menu_user(manager, side="right", width=300, height=530)
            menu_user.slide_in()

            fr = ctk.CTkFrame(menu_user, width= 260, height= 85, corner_radius= 10,fg_color= grey)
            fr.place(relx=0.49, rely=0.12, anchor="center")
            user_img1 = ctk.CTkImage(Image.open("img/person.png"), size=(40, 40))
            img = ctk.CTkLabel(fr, width=65, height=65,corner_radius= 10, image= user_img1, text = "")
            img.place(relx=0.16, rely=0.5, anchor="center")
            user_name = ctk.CTkLabel(fr, text_color=black,text = get_user_name(manager.get_variable("user_id")), font = ('Plus jakarta Sans', 14, 'bold')).place(relx=0.6, rely=0.5, anchor="center")

            log_out =  ctk.CTkButton(menu_user, width= 260, height= 35, corner_radius= 10,fg_color= grey, hover_color = color_s,
                                    text= "Cerrar sesion",text_color=black, font = ('Plus jakarta Sans', 14, 'bold'), command= log_out_def)
            log_out.place(relx=0.49, rely=0.9, anchor="center")

            menu_user.is_active = True
        else:
            # Cierra el menu si está activo
            menu_user.slide_out()
            menu_user.is_active = False
    def log_out_def(event = None):
        manager.switch_scene("Login")

    btn_config = {'font': ('Plus jakarta Sans', 14, 'bold'), 'text_color': "#000000", 'fg_color': "transparent", 'hover_color': "#dcdcdc", 'height': 35, }
    user_img = ctk.CTkImage(Image.open("img/person.png"), size=(20, 20))

    header_fr = ctk.CTkFrame(manager, fg_color=color_p, border_color=color_s, border_width=1, height=70, width=800)
    header_fr.place(relx=0.5, y=35, anchor="center")

    name = ctk.CTkLabel(header_fr, text="|Urbanvibe", text_color=black, font=('Plus Jakarta Sans', 28, 'bold'))
    name.place(x=100, rely=0.5, anchor="center")

    user = ctk.CTkButton(header_fr, text="", image=user_img, fg_color="transparent", hover_color="#dcdcdc", height=35, width=35, command=toggle_menu, cursor="hand2")
    user.place(x=800 - 50, rely=0.5, anchor="center")

    # NAV Frame
    nav = ctk.CTkFrame(header_fr, fg_color=color_p, height=65, width=406)
    nav.place(relx=0.5, y=35, anchor="center")

    # Los botones
    if manager.get_variable('user_role') == 'Normal User':
        btn_nav =  [("Stock", (406 // 2) - 80, None, lambda: manager.switch_scene("Stock_nav"), 70),
                    ("Home", 406 // 2, None, lambda: manager.switch_scene("Men_p"), 70),
                    ("Ventas", (406 // 2) + 80, None, lambda: manager.switch_scene("Ventas_nav"), 70)]
        for text, x_cord, img, command, width in btn_nav:
            button = ctk.CTkButton(nav, text=text, image=img, **btn_config, width=width, command=command)
            button.place(x=x_cord, rely=0.5, anchor="center")

    elif manager.get_variable('user_role') == 'Admin':
        btn_nav =  [("Stock", (406 // 2) - 80, None, lambda: manager.switch_scene("Stock_nav"), 70),
                    ("Home", 406 // 2, None, lambda: manager.switch_scene("Men_p"), 70),
                    ("Ventas", (406 // 2) + 80, None, lambda: manager.switch_scene("Ventas_nav"), 70)]
        for text, x_cord, img, command, width in btn_nav:
            button = ctk.CTkButton(nav, text=text, image=img, **btn_config, width=width, command=command)
            button.place(x=x_cord, rely=0.5, anchor="center")

    elif manager.get_variable('user_role') == 'General Admin':
        btn_nav =  [("Notifications", (406 // 2) - 90, None, lambda: manager.switch_scene("Users"), 70),#cambiar por la respectiva pantalla
                    ("Home", (406 // 2) + 10, None, lambda: manager.switch_scene("Men_p_admin"), 70),
                    ("Users", (406 // 2) + 90, None, lambda: manager.switch_scene("Users"), 70)]
        for text, x_cord, img, command, width in btn_nav:
            button = ctk.CTkButton(nav, text=text, image=img, **btn_config, width=width, command=command)
            button.place(x=x_cord, rely=0.5, anchor="center")


    return header_fr


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calcula la distancia de Levenshtein entre dos cadenas."""
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    # Crea una lista que representa la distancia desde la cadena vacía hasta cada prefijo de s1
    distances = range(len(s1) + 1)

    # Itera sobre cada carácter de s2
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            cost = 0 if c1 == c2 else 1
            distances_.append(min(
                distances[i1] + cost,    # Costo de sustitución o coincidencia
                distances[i1 + 1] + 1,   # Costo de eliminación
                distances_[-1] + 1       # Costo de inserción
            ))
        distances = distances_

    return distances[-1]

def normalize_string(s: str) -> str:
    """Normaliza una cadena para eliminar espacios en blanco adicionales y convertir a minúsculas."""
    return ''.join(c for c in s.lower().strip() if c.isalnum())

def fuzzy_match(s1: str, s2: str) -> float:
    """Calcula una puntuación de coincidencia difusa entre dos cadenas basándose en Levenshtein."""
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0  # Cadenas vacías coinciden completamente
    distance = levenshtein_distance(s1, s2)
    return 1 - (distance / max_len)  # Puntuación entre 0 y 1

def search_function(product_list: list, search: str, max_distance: int = 8, threshold: float = 0.4) -> list:
    """Mejora la precisión de la búsqueda utilizando coincidencias difusas y normalización."""
    search_normalized = normalize_string(search)
    result = []

    for product in product_list:
        product_name_normalized = normalize_string(product.name)
        
        # Coincidencia difusa con ponderación
        match_score = fuzzy_match(search_normalized, product_name_normalized)
        
        # Si la puntuación de coincidencia es mayor que el umbral, considera el producto como coincidencia
        if match_score >= threshold:
            result.append((product, match_score))
    
    # Ordena los resultados por la puntuación de coincidencia
    result.sort(key=lambda x: x[1], reverse=True)

    return [product for product, score in result]

def show_notification(manager, text:str)->None:
    Slideout(manager, side="right", width=250, height=75, bg_color= grey, text=text, text_color='#000000').slide_in()

def menu_sesions(manager, si):
    if not si:
        menu_fr = Menu_user(manager, side= "right", width= 300, height= 530, bg_color= grey)
        menu_fr.slide_in()

def binary_to_image(byte_data: bytearray) -> Image:
    """Convierte un array de bytes en una imagen usando Pillow."""
    byte_io = io.BytesIO(byte_data)  # Convierte el bytearray a un objeto BytesIO
    return Image.open(byte_io)