"""
=============================================================================
SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS
Empresa: Software FJ
Curso: Programación 213023 - UNAD
FASE 4 - Programación Orientada a Objetos + Manejo Avanzado de Excepciones
=============================================================================
"""

import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime

# Configuración del Sistema de Logs

logging.basicConfig(
    filename="sistema_fj_logs.txt",
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="uft-8",
)
logger = logging.getLogger("SistemaFJ")

def log_evento(mensaje: str, nivel: str = "info"):
    """Registra un evento en el archivo de logs y en consola."""
    niveles = {
        "info":     logger.info,
        "warning":  logger.warning,
        "error":    logger.error,
        "critical": logger.critical,
        "debug":    logger.debug,
    }
    niveles.get(nivel, logger.info)(mensaje)
    print(f" [LOG-{nivel.upper()}] {mensaje}")
    

# Excepciones Personalizadas


class ErrorSistemaFJ(Exception):
    """Excepción base del sistema Software FJ."""
    def __init__(self, mensaje: str, codigo: int = 0):
        super().__init__(mensaje)
        self.codigo = codigo
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def __str__(self):
        return f"[Codigo {self.codigo}] {super().__str__()} ({self.timestamp})"
    

class ErrorClienteInvalido(ErrorSistemaFJ):
    """Se lanza cuando los datos del cliente no son válidos."""
    pass


class ErrorServicioNoDisponible(ErrorSistemaFJ):
    """Se lanza cuando los datos del cliente no son válidos."""
    pass


class ErrorReservaInvalida(ErrorSistemaFJ):
    """Se lanza cuando una reserva no puede procesarse."""
    pass


class ErrorDuracionInvalida(ErrorSistemaFJ):
    """Se lanza cuando la duración proporcionada no es valida."""
    pass


class ErrorCalculoCosto(ErrorSistemaFJ):
    """Se lanza cuando ocurre un error en el cálculo de costos."""
    pass


# Clase Abstracta Base - Entidad del Sistema

