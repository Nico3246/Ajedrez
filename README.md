# Ajedrez 

Repositorio de un juego de ajedrez implementado en Python con interfaz básica y lógica de partida.

## Características

* Representación de tablero y piezas clásicas (torre, alfil, caballo, dama, rey, peón).
* Movimientos válidos según reglas estándar del ajedrez.
* Detección de jaque, jaque mate y tablas (ahogado, repetición, regla de los 50 movimientos).
* Modo de juego contra otro jugador por turnos.
* Interfaz de texto (CLI); posible integración con GUI o AI en versiones futuras.

## Requisitos

* Python 3.8 o superior
* Módulos necesarios (puede listarse en un `requirements.txt`)

  * Ejemplo: `pip install colorama`

## Instalación y ejecución

```bash
git clone https://github.com/Nico3246/Ajedrez.git
cd Ajedrez
# si existe requirements.txt
pip install -r requirements.txt
python main.py
```

## Uso

* Inicia una partida con `python main.py`.
* Los jugadores ingresan movimientos en notación algebraica, por ejemplo: `e2e4`, `g8f6`.
* La aplicación valida y ejecuta los movimientos, actualiza el tablero y notifica condiciones especiales: jaque, jaque mate, tablas.
* Al terminar la partida, muestra resultado: *victoria blancas*, *victoria negras* o *empate*.

## Estructura del proyecto

* `main.py` – Punto de entrada principal, bucle de juego y control de flujo.
* `board.py` – Representación del tablero, generación de movimientos y control de estado.
* `piece.py` – Clases de piezas y sus movimientos específicos.
* `utils.py` – Funciones auxiliares (como notación algebraica, dibujo del tablero).
* `tests/` – Conjunto de pruebas unitarias para validar reglas y lógica.

## Ejemplos

```txt
Turno 1: Blancas
Ingresa movimiento (ej. e2e4): e2e4

Turno 2: Negras
Ingresa movimiento (ej. e7e5): e7e5

... continúa hasta jaque mate o empate...
```

## Pruebas

Se incluye un suite de pruebas usando `pytest` para verificar movimientos válidos, detección de jaque/jaque mate/tablas:

```bash
pip install pytest
pytest
```

## Contribuciones

¡Las contribuciones son bienvenidas! Puedes:

* Reportar errores o sugerir mejoras en **Issues**.
* Proponer nuevas funcionalidades o variaciones de juego (como control de tiempo, AI, modo multijugador online) mediante **Pull Requests**.

## Recursos y referencias

* [Reglas oficiales del ajedrez](https://es.wikipedia.org/wiki/Ajedrez)
* Posibles integraciones futuras con bibliotecas como `python-chess`, motores UCI como Stockfish, o interfaces gráficas (Tkinter, Pygame, Web).

## Licencia

El proyecto está bajo licencia **[MIT License](LICENSE)**.

---


