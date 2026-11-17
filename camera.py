import cv2
import face_recognition
import os

# Carica le immagini e i loro encoding
def carica_persona(nome, cartella):
    encodings = []
    for file in os.listdir(cartella):
        if file.startswith(nome) and (file.endswith('.jpg') or file.endswith('.jpeg')):
            percorso = os.path.join(cartella, file)
            immagine = face_recognition.load_image_file(percorso)
            risultati = face_recognition.face_encodings(immagine)
            if risultati:
                encodings.append(risultati[0])
    return encodings

# Imposta la cartella contenente le immagini
cartella = 'volti-fr'
encodings_noti = []
nomi_noti = []

if os.path.isdir(cartella):
    for nome in ['Francesco', 'John', 'Giulia']:
        enc = carica_persona(nome, cartella)
        encodings_noti.extend(enc)
        nomi_noti.extend([nome] * len(enc))

print(f"Caricati {len(encodings_noti)} encoding totali")

# Avviso se la cartella manca, è vuota o non contiene volti validi
messaggio_avviso = None

if not os.path.isdir(cartella):
    messaggio_avviso = f"Cartella '{cartella}' non trovata"
elif not os.listdir(cartella):
    messaggio_avviso = f"Cartella '{cartella}' vuota"
elif not encodings_noti:
    messaggio_avviso = "Nessun volto valido caricato"

if messaggio_avviso:
    print("ATTENZIONE:", messaggio_avviso)

cap = cv2.VideoCapture(0)

# Inizializza il video
while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        continue
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    posizioni = face_recognition.face_locations(rgb_frame)
    encodings = face_recognition.face_encodings(rgb_frame, posizioni)

    for encoding, (top, right, bottom, left) in zip(encodings, posizioni):
        risultati = face_recognition.compare_faces(encodings_noti, encoding, tolerance=0.5)
        nome = 'Sconosciuto'

        if True in risultati:
            nome = nomi_noti[risultati.index(True)]

        # Colore diverso per sconosciuti
        colore = (0, 255, 0) if nome != 'Sconosciuto' else (0, 0, 255)

        # Contorno Volto
        cv2.rectangle(frame, (left, top), (right, bottom), colore, 2)

        # Nome del soggetto
        cv2.putText(frame, nome, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, colore, 2)

        # Calcola centro del volto
        cx = (left + right) // 2
        cy = (top + bottom) // 2

        # Puntatore — cerchio + croce centrata sul volto
        cv2.circle(frame, (cx, cy), 30, colore, 2)
        cv2.line(frame, (cx - 40, cy), (cx + 40, cy), colore, 1)
        cv2.line(frame, (cx, cy - 40), (cx, cy + 40), colore, 1)

    # Avviso a schermo
    if messaggio_avviso:
        # Banda scura in alto per leggibilità
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (0, 0, 0), -1)
        cv2.putText(frame, "ATTENZIONE: " + messaggio_avviso, (10, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()