class EntidadSistema(ABC):
    """
    Clase abstracta base que representa cualquier entidad del sistema.
    Implementa abstracción y define la interfaz mínima obligatoria.
    """
    _contador_id = 0
    
    def __init__(self, nombre: str):
        EntidadSistema._contador_id += 1
        self._id = EntidadSistema._contador_id
        self._nombre = nombre
        self._fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    @property
    def id(self):
        return self._id
    
    @property
    def nombre(self):
        return self._nombre
    
    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción completa de la entidad."""
        pass
    
    @abstractmethod
    def validar(self) -> bool:
        """Valida que la entidad tenga datos correctos."""
        pass
    
    def __repr__(self):
        return f"{self.__class__.__name__}(id={self._id}, nombre='{self._nombre}')"
    

# Clase Cliente - Encapsulación y validaciones robustas

class Cliente(EntidadSistema):
    """
    Representa un cliente de Software FJ.
    Implementa encapsulación completa con propiedades y setters validados.
    """
    
    def __init__(self, nombre: str, email: str, telefono: str, documento: str):
        super().__init__(nombre)
        self.__email = None
        self.__telefono = None
        self.__documento = None
        self.__reservas = []
        self.email = email
        self.telefono = telefono
        self.documento = documento
        
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, valor: str):
        if not valor or "@" not in valor or "." not in valor.split("@")[-1]:
            raise ErrorClienteInvalido(
                f"Email Invalido: '{valor}'", codigo=101
            )
        self.__email = valor.strip().lower()
        
    @property
    def telefono(self):
        return self.__telefono
    
    @telefono.setter
    def telefono(self, valor: str):
        digitos = str(valor).replace(" ", "").replace("-", "")
        if not digitos.isdigit() or len(digitos) < 7:
            raise ErrorClienteInvalido(
                f"Telefono Invalido: '{valor}'. Debe contener al menos 7 digitos.", codigo=102
            )
        self.__telefono = digitos
        
    @property
    def documento(self):
        return self.__documento
    
    @documento.setter
    def documento(self, valor: str):
        if not str(valor).strip().isdigit() or len(str(valor).strip()) < 6:
            raise ErrorClienteInvalido(
                f"Documento Invalido: '{valor}'. Solo digitos, minimo 6.", codigo=103
            )
        self.__documento = str(valor).strip()
        
    @property
    def reservas(self):
        return list(self.__reservas)
    
    def agregar_reserva(self, reserva):
        self.__reservas.append(reserva)
        
    def describir(self) -> str:
        return (
            f"Cliente #{self._id} | Nombre: {self._nombre} | "
            f"Email: {self.__email} | Tel: {self.__telefono} | "
            f"Doc: {self.__documento} | Reservas: {len(self.__reservas)}"
        )
        
    def validar(self) -> bool:
        return bool(self.__email and self.__telefono and self.__documento)

    
# Clase Abstracta Servicio + 3 servicios especializados

class Servicio(EntidadSistema):
    """
    Clase abstracta que representa un servicio ofrecido por Sosftware FJ.
    Define la interfaz para calcular costos, describir y validar parametros.
    """
    IVA = 0.19
    
    def __init__(self, nombre: str, precio_base: float, disponible: bool = True):
        super().__init__(nombre)
        if precio_base <= 0:
            raise ErrorServicioNoDisponible(
                f"El precio base deb ser positivo. Se recibio: {precio_base}", codigo=201
            )
        self._precio_base = precio_base
        self._disponible = disponible
        
    @property
    def precio_base(self):
        return self._precio_base
    
    @property
    def disponible(self):
        return self._disponible
    
    @disponible.setter
    def disponible(self, valor: bool):
        self._disponible = valor
        
    @abstractmethod
    def calcular_costo(self, horas: float) -> float:
        pass
    
    def calcular_costo_con_iva(self, horas: float) -> float:
        """Calcula el costo incluyendo IVA."""
        return self.calcular_costo(horas) * (1 + self.IVA)
    
    def calcular_costo_con_descuento(self, horas: float, descuento: float = 0.0) -> float:
        """Calcula el costo con descuento opcional."""
        if not (0 <= descuento <= 1):
            raise ErrorCalculoCosto(
                f"Descuento Inválido: {descuento}. Debe estar entre 0 y 1.", codigo=301
            )
        return self.calcular_costo(horas) * (1 - descuento)
    
    def calcular_costo_total(self, horas: float, descuento: float = 0.0, incluir_iva: bool = True) -> float:
        """Calculo completo con descuento e IVA opcionales."""
        costo = self.calcular_costo_con_descuento(horas, descuento)
        if incluir_iva:
            costo *= (1 + self.IVA)
        return round(costo, 2)
    
    @abstractmethod
    def validar_parametros(self, horas: float) -> bool:
        pass
    
    def validar(self) -> bool:
        return self.disponible and self._precio_base > 0
    
    
# Servicio 1: Reserva de Sala


class ReservaSala(Servicio):
    """Servicio de reserva de salas de reuniones o conferencias."""
    
    HORAS_MAX = 8
    HORAS_MIN = 1
    
    def __init__(self, nombre: str, capacidad: int, precio_hora: float, disponible: bool = True):
        super().__init__(nombre, precio_hora, disponible)
        if capacidad <= 0:
            raise ErrorServicioNoDisponible(
                f"La capacidad de la sala debe ser positiva: {capacidad}", codigo=202
            )
        self.__capacidad = capacidad
        
    @property
    def capacidad(self):
        return self.__capacidad
    
    def calcular_costo(self, horas: float) -> float:
        self.validar_parametros(horas)
        return self._precio_base * horas
    
    def validar_parametros(self, horas: float) -> bool:
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ErrorDuracionInvalida(
                f"Horas inválidas para ReservaSala: {horas}", codigo=401
            )
        if horas > self.HORAS_MAX:
            raise ErrorDuracionInvalida(
                f"Una sala no puede reservarse mas de {self.HORAS_MAX} horas. Se solicito: {horas}", codigo=402
            )
        if horas < self.HORAS_MIN:
            raise ErrorDuracionInvalida(
                f"La reserva minima es {self.HORAS_MIN} hora(s). Se solicito: {horas}", codigo=403
            )
        return True
    
    def describir(self) -> str:
        estado = "Disponible" if self._disponible else "No Disponible"
        return (
            f"[SALA] {self._nombre} | Capacidad: {self.__capacidad} personas | "
            f"Precio/hora: ${self._precio_base:,.0f} COP | Estado: {estado}"
        )
        

# Servicio 2: Alquiler de Equipos

class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos tecnológicos."""
    
    DIAS_MAX = 30
    
    def __init__(self, nombre: str, tipo_equipo: str, precio_dia: float, stock: int, disponible: bool = True):
        super().__init__(nombre, precio_dia, disponible)
        if stock < 0:
            raise ErrorServicioNoDisponible(
                f"El stock no puede ser negativo: {stock}", codigo=203
            )
        self.__tipo_equipo = tipo_equipo
        self.__stock = stock
        
    @property
    def stock(self):
        return self.__stock
    
    def reducir_stock(self):
        if self.__stock <=0:
            raise ErrorServicioNoDisponible(
                f"Sin stock disponible para: {self._nombre}", codigo=204
            )
        self.__stock -= 1
        if self.__stock == 0:
            self._disponible = False
            
    def calcular_costo(self, dias: float) -> float:
        self.validar_parametros(dias)
        return self._precio_base * dias
    
    def validar_parametros(self, dias: float) -> bool:
        if not isinstance(dias, (int, float)) or dias <= 0:
            raise ErrorDuracionInvalida(
                f"El alquiler maximo es {self.DIAS_MAX} dias. Se solicitó: {dias}", codigo=405
            )
        return True
    
    def describir(self) -> str:
        estado = "Disponible" if self._disponible else "Agotado"
        return (
            f"[EQUIPO] {self._nombre} | Tipo: {self.__tipo_equipo} | "
            f"Precio/dia: ${self._precio_base:,.0f} COP | "
            f"Stock: {self.__stock} | Estado: {estado}"
        )
        
        
