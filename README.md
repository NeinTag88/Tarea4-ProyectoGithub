# Sistema Integral de Gestión – Software FJ

## Descripción
Sistema orientado a objetos para gestionar clientes, servicios y reservas
de la empresa Software FJ. Desarrollado para el curso Programación 213023
– UNAD, Fase 4.

## Autor
Juan Felipe Diaz Moreno

## Cómo ejecutar
1. Tener Python 3.10 o superior instalado
2. Clonar el repositorio:
   git clone https://github.com/NeinTag88/Tarea4-ProyectoGithub.git
3. Abrir la terminal dentro de la carpeta src/ y ejecutar:
   python sistema_software_fj.py
4. El log se genera automáticamente en: logs/sistema_fj_logs.txt

## Estructura del proyecto
- src/ → Código fuente principal
- logs/ → Registro de eventos y errores
- docs/ → Documentación adicional

## Conceptos implementados
- Clases abstractas: EntidadSistema y Servicio
- Herencia y polimorfismo: ReservaSala, AlquilerEquipo, AsesoriaEspecializada
- Encapsulación completa en la clase Cliente
- 6 excepciones personalizadas con códigos de error
- try/except, try/except/else, try/except/finally
- Encadenamiento de excepciones con raise...from
- Sistema de logs con el módulo logging
- 13 simulaciones completas (válidas e inválidas)