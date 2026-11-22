# Importamos las herramientas necesarias

from abc import ABC, abstractmethod
import logging

# Creamos la excepcion general del sistema
# Sirve como base para manejar los errores propios del programa.

class ErrorSistema(Exception):
    pass

# Excepcion para datos incorrectos
# Se utiliza cuando un dato ingresado no cumple las validaciones.

class DatosInvalidosError(ErrorSistema):
    pass

# Excepcion para servicios no disponibles
# Indica que se intenta utilizar un servicio que no esta disponible.

class ServicioNoDisponibleError(ErrorSistema):
    pass


# Excepcion para reservas no permitidas
# Se presenta cuando una reserva no puede realizar una accion.
class ReservaNoPermitidaError(ErrorSistema):
    pass


# Excepcion cuando no se encuentra un cliente
# Representa el caso en que no se localiza un cliente.
class ClienteNoEncontradoError(ErrorSistema):
    pass

# Clase abstracta para las entidades del sistema
# Define la estructura general que deben tener las entidades.
class Entidad(ABC):

# Inicializa la entidad con un identificador para reconocerla.
    def __init__(self, identificador):
        self.identificador = identificador

# Metodo que deben implementar las clases hijas
# Permite que cada clase hija muestre su propia informacion.
    
    @abstractmethod
    def mostrar_informacion(self):
        pass

# Clase Cliente que hereda de Entidad
# Guarda los datos de cada cliente y verifica que sean correctos.

class Cliente(Entidad):

# Recibe los datos del cliente y prepara su registro.
    
    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)

# Validamos que el nombre no este vacio.
# Esto evita registrar clientes sin un nombre.
        
        if not nombre.strip():
            raise DatosInvalidosError("El nombre no puede estar vacio")
            
 # Comprobamos que el correo tenga un formato basico.
# Asi evitamos registrar correos que no tengan los datos necesarios.
        
        if "@" not in correo or "." not in correo:
            raise DatosInvalidosError("El correo no es valido")
            
# Verificamos que el telefono tenga solo numeros y al menos 7 digitos.
# Esto permite detectar numeros de telefono incorrectos.
        
        if not telefono.isdigit() or len(telefono) < 7:
            raise DatosInvalidosError("El telefono no es valido")

# Encapsulamos los datos personales.
 # Esto evita que se acceda directamente a estos atributos.
        
        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono

# Consultamos el nombre del cliente.
# Devuelve el nombre sin modificar el dato encapsulado.# Consultamos el nombre del cliente
    
    def obtener_nombre(self):
        return self.__nombre

# Consultamos el correo del cliente.
# Permite conocer el correo que se registro.
    
    def obtener_correo(self):
        return self.__correo

# Consultamos el telefono del cliente.
# Devuelve el telefono almacenado del cliente.
    
    def obtener_telefono(self):
        return self.__telefono

# Mostramos la informacion del cliente.
# Organiza los datos del cliente en un texto para consultarlos.
    
    def mostrar_informacion(self):
        return (
            f"ID: {self.identificador}, "
            f"Nombre: {self.__nombre}, "
            f"Correo: {self.__correo}, "
            f"Telefono: {self.__telefono}"
        )

# Clase abstracta que representa los servicios
# Establece las caracteristicas y metodos comunes de los servicios.

class Servicio(ABC):

    def __init__(self, nombre, tarifa_base):
        if tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa debe ser mayor que cero")

        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.disponible = True

    # Metodo para calcular el costo del servicio.
    # Cada servicio especializado debe realizar su propio calculo.
    
    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass

    # Metodo para describir el servicio.
    # Permite que cada servicio muestre sus caracteristicas.
    
    @abstractmethod
    def describir_servicio(self):
        pass

    # Metodo para validar los parametros del servicio.
    # Cada servicio debe comprobar que la duracion sea correcta.
    
    @abstractmethod
    def validar_parametros(self, duracion):
        pass


# Servicio especializado para reservar salas
# Representa el servicio de alquiler o reserva de una sala.

class ReservaSala(Servicio):

 # Recibe la tarifa y capacidad de la sala para crear el servicio.
    
    def __init__(self, nombre, tarifa_base, capacidad):
        super().__init__(nombre, tarifa_base)
        
# Verificamos que la capacidad sea mayor que cero.
# Esto evita registrar salas sin capacidad valida.
        
        if capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser mayor que cero")

        self.capacidad = capacidad

# Calculamos el costo de la reserva de sala.
# Tiene en cuenta la tarifa, duracion, descuento e impuesto.
    
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)

        subtotal = self.tarifa_base * duracion
        total = subtotal - descuento + (subtotal * impuesto / 100)

        return total

# Describimos las caracteristicas de la sala.
# Devuelve el nombre de la sala y la capacidad que tiene.
    
    def describir_servicio(self):
        return f"Sala: {self.nombre}, Capacidad: {self.capacidad} personas"

