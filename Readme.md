# Detector de expresiones faciales

El proyecto consiste en la detección de expresiones faciales a través de la cámara del ordenador. 

## Descripción

Se utiliza los marcadores faciales (Facial Landmarks) de la librería dlib, que permiten identificar puntos en los diferentes rasgos de la cara. 

![Dlib Facial Landmarks](https://github.com/gmfv/Detector-de-emociones/blob/main/Dlib_Facial_landmarks%20(2).jpg)

El programa logra detectar: Ojos cerrados, guiño derecho, guiño izquierdo, cejas levantadas, ceja derecha levantada, ceja izquierda levantada, sonrisa y beso.

## Iniciando
### Prerequisitos
* Tener instalado [DLIB](https://pypi.org/project/dlib/) (Les recomiendo este [blog](https://pyimagesearch.com/2017/03/27/how-to-install-dlib/))

### Ejecutar el programa (Windows)
* Clonar el proyecto
* Descargar el modelo detector de la [esta página](https://www.kaggle.com/datasets/codebreaker619/face-landmark-shape-predictor)(Es muy pesado para subir)
* Tener al main.py y al shape_predictor_68_face_landmarks.dat en la misma carpeta
* Ejecutar el archivo main.py

## Autora
[Giohanna Martínez](https://github.com/gmfv)

## Referencias
* [Facial landmarks with dlib, OpenCV, and Python](https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/?_ga=2.267746444.321007053.1637623315-444521202.1637623315)
* [Real-time facial landmark detection with OpenCV, Python, and dlib](https://www.pyimagesearch.com/2017/04/17/real-time-facial-landmark-detection-opencv-python-dlib/)
