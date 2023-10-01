import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)

# Inicializa a captura de vídeo (definida como None inicialmente)
cap = None

# Função para gerar quadros da câmera
def generate_frames():
    global cap  # Use a variável global cap
    while True:
        if cap is not None:
            success, frame = cap.read()  # Lê um quadro da câmera

            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    continue
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Rota inicial da página
@app.route('/')
def index():
    return render_template('homepage.html')

# Rota para a transmissão ao vivo
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Rota para iniciar a transmissão
@app.route('/start_stream')
def start_stream():
    global cap
    cap = cv2.VideoCapture(0)  # Inicia uma nova captura de vídeo
    return "Streaming is already running"

# Rota para parar a transmissão
@app.route('/stop_stream')
def stop_stream():
    global cap
    if cap is not None and cap.isOpened():
        cap.release()  # Libera a câmera
        cap = None
        return "Streaming stopped"
    return "Streaming is not running"

if __name__ == "__main__":
    app.run(debug=True)