# Servicio 3: Asesoria Especializada

class AsesoriaEspecializada(Servicio):
    """Servicio de asesoria técnica o empresarial especializada."""
    
    ESPECIALIDADES = ["sistemas", "redes", "base de datos", "seguridad", "negocios"]
    
    def __init__(self, nombre: str, especialidad: str, precio_hora: float, asesor: str, disponible: bool = True):
        super().__init__(nombre, precio_hora, disponible)
        especialidad_lower = especialidad.lower()
        if especialidad_lower not in self.ESPECIALIDADES:
            raise ErrorServicioNoDisponible(
                f"Especialidad '{especialidad}' no valida. Opciones: {self.ESPECIALIDADES}", codigo=205
            )
        self.__especialidad = especialidad_lower
        self.__asesor = asesor
        
    @property
    def especialidad(self):
        return self.__especialidad
    
    def calcular_costo(self, horas: float) -> float:
        self.validar_parametros(horas)
        return self._precio_base * horas * 1.15
    
    def validar_parametros(self, horas: float) -> bool:
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ErrorDuracionInvalida(
                f"Horas inválidas para Asesoria: {horas}", codigo=406
            )
        if horas > 4:
            raise ErrorDuracionInvalida(
                "Una asesoria no puede superar 4 horas por sesión.", codigo=407
            )
        return True
    
    def describir(self) -> str:
        estado = "Disponible" if self._disponible else "No Disponible"
        return (
            f"[ASESORIA] {self._nombre} | Especialidad: {self.__especialidad.title()} | "
            f"Asesor: {self.__asesor} | Precio/hora: ${self._precio_base:,.0f} COP | Estado: {estado}"
        )
        
# Clase Reserva

