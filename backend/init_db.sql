CREATE DATABASE IF NOT EXISTS modema;
USE modema;

CREATE TABLE IF NOT EXISTS proyectos(
    id INT AUTO_INCREMENT PRIMARY KEY;
    titulo VARCHAR(60),
    descrip TEXT,
    imagen VARCHAR(150)
)

CREATE TABLE IF NOT EXISTS usuarios (
	id INT AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(50),
	contrasenia VARCHAR(50)
);


INSERT INTO usuarios(email, contrasenia) VALUES
('trabajador@modema.com', 'modemaemp');

INSERT INTO proyectos(titulo, descrip, imagen) VALUES
('Automatismo en grupo electrógeno de250 Kw.', 'En un puerto muy importante de la zona sobre el río Iguazú se diseñó y construyó un tablero de control manual/automático para solucionar los problemas de corte de energía automatizando el arranque del grupo, la conexión de energía y la restitución automática al retornar la energía externa con el apagado del grupo electrógeno.', 'images/3.jpg'),
('Montaje de medidores de humedad y espesor.', 'En una importante empresa de la zona de Zárate se montaron dos medidores de humedad del ancho de la máquina formadora de planchas de aglomerado y un medidor de humedad dejando todo el sistema listo para que el fabricante ponga en funcionamiento los equipos. Para el trabajo se buscó compatibilidad de los diferentes tipos de conductores originales contra los nacionales para la interconexión entre los equipos de origen europeos y se realizó la ingeniería de interconexión.', 'images/6.jpg'),
('Cambio de posición de tableros de operación de plataformas hidráulicas.', 'En un puerto importante sobre el río Paraná se cambiaron de posición dos tableros de operación de volcado de camiones cerealeros. Para el trabajo se tuvo que realizar la ingeniería de conexionado ya que no existían planos y posteriormente los planos eléctricos del conexionado.', 'images/8.jpg'),
('Cambio de luminarias en nave de maquina.', 'En una importante empresa de la zona se reemplazaron todas las luminarias gaseosas de la nave y sala de control por otras de LED.', 'images/9.jpg'),
('Armado y montaje de tableros de control.', 'En una empresa de la zona en un sector de la planta se debía realizar un cambio sistema de control automático (Up grade del PLC y software) por tal motivo se construyó montó y conectó un tablero de operación manual para que no se interrumpiera el proceso de operación. Para ello se construyó un tablero con llaves, interruptores e indicadores luminosos se tendió y se conectaron los multipares.', 'images/Controlador-con-micro1.jpg'),
('Armado, mantenimiento y reparación del automatismo de portones industriales.', 'Se realizó el mantenimiento de portones automáticos industriales. También se realizó el diseño del automatismo y el armado del tablero de control como la programación. Se armaron sistemas de control tanto con PLC como con microcontroladores.', 'images/Desarrollo-de-impreso1.jpg'),
('Conexionado de transformador de media tensión de máquina.', 'Se conexionó la entrada de 13,2 Kv y la salida de 380 V del transformador trifásico de alimentación de la una máquina papelera y sus servicios anexos de 3150 Kva.', 'images/Estabilizadores-trifasicos-2.jpg'),
('Chequeo y medición de puestas a tierra.', 'Se revisaron 300 puestas a tierra reparando y generando un informe completo escrito y fotografiado sobre el estado en que se encontró cada elemento y como queda finalizada la intervención.','images/Gabinete1.jpg'),
('Automatismo de un sistema cerrado', 'Se diseña el automatismo de un sistema cerrado de preparador de producto con microcontrolador.', 'images/Planos-1.jpg'),
('Agregado de un sistema de control a través de display táctil y PLC.', 'En una empresa de productos comestibles debían variar la velocidad de nueve motores de una cinta de transporte para diferentes productos. Se montó un PLC con una pantalla táctil para que el operador no tenga que abrir los gabinetes contenedores de los PLC y pueda variar la velocidad de forma segura y cómoda a través de un display táctil dedicado.', 'images/Planos-2.jpg'),
('Ingeniería, supervisión y montaje de puestos de soldadura.', 'En una empresa de fabricación de motocicletas de la zona se realizó la ingeniería de tres nuevas estaciones de soldaduras para el uso de equipos de soldado MIG. La misma cuenta con una capacidad instalada de 200 Kw con un tendido de cable alimentador de 3X150+70 mm sobre bandejas en una distancia de 75 mts. En cada una de las estaciones se instaló un estabilizador trifásico por fase de una potencia de 132Kw cada uno. También se instaló la iluminación de cada línea de soldado y la potencia a un extractor de humos con un arrancador suave de 15 Kw.', 'images/Planos-3.jpg'),
('Ingeniería, de iluminación y potencia de un buque arenero.', 'Se realiza la ingeniería completa de alimentación de potencia de 380 voltios y la iluminación de led en 24 Voltios y 220 voltios de un buque arenero que tiene una instalación eléctrica con motores de corriente continua y alimentación general de 110 voltios.', 'images/Tablero-porton-2.jpg');

