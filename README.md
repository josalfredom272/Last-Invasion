# Last-Invasion

a simple asteroids shooter game made with pygame

# THE GAME WAS CODED BY ME, IF YOU WANT TO ADD LEVELS OR USE THIS CODE AS A REFERENCE FOR YOUR ENGINE,

# GO FOR IT, I DON'T MIND, BUT IF YOU ARE GONNA USE THE SPRITES, MAKE SURE TO CREDIT ALL THE AUTHORS

#####################################################################################################

# ESTE JUEGO FUE PROGRAMADO POR MI, NADIE ME AYUDO T-T, SI QUIEREN USAR ESTE CODIGO PARA SUS PROJECTOS ESTA BIEN,

# SOLO QUE SI VAN A USAR EL ARTE QUE SE ENCUENTRA EN ESTE PROJECTO, ASEGURENSE DE DARLE CREDITO A LOS ARTISTAS Y COMPOSITORES DE AUDIO

# EN CERIO!!!!!, eso incluye a la mayoria de LATAM, se que no todos son asi, pero ya conosco algunos mañosos como son.

# pero mas que nada, espero que este projecto les ayude a entender muchos de los conceptos involucrados en desarrollo de video juegos

# pasenla bien y que tengan buen dia

# select menu and clicking menu sounds provided by:

# https://justsoundeffects.com/

CREDITS TO EVERYONE WHO SHARED THEIR CONTENT FROM OPENGAMEART.ORG

Programer: Lu

SPECIAL THANKS TO https://opengameart.org/

sprites Artists:

game background and main menu background:
Rawdanitsu
https://opengameart.org/content/space-backgrounds-3
player space ship sprite:
Tummyache
https://opengameart.org/content/purple-space-ship

ufos sprites:
The_Scientist\_\_\_
https://opengameart.org/content/basic-ufo-set

mini boss space ship sprite:
Skorpio
http://opengameart.org/users/skorpio

asteroids sprite:
FunwithPixels
https://opengameart.org/content/brown-asteroid

explosion sprites:
JROB774
https://opengameart.org/content/pixel-explosion-12-frames

cursor sprite:
Kednar
https://opengameart.org/content/pointing-hand-mouse-cursors

GUI main menu:
Rawdanitsu
https://opengameart.org/content/simple-hud-gui-constraction-kit-in-8-colors

#### planet sprites:

first planet:
ansimuz
https://opengameart.org/content/space-background-3

planet earth:
St_and
https://opengameart.org/content/earth-1

planet Citronis:
"Citronis" by Molly "Cougarmint" Willits
https://opengameart.org/content/citronis-the-yellow-planet

soundtrack:
main menu soundtrack composer:
yd
https://opengameart.org/content/background-space-track

game soundtrack composer:
Subdream - space-philately
https://opengameart.org/content/space-philately-seamless-loop

mini boss sound track composer:
Alexandr Zhelanov
https://soundcloud.com/alexandr-zhelanov

game over sound track composer:
CodeManu - Magic Space
https://opengameart.org/content/magic-space

sound effects:

lasers sound effects composer:
dklon
https://opengameart.org/content/laser-fire

player damage sound composer:
qubodup
Punch by Iwan 'qubodup' Gabovitch http://opengameart.org/users/qubodup

enemy explosions, player low life alert, asteroids explosions composer:
hosch
https://hosch.itch.io
https://opengameart.org/content/8-bit-sound-effects-2

player dead explosion composer:
Q009
https://opengameart.org/content/q009s-weapon-sounds

---

## 📝 Actualizaciones (21 de Noviembre de 2025)

Se ha realizado una refactorización mayor del código para mejorar su organización y rendimiento:

### 🔧 Refactorización de Código

- **Estructura Modular**: Se dividió `main.py` en varios archivos para separar responsabilidades:
  - `settings.py`: Contiene todas las constantes globales (colores, dimensiones, etc.).
  - `entities.py`: Define las clases del juego (`Entity`, `Enemy`, `Asteroid`, `MidBoss`).
  - `resources.py`: Centraliza la carga y gestión de sonidos y música.
  - `game.py`: Contiene la lógica principal de la clase `Game`.
  - `main.py`: Ahora sirve únicamente como punto de entrada limpio.

### 🐛 Corrección de Errores y Mejoras

- **FPS Estables**: Se reemplazó `time.sleep()` por `pygame.time.Clock().tick(60)` para garantizar 60 FPS fluidos en cualquier máquina.
- **Cierre Correcto**: Se implementó `sys.exit()` para cerrar la aplicación correctamente sin errores.
- **Correcciones Varias**: Se arreglaron errores tipográficos (`colidesWith` -> `collidesWith`) y se eliminaron importaciones innecesarias o redundantes (wildcard imports).

---

## 🚀 Instrucciones de Ejecución

Para jugar a **Last Invasion** en tu computadora, sigue estos pasos:

### Prerrequisitos

Necesitas tener instalado **Python 3.x**.

### 1. Instalar Dependencias

Abre tu terminal o línea de comandos y ejecuta:

```bash
pip install pygame
```

### 2. Ejecutar el Juego

Navega a la carpeta del juego y ejecuta:

```bash
python main.py
```

---

## 📦 Guía para Compilar a .EXE

Si deseas convertir este juego en un archivo ejecutable (`.exe`) para compartirlo con amigos que no tienen Python instalado, puedes usar **PyInstaller**.

### 1. Instalar PyInstaller

```bash
pip install pyinstaller
```

### 2. Crear el Ejecutable

Ejecuta el siguiente comando en la terminal dentro de la carpeta del proyecto:

```bash
pyinstaller --onedir --noconsole --name "LastInvasion" main.py
```

- `--onedir`: Crea una carpeta con el ejecutable y sus dependencias (recomendado para juegos con assets).
- `--noconsole`: Oculta la ventana negra de la consola al jugar.
- `--name "LastInvasion"`: Nombre del archivo final.

### 3. Importante: Mover Assets

Una vez termine el proceso, verás una carpeta llamada `dist/LastInvasion`.
**IMPORTANTE**: Debes copiar manualmente las carpetas `assets`, `sound` y `font` dentro de `dist/LastInvasion` para que el juego encuentre las imágenes y sonidos.

¡Ahora puedes ejecutar `LastInvasion.exe` desde esa carpeta!
