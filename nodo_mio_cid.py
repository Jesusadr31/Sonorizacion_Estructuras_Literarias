import socket
import time
import re

class NodoTexto:
    def __init__(self, nombre, archivo_texto, host='localhost', port=5000):
        self.nombre = nombre
        self.archivo_texto = archivo_texto
        self.host = host
        self.port = port
    
    def cargar_texto(self):
    # Carga y limpia el texto
        with open(self.archivo_texto, 'r', encoding='utf-8') as f:
            texto = f.read()
        return texto
    
    def abreviar_oraciones(self, texto):
    # Divide el texto en oraciones
        oraciones = re.split(r'[.!?]+', texto)
        return [o.strip() for o in oraciones if o.strip()]
    
    def calcular_complejidad(self, oracion):
    # Calcula un valor numérico basado en características del texto.
    # Longitud promedio de palabras
        palabras = oracion.split()
    # Nota y velocidad base
        if not palabras:
            return 60, 64  
        long_promedio = sum(len(palabra) for palabra in palabras) / len(palabras)
    # Complejidad sintactica
        num_comas = oracion.count(',')
        num_y = oracion.lower().count(' y ')
        num_que = oracion.lower().count(' que ')
    # Fórmula de conversióon
        valor = (long_promedio * 8) + (num_comas * 3) + (num_y * 2) + (num_que * 4)
    # Normalizar al rango MIDI [21-108] 
        nota = int(21 + (valor % 88))
    # Velocidad basada en longitud de oracion
        velocidad = min(127, max(40, len(palabras) * 5))
        return nota, velocidad
    
    def procesar_y_enviar(self):
    # Procesa el texto y envía eventos al servidor
        texto = self.cargar_texto()
        oraciones = self.abreviar_oraciones(texto)
        print(f"[{self.nombre}] Conectando al servidor...")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
        # Enviar Id
            sock.send(self.nombre.encode('utf-8'))
            time.sleep(0.5)
            print(f"[{self.nombre}] Procesando {len(oraciones)} oraciones...")
        # Limitar a 100 para demostracion
            for i, oracion in enumerate(oraciones[:100]):  
                if not oracion:
                    continue
                nota, velocidad = self.calcular_complejidad(oracion)
                
            # Formato de Mensaje
                mensaje = f"NOTE_ON|{nota}|{velocidad}|{oracion[:50]}"
                sock.send(mensaje.encode('utf-8'))
            # Esperar confirmacion
                ack = sock.recv(1024)
            # Pausa entre oraciones 
                time.sleep(0.4)
                if (i + 1) % 10 == 0:
                    print(f"[{self.nombre}] Procesadas {i + 1} oraciones")
            
            print(f"[{self.nombre}] Procesamiento completado")
            sock.close()
        
        except Exception as e:
            print(f"[{self.nombre}] Error: {e}")

if __name__ == "__main__":
    nodo = NodoTexto("NODO_MIO_CID", "textos/mio_cid.txt")
    nodo.procesar_y_enviar()
