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
    