class Reserva(EntidadSistema):
    """
    Integra un cliente, un servicio, duración y estado.
    Implementa confirmación, cancelación y procesamiento con manejo de excepciones.
    """

    ESTADOS = ["pendiente", "confirmada", "cancelada", "procesada"]

    def __init__(self, cliente: Cliente, servicio: Servicio, duracion: float, descuento: float = 0.0):
        nombre_reserva = f"Reserva-{cliente.nombre}-{servicio.nombre}"
        super().__init__(nombre_reserva)
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__descuento = descuento
        self.__estado = "pendiente"
        self.__costo_total = 0.0
        self.__fecha_reserva = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    def confirmar(self) -> bool:
        """
        Confirma la reserva validando disponibilidad y calculando el costo.
        Usa try/except/else/finally para manejo completo de excepciones.
        """
        try:
            if self.__estado != "pendiente":
                raise ErrorReservaInvalida(
                    f"La reserva #{self._id} ya está en estado '{self.__estado}'.", codigo=501
                )
            if not self.__servicio.disponible:
                raise ErrorServicioNoDisponible(
                    f"El servicio '{self.__servicio.nombre}' no está disponible.", codigo=502
                )
            if not self.__cliente.validar():
                raise ErrorClienteInvalido(
                    f"El cliente '{self.__cliente.nombre}' tiene datos incompletos.", codigo=503
                )
            self.__costo_total = self.__servicio.calcular_costo_total(
                self.__duracion, self.__descuento, incluir_iva=True
            )

        except (ErrorServicioNoDisponible, ErrorClienteInvalido, ErrorDuracionInvalida) as e:
            log_evento(f"Error al confirmar reserva #{self._id}: {e}", "error")
            self.__estado = "cancelada"
            raise ErrorReservaInvalida(
                f"No se pudo confirmar la reserva: {e}", codigo=504
            ) from e

        except ErrorReservaInvalida as e:
            log_evento(f"Reserva inválida #{self._id}: {e}", "warning")
            raise

        else:
            self.__estado = "confirmada"
            self.__cliente.agregar_reserva(self)
            log_evento(
                f"Reserva #{self._id} CONFIRMADA | Cliente: {self.__cliente.nombre} | "
                f"Servicio: {self.__servicio.nombre} | Costo: ${self.__costo_total:,.2f} COP",
                "info"
            )
            return True

        finally:
            log_evento(
                f"Intento de confirmación finalizado para Reserva #{self._id} "
                f"| Estado resultante: {self.__estado}",
                "debug"
            )

    def cancelar(self, motivo: str = "Sin especificar") -> bool:
        """Cancela una reserva confirmada o pendiente."""
        try:
            if self.__estado == "cancelada":
                raise ErrorReservaInvalida(
                    f"La reserva #{self._id} ya estaba cancelada.", codigo=505
                )
            if self.__estado == "procesada":
                raise ErrorReservaInvalida(
                    f"No se puede cancelar la reserva #{self._id}: ya fue procesada.", codigo=506
                )
            estado_anterior = self.__estado
            self.__estado = "cancelada"

        except ErrorReservaInvalida as e:
            log_evento(f"Error al cancelar reserva #{self._id}: {e}", "warning")
            raise

        else:
            log_evento(
                f"Reserva #{self._id} CANCELADA (estaba '{estado_anterior}') | Motivo: {motivo}",
                "info"
            )
            return True

        finally:
            log_evento(f"Proceso de cancelación completado para Reserva #{self._id}.", "debug")

    def procesar(self) -> bool:
        """Marca la reserva como procesada (servicio ya prestado)."""
        try:
            if self.__estado != "confirmada":
                raise ErrorReservaInvalida(
                    f"Solo se pueden procesar reservas confirmadas. Estado actual: '{self.__estado}'.",
                    codigo=507
                )
            self.__estado = "procesada"

        except ErrorReservaInvalida as e:
            log_evento(f"Error al procesar reserva #{self._id}: {e}", "error")
            raise

        else:
            log_evento(f"Reserva #{self._id} PROCESADA exitosamente.", "info")
            return True

        finally:
            log_evento(f"Intento de procesamiento finalizado para Reserva #{self._id}.", "debug")

    def describir(self) -> str:
        return (
            f"Reserva #{self._id} | Estado: {self.__estado.upper()} | "
            f"Cliente: {self.__cliente.nombre} | Servicio: {self.__servicio.nombre} | "
            f"Duración: {self.__duracion} u. | Descuento: {self.__descuento*100:.0f}% | "
            f"Costo Total (c/IVA): ${self.__costo_total:,.2f} COP | Fecha: {self.__fecha_reserva}"
        )

    def validar(self) -> bool:
        return self.__estado in self.ESTADOS
    
# Sistema Principal - Gestor Sistema

