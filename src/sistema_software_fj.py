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
        
        
    