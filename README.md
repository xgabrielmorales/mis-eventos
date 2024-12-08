# Mis Eventos

![Python version](https://img.shields.io/badge/Python-3.12-blue?style=flat-square)
[![Continuous integration](https://img.shields.io/github/actions/workflow/status/xgabrielmorales/mis-eventos/ci.yml?branch=main&style=flat-square)](https://github.com/xgabrielmorales/mis-eventos/actions?query=branch:main)
[![Coverage Status](https://img.shields.io/coverallsCoverage/github/xgabrielmorales/mis-eventos?branch=main&style=flat-square)](https://coveralls.io/github/xgabrielmorales/mis-eventos)

## Configuración Inicial

1. Clona este repositorio:
    ```sh
    $ git clone https://github.com/xgabrielmorales/mis-eventos.git
    ```
2. Desencripta las variables de entorno:
    ```sh
    $ openssl enc -d -aes-256-cbc -pbkdf2 -in environment/.env.dev.enc -out environment/.env.dev -pass file:environment/.secret_key
    ```
    Necesitarás la llave de cifrado en la ruta `environment/.secret_key`.
3. Construye la imagen de Docker:
    ```sh
    $ docker compose -f docker-compose.dev.yml build
    ```
4. Levanta los servicios:
    ```sh
    $ docker compose -f docker-compose.dev.yml up -d
    ```

## Guía de Desarrollo

En el directorio `scripts` hay una colección de scripts que te pueden ser de utilidad:

1. Linters:
    ```sh
    $ ./scripts/lint.sh
    ```
2. Tests:
    ```sh
    $ ./scripts/tests.sh
    ```

## Documentación del API

Puedes acceder a la documentación del API a través de la colección de Postman incluida en el repositorio o a través de la URL: `http://localhost:8000/graphql`.

## Aproximación
### Diagrama Entidad Relación
<div style="text-align: center;">
    <img src="./extra/mis-eventos-UML.svg" alt="Diagrama Entidad Relación" title="Diagrama Entidad Relación" style="width: 50%;">
</div>

1. **User - Event**
   - Un **Usuario** con el rol de "Organizador" puede gestionar múltiples **Eventos**.
   - Un **Evento** es gestionado por un único **Usuario** (Organizador).

2. **User - Registration**
   - Un **Usuario** con el rol de "Asistente" puede tener múltiples **Inscripciones**.
   - Una **Inscripción** pertenece a un único **Usuario** (Asistente).

3. **Event - Registration**
   - Un **Evento** puede tener múltiples **Inscripciones**.
   - Una **Inscripción** está asociada a un único **Evento**.

4. **Event - Schedule**
   - Un **Evento** puede tener múltiples **Horarios**.
   - Un **Horario** está asociado a un único **Evento**.

5. **Event - Resource**
   - Un **Evento** puede requerir múltiples **Recursos**.
   - Un **Recurso** está asociado a un único **Evento**.

6. **Registration - Attendance**
   - Una **Inscripción** puede tener un único registro de **Asistencia**.
   - Una **Asistencia** está asociada a una única **Inscripción**.

## Completitud
### Requerimientos Técnicos Obligatorios
- [x] Python 3.12
- [x] Docker & Docker Compose
- [x] Poetry
- [x] FastAPI
- [x] GraphQL (Strawberry)
- [x] SqlModel
- [x] Postgres
- [ ] Elastic
- [ ] Redis (Opcional)
- [x] Tests Unitarios (con reporte de cobertura)
- [x] Documentación de API
- [x] Migraciones (Alembic)