class GestorSistema:
    """Clase principal que orquesta clientes, servicios y reservas."""

    def __init__(self):
        self.__clientes: list = []
        self.__servicios: list = []
        self.__reservas: list = []

    def registrar_cliente(self, nombre, email, telefono, documento):
        try:
            cliente = Cliente(nombre, email, telefono, documento)
            self.__clientes.append(cliente)
            log_evento(f"Cliente REGISTRADO: {cliente.describir()}", "info")
            return cliente
        except ErrorClienteInvalido as e:
            log_evento(f"Fallo al registrar cliente '{nombre}': {e}", "error")
            return None

    def agregar_servicio(self, servicio) -> bool:
        try:
            if not servicio.validar():
                raise ErrorServicioNoDisponible(
                    f"El servicio '{servicio.nombre}' no es válido.", codigo=206
                )
            self.__servicios.append(servicio)
            log_evento(f"Servicio AGREGADO: {servicio.describir()}", "info")
            return True
        except ErrorServicioNoDisponible as e:
            log_evento(f"Fallo al agregar servicio: {e}", "error")
            return False

    def crear_reserva(self, cliente, servicio, duracion, descuento=0.0):
        try:
            if cliente is None:
                raise ErrorReservaInvalida("Cliente no encontrado o inválido.", codigo=508)
            if servicio is None:
                raise ErrorReservaInvalida("Servicio no encontrado o inválido.", codigo=509)
            reserva = Reserva(cliente, servicio, duracion, descuento)
            reserva.confirmar()
            self.__reservas.append(reserva)
            return reserva
        except ErrorReservaInvalida as e:
            log_evento(f"Reserva NO creada: {e}", "error")
            return None
        except Exception as e:
            log_evento(f"Error inesperado al crear reserva: {e}", "critical")
            return None

    def cancelar_reserva(self, reserva, motivo="Sin especificar") -> bool:
        try:
            return reserva.cancelar(motivo)
        except ErrorReservaInvalida as e:
            log_evento(f"No se pudo cancelar: {e}", "warning")
            return False

    def procesar_reserva(self, reserva) -> bool:
        try:
            return reserva.procesar()
        except ErrorReservaInvalida as e:
            log_evento(f"No se pudo procesar: {e}", "error")
            return False

    def listar_clientes(self):
        print("\n" + "═"*70)
        print("  CLIENTES REGISTRADOS")
        print("═"*70)
        for c in self.__clientes:
            print(f"  ► {c.describir()}")
        if not self.__clientes:
            print("  (Sin clientes registrados)")

    def listar_servicios(self):
        print("\n" + "═"*70)
        print("  SERVICIOS DISPONIBLES")
        print("═"*70)
        for s in self.__servicios:
            print(f"  ► {s.describir()}")
        if not self.__servicios:
            print("  (Sin servicios registrados)")

    def listar_reservas(self):
        print("\n" + "═"*70)
        print("  HISTORIAL DE RESERVAS")
        print("═"*70)
        for r in self.__reservas:
            print(f"  ► {r.describir()}")
        if not self.__reservas:
            print("  (Sin reservas registradas)")
            
# Simulaciones

def separador(titulo: str):
    print(f"\n{'─'*70}")
    print(f"  {titulo}")
    print(f"{'─'*70}")


