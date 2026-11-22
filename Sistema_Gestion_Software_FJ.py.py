
# Importamos las herramientas necesarias
from abc import ABC, abstractmethod
import logging


# Creamos la excepcion general del sistema
class ErrorSistema(Exception):
    pass


# Excepcion para datos incorrectos
class DatosInvalidosError(ErrorSistema):
    pass


# Excepcion para servicios no disponibles
class ServicioNoDisponibleError(ErrorSistema):
    pass


# Excepcion para reservas no permitidas
class ReservaNoPermitidaError(ErrorSistema):
    pass


# Excepcion cuando no se encuentra un cliente
class ClienteNoEncontradoError(ErrorSistema):
    pass

# Clase abstracta para las entidades del sistema
class Entidad(ABC):

    def __init__(self, identificador):
        self.identificador = identificador

    # Metodo que deben implementar las clases hijas
    @abstractmethod
    def mostrar_informacion(self):
        pass


# Clase Cliente que hereda de Entidad
class Cliente(Entidad):

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)

        # Validamos los datos personales
        if not nombre.strip():
            raise DatosInvalidosError("El nombre no puede estar vacio")

        if "@" not in correo or "." not in correo:
            raise DatosInvalidosError("El correo no es valido")

        if not telefono.isdigit() or len(telefono) < 7:
            raise DatosInvalidosError("El telefono no es valido")

        # Encapsulamos los datos personales
        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono

    # Consultamos el nombre del cliente
    def obtener_nombre(self):
        return self.__nombre

    # Consultamos el correo del cliente
    def obtener_correo(self):
        return self.__correo

    # Consultamos el telefono del cliente
    def obtener_telefono(self):
        return self.__telefono

    # Mostramos la informacion del cliente
    def mostrar_informacion(self):
        return (
            f"ID: {self.identificador}, "
            f"Nombre: {self.__nombre}, "
            f"Correo: {self.__correo}, "
            f"Telefono: {self.__telefono}"
        )

# Clase abstracta que representa los servicios
class Servicio(ABC):

    def __init__(self, nombre, tarifa_base):
        if tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa debe ser mayor que cero")

        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.disponible = True

    # Metodo para calcular el costo del servicio
    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass

    # Metodo para describir el servicio
    @abstractmethod
    def describir_servicio(self):
        pass

    # Metodo para validar los parametros del servicio
    @abstractmethod
    def validar_parametros(self, duracion):
        pass


# Servicio especializado para reservar salas
class ReservaSala(Servicio):

    def __init__(self, nombre, tarifa_base, capacidad):
        super().__init__(nombre, tarifa_base)

        if capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser mayor que cero")

        self.capacidad = capacidad

    # Calculamos el costo de la reserva de sala
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)

        subtotal = self.tarifa_base * duracion
        total = subtotal - descuento + (subtotal * impuesto / 100)

        return total

    # Describimos las caracteristicas de la sala
    def describir_servicio(self):
        return f"Sala: {self.nombre}, Capacidad: {self.capacidad} personas"

    # Validamos la duracion de la reserva
    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise DatosInvalidosError("La duracion debe ser mayor que cero")


# Servicio especializado para alquilar equipos
class AlquilerEquipo(Servicio):

    def __init__(self, nombre, tarifa_base, cantidad):
        super().__init__(nombre, tarifa_base)

        if cantidad <= 0:
            raise DatosInvalidosError("La cantidad debe ser mayor que cero")

        self.cantidad = cantidad

    # Calculamos el costo del alquiler de equipos
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)

        subtotal = self.tarifa_base * duracion
        total = subtotal - descuento + (subtotal * impuesto / 100)

        return total

    # Describimos los equipos disponibles
    def describir_servicio(self):
        return f"Equipo: {self.nombre}, Cantidad: {self.cantidad}"

    # Validamos la duracion del alquiler
    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise DatosInvalidosError("La duracion debe ser mayor que cero")


# Servicio especializado para asesorias
class AsesoriaEspecializada(Servicio):

    def __init__(self, nombre, tarifa_base, especialidad):
        super().__init__(nombre, tarifa_base)

        if not especialidad.strip():
            raise DatosInvalidosError("La especialidad no puede estar vacia")

        self.especialidad = especialidad

    # Calculamos el costo de la asesoria
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)

        subtotal = self.tarifa_base * duracion
        total = subtotal - descuento + (subtotal * impuesto / 100)

        return total

    # Describimos la asesoria especializada
    def describir_servicio(self):
        return f"Asesoria: {self.nombre}, Especialidad: {self.especialidad}"

    # Validamos la duracion de la asesoria
    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise DatosInvalidosError("La duracion debe ser mayor que cero")