# Validamos la duracion de la reserva.
# Evita crear reservas con una duracion igual o menor que cero.
    
    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise DatosInvalidosError("La duracion debe ser mayor que cero")

# Servicio especializado para alquilar equipos
# Representa el servicio de alquiler de equipos.

class AlquilerEquipo(Servicio):

# Recibe la tarifa y cantidad de equipos para registrar el servicio.  

    def __init__(self, nombre, tarifa_base, cantidad):
        super().__init__(nombre, tarifa_base)
        
# Verificamos que la cantidad sea mayor que cero.
# Esto evita registrar una cantidad de equipos incorrecta.
        
        if cantidad <= 0:
            raise DatosInvalidosError("La cantidad debe ser mayor que cero")

        self.cantidad = cantidad

# Calculamos el costo del alquiler de equipos.
# Tiene en cuenta la tarifa, duracion, descuento e impuesto.
    
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)

        subtotal = self.tarifa_base * duracion
        total = subtotal - descuento + (subtotal * impuesto / 100)

        return total

# Describimos los equipos disponibles.
# Muestra el nombre del equipo y la cantidad registrada.
    
    def describir_servicio(self):
        return f"Equipo: {self.nombre}, Cantidad: {self.cantidad}"

# Validamos la duracion del alquiler.
# Comprueba que el tiempo de alquiler sea mayor que cero.
    
    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise DatosInvalidosError("La duracion debe ser mayor que cero")


# Servicio especializado para asesorias
# Representa un servicio de asesoria en un area especifica.

class AsesoriaEspecializada(Servicio):

 # Recibe la tarifa y el area de especialidad de la asesoria.
    
    def __init__(self, nombre, tarifa_base, especialidad):
        super().__init__(nombre, tarifa_base)
        
# Verificamos que la especialidad no este vacia.
# Esto permite identificar correctamente el area de asesoria.
        
        if not especialidad.strip():
            raise DatosInvalidosError("La especialidad no puede estar vacia")

        self.especialidad = especialidad

# Calculamos el costo de la asesoria.
# Tiene en cuenta la tarifa, duracion, descuento e impuesto.
    
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)

        subtotal = self.tarifa_base * duracion
        total = subtotal - descuento + (subtotal * impuesto / 100)

        return total

# Describimos la asesoria especializada.
# Muestra el nombre de la asesoria y su especialidad.
    
    def describir_servicio(self):
        return f"Asesoria: {self.nombre}, Especialidad: {self.especialidad}"

# Validamos la duracion de la asesoria.
# Comprueba que la duracion sea mayor que cero.
    
    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise DatosInvalidosError("La duracion debe ser mayor que cero")

# Clase que administra las reservas
# Relaciona un cliente con un servicio y controla el estado de la reserva.

class Reserva:

