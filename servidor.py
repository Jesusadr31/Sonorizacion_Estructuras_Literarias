import socket
import threading
import time
from datetime import datetime
import mido


class ServidorMIDI:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.clientes = []
        self.lock = threading.Lock()
        self.log_file = open('resultados/logs/servidor_log.txt', 'w', encoding='utf-8')
        
    # Configurar puerto MIDI virtual
        try:
            self.outport = mido.open_output('Microsoft GS Wavetable Synth')
        except:
            print("Puerto MIDI no disponible, usando modo simulacion")
            self.outport = None
    
    def log(self, mensaje):
    # Registra eventos en el log
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {mensaje}"
        print(log_entry)
        self.log_file.write(log_entry + "\n")
        self.log_file.flush()
    
    def manejar_cliente(self, conexion, direccion):
    #Maneja la conexión de un nodo cliente
        self.log(f"-. Nodo conectado desde {direccion}")
        
        try:
        # Recibir identificación del nodo
            nodo_id = conexion.recv(1024).decode('utf-8')
            self.log(f"Nodo identificado: {nodo_id}")
            
            while True:
                data = conexion.recv(1024).decode('utf-8')
                if not data:
                    break
                
            # Parsear evento MIDI del nodo
                partes = data.split('|')
                if len(partes) >= 3:
                    tipo = partes[0]
                    nota = int(partes[1])
                    velocidad = int(partes[2])
                    texto = partes[3] if len(partes) > 3 else ""
                    
                    self.log(f"{nodo_id} -> Nota: {nota} | Vel: {velocidad} | Texto: '{texto[:30]}...'")
                    
                # Enviar evento MIDI
                    if self.outport:
                        if tipo == "NOTE_ON":
                            msg = mido.Message('note_on', note=nota, velocity=velocidad)
                            self.outport.send(msg)
                        # Duración de la nota
                            time.sleep(0.3)  
                            msg = mido.Message('note_off', note=nota)
                            self.outport.send(msg)
                    
                    # Responder al cliente
                    conexion.send(b"ACK")
        
        except Exception as e:
            self.log(f"Error con {direccion}: {e}")
        finally:
            conexion.close()
            self.log(f"Nodo desconectado: {direccion}")
    
    def iniciar(self):
    # Inicia el servidor
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor_socket.bind((self.host, self.port))
        servidor_socket.listen(5)
        print(f"Servidor iniciado en {self.host}:{self.port}")
        self.log("Esperando nodos de procesamiento...")
        
        try:
            while True:
                conexion, direccion = servidor_socket.accept()
                thread = threading.Thread(target=self.manejar_cliente, args=(conexion, direccion))
                thread.start()
        except KeyboardInterrupt:
            self.log("Servidor detenido")
            servidor_socket.close()
            self.log_file.close()
            if self.outport:
                self.outport.close()

if __name__ == "__main__":
    servidor = ServidorMIDI()
    servidor.iniciar()
