Sincronización de Estructuras Literarias mediante un Sistema Distribuido de Análisis Auditivo (MIDI-Sockets). 
Un sistema en Python que utiliza una arquitectura cliente-servidor para transformar la métrica y gramática de obras clásicas (como El Quijote y el Mio Cid) en eventos sonoros MIDI en tiempo real.

🎵 MIDI-Sockets: Sonorización Distribuida de Estructuras Literarias
Este proyecto explora la intersección entre los Sistemas Distribuidos y el Análisis de Datos No Convencional. El objetivo es procesar obras literarias clásicas en nodos independientes, transformando su estructura sintáctica en "firmas sonoras" mediante el protocolo MIDI.

🚀 Características Principales
Arquitectura Distribuida: Implementación de una red en estrella utilizando Sockets TCP/IP en Python.
Procesamiento en Paralelo: Nodos ejecutores que tokenizan, normalizan y cuantifican el corpus textual de forma autónoma.
Mapeo Matemático: Conversión de métricas gramaticales (longitud de palabras, frecuencias, ASCII) a valores MIDI [0-127].
Monitor Central: Nodo orquestador que coordina la carga de trabajo, gestiona la comunicación privada entre nodos y visualiza los eventos en tiempo real.
🛠️ Tecnologías Utilizadas
Lenguaje: Python
Comunicación: Sockets (TCP/IP)
Música Algorítmica: Librerías Mido / Mingus
Corpus: Don Quijote de la Mancha y Cantar de mio Cid