# Verifica los objetos recibidos y crea la reserva pendiente
    
    def __init__(self, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El cliente no es valido")
            
# Comprobamos que el objeto recibido sea un cliente.
# Esto evita crear reservas con datos de otro tipo.
        
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El servicio no es valido")
            
# Verificamos que la duracion de la reserva sea valida.
        
        servicio.validar_parametros(duracion)

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        
# Confirmamos la reserva.
# Cambia la reserva a confirmada si el servicio esta disponible.
    
    def confirmar(self):

# Verificamos que el servicio se encuentre disponible.
        
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError("El servicio no esta disponible")
            
# Comprobamos que la reserva este pendiente.
        
        if self.estado != "Pendiente":
            raise ReservaNoPermitidaError("La reserva no se puede confirmar")

        self.estado = "Confirmada"

# Cancelamos la reserva.
# Cambia el estado de la reserva y evita cancelarla dos veces.
    
    def cancelar(self):
        if self.estado == "Cancelada":
            raise ReservaNoPermitidaError("La reserva ya fue cancelada")

        self.estado = "Cancelada"

# Procesamos la reserva y calculamos su costo.
# Verifica que este confirmada y controla los errores que puedan aparecer.
    
    def procesar(self):
        try:
            
 # Comprobamos que la reserva este confirmada.
            
            if self.estado != "Confirmada":
                raise ReservaNoPermitidaError(
                    "La reserva debe estar confirmada"
                )
 # Calculamos el costo del servicio.
            
            costo = self.servicio.calcular_costo(self.duracion)
            self.estado = "Procesada"
            
 # Capturamos errores relacionados con datos incorrectos.
 # Se genera una excepcion de reserva y se conserva el error original.
        
        except DatosInvalidosError as error:
            raise ReservaNoPermitidaError(
                "No fue posible procesar la reserva"
            ) from error
            
 # Permitimos que el error de reserva continue hacia quien lo maneja.
        
        except ReservaNoPermitidaError:
            raise

        return costo

# Mostramos los datos de la reserva.
# Devuelve un resumen con el cliente, servicio, duracion y estado.
    
    def mostrar_reserva(self):
        return (
            f"Cliente: {self.cliente.obtener_nombre()}, "
            f"Servicio: {self.servicio.nombre}, "
            f"Duracion: {self.duracion}, "
            f"Estado: {self.estado}"
        )
        
# Configuramos el registro de eventos y errores.
# Permite guardar las operaciones y los errores en un archivo de texto.

logging.basicConfig(
    filename="registro_sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Funcion para registrar los eventos del sistema.
# Guarda en el archivo de registro las operaciones realizadas correctamente.

def registrar_evento(mensaje):
    logging.info(mensaje)


# Funcion para registrar los errores.
# Guarda en el archivo los errores detectados durante la ejecucion.

def registrar_error(mensaje):
    logging.error(mensaje)
    
# Clase para realizar calculos de costos
# Permite calcular costos utilizando diferentes formatos de datos.

from functools import singledispatchmethod


class CalculadoraCostos:

# Calculamos el costo segun el tipo de dato recibido.
# Si el formato no es reconocido, genera un error de datos invalidos.
    
    @singledispatchmethod
    def calcular(self, datos):
        raise DatosInvalidosError("Formato de datos no valido")

# Calculamos el costo usando una tupla.
# Recibe la tarifa y la duracion para obtener el costo basico.
    
    @calcular.register
    def _(self, datos: tuple):
        tarifa, duracion = datos
        return tarifa * duracion

# Calculamos el costo usando un diccionario.
# Permite incluir tarifa, duracion, descuento e impuesto.
    
    @calcular.register
    def _(self, datos: dict):
        tarifa = datos["tarifa"]
        duracion = datos["duracion"]
        descuento = datos.get("descuento", 0)
        impuesto = datos.get("impuesto", 0)

        subtotal = tarifa * duracion
        return subtotal - descuento + (subtotal * impuesto / 100)
        
# Funcion principal del sistema
# Ejecuta el registro de clientes, crea servicios y procesa una reserva.

def main():

    print("SISTEMA DE GESTION SOFTWARE FJ")

# Creamos la lista de clientes.
# Aqui almacenamos los clientes que se registran correctamente.
    
    clientes = []

# Creamos algunos clientes.
# Utilizamos try para detectar errores durante el registro.
    
    try:
        cliente1 = Cliente(1, "Fredy Pimentel", "fredy@gmail.com", "3118447352")
        clientes.append(cliente1)
        registrar_evento("Cliente Fredy Pimentel registrado")

        cliente2 = Cliente(2, "Danny Galindo", "danny@gmail.com", "3132182789")
        clientes.append(cliente2)
        registrar_evento("Cliente Danny Galindo registrado")

    except DatosInvalidosError as error:
        print("Error al registrar cliente:", error)
        registrar_error(str(error))

# Creamos los servicios.
# En esta lista almacenamos las diferentes opciones que ofrece el sistema.
    
    servicios = []

    try:
        sala = ReservaSala("Sala de reuniones", 50000, 10)
        equipo = AlquilerEquipo("Video beam", 30000, 5)
        asesoria = AsesoriaEspecializada("Asesoria tecnica", 80000, "Electronica")

        servicios.append(sala)
        servicios.append(equipo)
        servicios.append(asesoria)

        registrar_evento("Servicios registrados correctamente")

    except DatosInvalidosError as error:
        print("Error al crear servicios:", error)
        registrar_error(str(error))

    # Creamos la lista de reservas.
    # Aqui se pueden almacenar las reservas realizadas por los clientes.
    
    reservas = []
    
    # Creamos y procesamos una reserva.
    # Se confirma antes de calcular el costo del servicio.
    
    try:
        reserva1 = Reserva(cliente1, sala, 2)
        reserva1.confirmar()
        reservas.append(reserva1)

        costo = reserva1.procesar()

        print(reserva1.mostrar_reserva())
        print("Costo:", costo)

        registrar_evento("Reserva 1 procesada correctamente")

    except ErrorSistema as error:
        print("Error en la reserva:", error)
        registrar_error(str(error))
        
# Funcion para realizar las pruebas del sistema
# Ejecuta diez situaciones para comprobar operaciones correctas y manejo de errores.

def realizar_pruebas():

    print("\nINICIO DE LAS PRUEBAS")

# Creamos datos para las pruebas de reservas.
# Estos objetos sirven como base para realizar varias pruebas.
    
    cliente_prueba = Cliente(99, "Cliente Prueba", "prueba@gmail.com", "3001234567")
    sala_prueba = ReservaSala("Sala de prueba", 50000, 15)

# Prueba 1: registrar un cliente valido.
# Comprueba que el sistema permita registrar un cliente con datos correctos.
    
    try:
        cliente = Cliente(3, "Pedro Gomez", "pedro@gmail.com", "3201234567")
        print("Prueba 1: Cliente registrado correctamente")
        registrar_evento("Prueba 1 exitosa")

    except DatosInvalidosError as error:
        print("Prueba 1: Error:", error)
        registrar_error(str(error))

# Prueba 2: registrar un cliente con datos incorrectos.
# Comprueba que el sistema detecte y rechace los datos invalidos.
    
    try:
        cliente_malo = Cliente(4, "", "correo", "123")
        print("Prueba 2: Cliente registrado")

    except DatosInvalidosError as error:
        print("Prueba 2: Se detectaron datos incorrectos")
        registrar_error(str(error))

# Prueba 3: crear un servicio valido.
# Comprueba que se pueda crear una sala con datos correctos.
    
    try:
        sala = ReservaSala("Sala principal", 50000, 15)
        print("Prueba 3: Servicio creado correctamente")
        registrar_evento("Prueba 3 exitosa")

    except DatosInvalidosError as error:
        print("Prueba 3: Error:", error)
        registrar_error(str(error))

# Prueba 4: crear un servicio con tarifa incorrecta.
# Comprueba que el sistema no permita crear servicios con tarifa cero.
    
    try:
        equipo_malo = AlquilerEquipo("Computador", 0, 3)
        print("Prueba 4: Servicio creado")

    except DatosInvalidosError as error:
        print("Prueba 4: Se detecto una tarifa incorrecta")
        registrar_error(str(error))

# Prueba 5: crear y procesar una reserva correctamente.
# Comprueba que se pueda confirmar y procesar una reserva valida.
    
    try:
        reserva = Reserva(cliente_prueba, sala_prueba, 2)
        reserva.confirmar()
        costo = reserva.procesar()

        print("Prueba 5: Reserva procesada")
        print("Costo:", costo)
        registrar_evento("Prueba 5 exitosa")

    except ErrorSistema as error:
        print("Prueba 5: Error:", error)
        registrar_error(str(error))

# Prueba 6: intentar procesar una reserva sin confirmar.
# Comprueba que el sistema impida procesar reservas pendientes.
    
    try:
        reserva2 = Reserva(cliente_prueba, sala_prueba, 1)
        reserva2.procesar()

    except ReservaNoPermitidaError as error:
        print("Prueba 6: No se permitio procesar la reserva")
        registrar_error(str(error))

    else:
        print("Prueba 6: Operacion realizada")

    finally:
        print("Prueba 6: Proceso finalizado")

# Prueba 7: intentar reservar un servicio no disponible.
# Comprueba que el sistema no permita confirmar una reserva sin disponibilidad.
    
    try:
        sala_prueba.disponible = False
        reserva3 = Reserva(cliente_prueba, sala_prueba, 1)
        reserva3.confirmar()

    except ServicioNoDisponibleError as error:
        print("Prueba 7: Servicio no disponible")
        registrar_error(str(error))

# Prueba 8: cancelar una reserva.
# Comprueba que el sistema permita cambiar el estado de una reserva a cancelada.
    
    try:
        reserva4 = Reserva(cliente_prueba, sala_prueba, 1)
        reserva4.cancelar()

        print("Prueba 8: Reserva cancelada")
        registrar_evento("Prueba 8 exitosa")

    except ErrorSistema as error:
        print("Prueba 8: Error:", error)
        registrar_error(str(error))

# Prueba 9: crear una reserva con duracion incorrecta.
# Comprueba que el sistema rechace una reserva cuya duracion sea cero.
    
    try:
        reserva5 = Reserva(cliente_prueba, sala_prueba, 0)

    except DatosInvalidosError as error:
        print("Prueba 9: Duracion incorrecta detectada")
        registrar_error(str(error))

# Prueba 10: calcular costos con diferentes datos.
# Comprueba el calculo basico y el calculo con descuento e impuesto.
    
    try:
        calculadora = CalculadoraCostos()

        costo1 = calculadora.calcular((50000, 2))
        costo2 = calculadora.calcular({
            "tarifa": 50000,
            "duracion": 2,
            "descuento": 5000,
            "impuesto": 19
        })

        print("Prueba 10: Calculos realizados")
        print("Costo basico:", costo1)
        print("Costo con descuento e impuesto:", costo2)

        registrar_evento("Prueba 10 exitosa")

    except (DatosInvalidosError, KeyError, TypeError) as error:
        print("Prueba 10: Error en el calculo:", error)
        registrar_error(str(error))

    print("\nFIN DE LAS PRUEBAS")

# Ejecutamos el programa
# Esta condicion permite iniciar el programa cuando se ejecuta este archivo.

if __name__ == "__main__":
    main()
    realizar_pruebas()    
