# importamos las librerías necesarias
from imutils import face_utils
from scipy.spatial import distance as dist
import dlib
import cv2
 
# inicializamos el detector de rostros de la libreria dlib y creamos el predictor
# the facial landmark predictor
p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)
cuenta_frames = 0
cuenta_frames1 = 0
cuenta_frames2 = 0
cap = cv2.VideoCapture(0)
font=cv2.FONT_HERSHEY_SIMPLEX
estado_ojos = "NEUTRO"
estado_boca = "NEUTRO"
estado_cejas = "NEUTRO"
ojoscerrados = 0
def eye_aspect_ratio(eye):
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	C = dist.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear

def mouth_ratio(mouth):
        C = dist.euclidean(mouth[0], mouth[6])
        S = dist.euclidean(mouth[14], mouth[18])
        return C, S

def eyebrows_aspect_ratio(eyebrow, eye):
        A = dist.euclidean(eyebrow[2], eye[1])
        B = dist.euclidean(eyebrow[2], eye[2])
        radio = (A + B) / (2.0)
        return radio

while True:
    # cargamos la imagen y la pasamos a escala de grises
    _, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    # detectamos los puntos de inicio y fin de los rasgos faciales
    rects = detector(gray, 0)
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    (MStart, MEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
    (CejaDer_Start, CejaDer_End) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]
    (CejaIzq_Start, CejaIzq_End) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]

    # bucle para detección de rostros
    for (i, rect) in enumerate(rects):
        # determinamos los marcadores y convermos a un numpy array 
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        CejaDerecha = shape[CejaDer_Start:CejaDer_End]
        CejaIzquierda = shape[CejaIzq_Start:CejaIzq_End]
        Boca = shape[MStart:MEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        distanciaComisura, distanciaSonrisa = mouth_ratio(Boca)
        distanciaCEJA_I = eyebrows_aspect_ratio(CejaDerecha, rightEye)
        distanciaCEJA_D = eyebrows_aspect_ratio(CejaIzquierda, leftEye)
        if (leftEAR < 0.23 and rightEAR < 0.21):
            if cuenta_frames>8:
                estado_ojos = "OJOS CERRADOS"
                cuenta_frames = 0
                ojoscerrados=1
            else:
                cuenta_frames = cuenta_frames +1
        elif (leftEAR < 0.23 and rightEAR > 0.25):
            estado_ojos = "GUINHO IZQUIERDO"
            ojoscerrados=0
            cuenta_frames = 0
        elif (rightEAR < 0.24 and leftEAR > 0.25):
            ojoscerrados=0
            estado_ojos = "GUINHO DERECHO"
            cuenta_frames = 0
        elif(rightEAR > 0.33):
            estado_ojos = "NEUTRO"

        if (distanciaCEJA_D >42 and distanciaCEJA_I > 42 and ojoscerrados==0):
            estado_cejas = "CEJAS LEVANTADAS"
            cuenta_frames1 = 0
        elif (distanciaCEJA_D > 42 and distanciaCEJA_I < 38):
           estado_cejas = "CEJA DERECHA LEVANTADA"
           cuenta_frames1 = 0
        elif (distanciaCEJA_I > 42 and distanciaCEJA_D < 38):
            estado_cejas = "CEJA IZQUIERDA LEVANTADA"
            cuenta_frames1 = 0
        else:
            if (cuenta_frames1 >8):
                 estado_cejas = "NEUTRO"
                 cuenta_frames1 = 0
            else:
                 cuenta_frames1 = cuenta_frames1 + 1

        if (distanciaComisura<69):
            estado_boca = "BESO"
            cuenta_frames2 = 0
        elif (distanciaSonrisa>15 and distanciaComisura>77):
            estado_boca = "SONRISA"
            cuenta_frames2 = 0
        else:
            if(cuenta_frames2 > 5):
                 estado_boca = "NEUTRO"
                 cuenta_frames2 = 0
            else:
                 cuenta_frames2 = cuenta_frames2 +1

        cv2.putText(image, 'CEJAS: '+estado_cejas, (30, 50), font, 0.7, (0, 0, 255),2)
        cv2.putText(image, 'OJOS: '+estado_ojos, (30, 100), font, 0.7, (0, 0, 255),2)
        cv2.putText(image, 'BOCA: '+estado_boca, (30, 150), font, 0.7, (0, 0, 255),2)

    # se muestra la imagen con las etiquetas
    cv2.imshow("Output", image)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()