# Clase que administra las reservas
class Reserva:

    def __init__(self, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El cliente no es valido")

        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El servicio no es valido")

        servicio.validar_parametros(duracion)

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    # Confirmamos la reserva
    def confirmar(self):
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError("El servicio no esta disponible")

        if self.estado != "Pendiente":
            raise ReservaNoPermitidaError("La reserva no se puede confirmar")

        self.estado = "Confirmada"

    # Cancelamos la reserva
    def cancelar(self):
        if self.estado == "Cancelada":
            raise ReservaNoPermitidaError("La reserva ya fue cancelada")

        self.estado = "Cancelada"

    # Procesamos la reserva y calculamos su costo
    def procesar(self):
        try:
            if self.estado != "Confirmada":
                raise ReservaNoPermitidaError(
                    "La reserva debe estar confirmada"
                )

            costo = self.servicio.calcular_costo(self.duracion)
            self.estado = "Procesada"

        except DatosInvalidosError as error:
            raise ReservaNoPermitidaError(
                "No fue posible procesar la reserva"
            ) from error

        except ReservaNoPermitidaError:
            raise

        return costo

    # Mostramos los datos de la reserva
    def mostrar_reserva(self):
        return (
            f"Cliente: {self.cliente.obtener_nombre()}, "
            f"Servicio: {self.servicio.nombre}, "
            f"Duracion: {self.duracion}, "
            f"Estado: {self.estado}"
        )
    # Configuramos el registro de eventos y errores
logging.basicConfig(
    filename="registro_sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Funcion para registrar los eventos del sistema
def registrar_evento(mensaje):
    logging.info(mensaje)


# Funcion para registrar los errores
def registrar_error(mensaje):
    logging.error(mensaje)
# Clase para realizar calculos de costos
from functools import singledispatchmethod


class CalculadoraCostos:

    # Calculamos el costo segun el tipo de dato recibido
    @singledispatchmethod
    def calcular(self, datos):
        raise DatosInvalidosError("Formato de datos no valido")

    # Calculamos el costo usando una tupla
    @calcular.register
    def _(self, datos: tuple):
        tarifa, duracion = datos
        return tarifa * duracion

    # Calculamos el costo usando un diccionario
    @calcular.register
    def _(self, datos: dict):
        tarifa = datos["tarifa"]
        duracion = datos["duracion"]
        descuento = datos.get("descuento", 0)
        impuesto = datos.get("impuesto", 0)

        subtotal = tarifa * duracion
        return subtotal - descuento + (subtotal * impuesto / 100)
# Funcion principal del sistema
def main():

    print("SISTEMA DE GESTION SOFTWARE FJ")

    # Creamos la lista de clientes
    clientes = []

    # Creamos algunos clientes
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

    # Creamos los servicios
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

    # Creamos las reservas
    reservas = []

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
def realizar_pruebas():

    print("\nINICIO DE LAS PRUEBAS")

        # Creamos datos para las pruebas de reservas
    cliente_prueba = Cliente(99, "Cliente Prueba", "prueba@gmail.com", "3001234567")
    sala_prueba = ReservaSala("Sala de prueba", 50000, 15)

    # Prueba 1: registrar un cliente valido
    try:
        cliente = Cliente(3, "Pedro Gomez", "pedro@gmail.com", "3201234567")
        print("Prueba 1: Cliente registrado correctamente")
        registrar_evento("Prueba 1 exitosa")

    except DatosInvalidosError as error:
        print("Prueba 1: Error:", error)
        registrar_error(str(error))

    # Prueba 2: registrar un cliente con datos incorrectos
    try:
        cliente_malo = Cliente(4, "", "correo", "123")
        print("Prueba 2: Cliente registrado")

    except DatosInvalidosError as error:
        print("Prueba 2: Se detectaron datos incorrectos")
        registrar_error(str(error))

    # Prueba 3: crear un servicio valido
    try:
        sala = ReservaSala("Sala principal", 50000, 15)
        print("Prueba 3: Servicio creado correctamente")
        registrar_evento("Prueba 3 exitosa")

    except DatosInvalidosError as error:
        print("Prueba 3: Error:", error)
        registrar_error(str(error))

    # Prueba 4: crear un servicio con tarifa incorrecta
    try:
        equipo_malo = AlquilerEquipo("Computador", 0, 3)
        print("Prueba 4: Servicio creado")

    except DatosInvalidosError as error:
        print("Prueba 4: Se detecto una tarifa incorrecta")
        registrar_error(str(error))

    # Prueba 5: crear y procesar una reserva correctamente
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

    # Prueba 6: intentar procesar una reserva sin confirmar
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

    # Prueba 7: intentar reservar un servicio no disponible
    try:
        sala_prueba.disponible = False
        reserva3 = Reserva(cliente_prueba, sala_prueba, 1)
        reserva3.confirmar()

    except ServicioNoDisponibleError as error:
        print("Prueba 7: Servicio no disponible")
        registrar_error(str(error))

    # Prueba 8: cancelar una reserva
    try:
        reserva4 = Reserva(cliente_prueba, sala_prueba, 1)
        reserva4.cancelar()

        print("Prueba 8: Reserva cancelada")
        registrar_evento("Prueba 8 exitosa")

    except ErrorSistema as error:
        print("Prueba 8: Error:", error)
        registrar_error(str(error))

    # Prueba 9: crear una reserva con duracion incorrecta
    try:
        reserva5 = Reserva(cliente_prueba, sala_prueba, 0)

    except DatosInvalidosError as error:
        print("Prueba 9: Duracion incorrecta detectada")
        registrar_error(str(error))

    # Prueba 10: calcular costos con diferentes datos
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
if __name__ == "__main__":
    main()
    realizar_pruebas()    