def ejecutar_simulaciones():
    gestor = GestorSistema()

    print("\n" + "█"*70)
    print("   SISTEMA INTEGRAL Software FJ – INICIO DE SIMULACIONES")
    print("█"*70)

    separador("OP 1 | Registro de clientes válidos")
    c1 = gestor.registrar_cliente("Ana Gómez",    "ana.gomez@email.com",  "3001234567", "1020345678")
    c2 = gestor.registrar_cliente("Luis Pérez",   "luis.perez@email.com", "3109876543", "987654321")
    c3 = gestor.registrar_cliente("María Torres", "m.torres@correo.co",   "6017891234", "1100556677")

    separador("OP 2 | Registro de clientes INVÁLIDOS")
    gestor.registrar_cliente("Juan Sin Email",  "email_sin_arroba",  "3001111111", "2233445566")
    gestor.registrar_cliente("Pedro Teléfono",  "pedro@mail.com",    "123",        "3344556677")
    gestor.registrar_cliente("Sin Documento",   "sin.doc@mail.com",  "3002222222", "123")

    separador("OP 3 | Creación de servicios válidos")
    try:
        sala_a    = ReservaSala("Sala Innovación A", capacidad=10, precio_hora=150_000)
        equipo1   = AlquilerEquipo("Laptop HP ProBook", tipo_equipo="Portátil",
                                   precio_dia=80_000, stock=5)
        asesoria1 = AsesoriaEspecializada("Consultoría en Seguridad", especialidad="Seguridad",
                                          precio_hora=200_000, asesor="Dr. Ramírez")
        gestor.agregar_servicio(sala_a)
        gestor.agregar_servicio(equipo1)
        gestor.agregar_servicio(asesoria1)
    except ErrorServicioNoDisponible as e:
        log_evento(f"Error inesperado creando servicio válido: {e}", "critical")

    separador("OP 4 | Creación de servicios INVÁLIDOS")
    try:
        ReservaSala("Sala sin precio", capacidad=5, precio_hora=-500)
    except ErrorServicioNoDisponible as e:
        log_evento(f"Servicio rechazado correctamente: {e}", "warning")
        print(f"  ✗ Error esperado capturado: {e}")

    try:
        AsesoriaEspecializada("Asesoría Inválida", especialidad="Magia",
                              precio_hora=100_000, asesor="Mago")
    except ErrorServicioNoDisponible as e:
        log_evento(f"Especialidad inválida rechazada: {e}", "warning")
        print(f"  ✗ Error esperado capturado: {e}")

    separador("OP 5 | Reserva exitosa – Sala con 10% descuento + IVA")
    r1 = gestor.crear_reserva(c1, sala_a, duracion=3, descuento=0.10)
    if r1:
        print(f"  ✔ {r1.describir()}")

    separador("OP 6 | Reserva exitosa – Alquiler de equipo 5 días")
    r2 = gestor.crear_reserva(c2, equipo1, duracion=5, descuento=0.0)
    if r2:
        print(f"  ✔ {r2.describir()}")

    separador("OP 7 | Reserva exitosa – Asesoría en Seguridad 2 horas")
    r3 = gestor.crear_reserva(c3, asesoria1, duracion=2, descuento=0.05)
    if r3:
        print(f"  ✔ {r3.describir()}")

    separador("OP 8 | Reserva FALLIDA – sala reservada por 12 horas (máx 8)")
    r4 = gestor.crear_reserva(c1, sala_a, duracion=12)
    print(f"  ✗ Reserva resultante: {r4}  (None = rechazada correctamente)")

    separador("OP 9 | Reserva FALLIDA – servicio no disponible")
    sala_cerrada = ReservaSala("Sala Mantenimiento", capacidad=6, precio_hora=100_000, disponible=False)
    r5 = gestor.crear_reserva(c2, sala_cerrada, duracion=2)
    print(f"  ✗ Reserva resultante: {r5}  (None = rechazada correctamente)")

    separador("OP 10 | Cancelar una reserva confirmada")
    if r2:
        exito = gestor.cancelar_reserva(r2, motivo="Cliente solicitó cambio de fecha")
        print(f"  {'✔' if exito else '✗'} Cancelación: {'exitosa' if exito else 'fallida'}")
        print(f"  Estado actual: {r2.estado}")

    separador("OP 11 | Cancelar reserva ya cancelada")
    if r2:
        exito2 = gestor.cancelar_reserva(r2, motivo="Intento duplicado")
        print(f"  Resultado: {'error manejado correctamente' if not exito2 else 'cancelada de nuevo'}")

    separador("OP 12 | Procesar reservas confirmadas")
    if r1:
        gestor.procesar_reserva(r1)
        print(f"  ✔ Estado r1: {r1.estado}")
    if r3:
        gestor.procesar_reserva(r3)
        print(f"  ✔ Estado r3: {r3.estado}")

    separador("OP 13 | Procesar reserva ya procesada")
    if r1:
        resultado = gestor.procesar_reserva(r1)
        print(f"  Resultado: {'error manejado correctamente' if not resultado else 'procesada (inesperado)'}")

    gestor.listar_clientes()
    gestor.listar_servicios()
    gestor.listar_reservas()

    print("\n" + "█"*70)
    print("   SIMULACIONES COMPLETADAS – Revisa 'sistema_fj_logs.txt'")
    print("█"*70)
    log_evento("=== FIN DE SIMULACIONES ===", "info")
    
    
# Punto de Entrada

if __name__ == "__main__":
    ejecutar_simulaciones()
    

    