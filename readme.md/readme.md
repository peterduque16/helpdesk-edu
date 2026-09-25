# HelpDesk EDU - Parcial 2

Este repositorio contiene la solución de los ejercicios 1, 2 y 3 del cuadernillo HelpDesk EDU.

---

## 📌 Ejercicio 1: Entidades y validaciones
- Clase `Ticket` con atributos:
  - `id`, `requester_id` obligatorios
  - `assigned_id` opcional
- Manejo de etiquetas (`tags`):
  - Normalización a minúsculas
  - Rechazo de espacios vacíos
  - Evitar duplicados
  - Propiedad de solo lectura
- **Pruebas:** `tests/test_ticket.py` valida normalización, rechazo de espacios, independencia de instancias y protección contra reasignación.

---

## 📌 Ejercicio 2: TicketService y repositorios falsos
- Clase `TicketService` con métodos:
  - `require(ticket_id)` para obtener tickets
  - `watchers(ticket_id)` para listar solicitante y técnico asignado
- Repositorios falsos (`FakeTicketsRepo`, `FakeUsersRepo`) para pruebas.
- **Pruebas:** `tests/test_ticket_service.py` valida que los watchers se obtienen correctamente.

---

## 📌 Ejercicio 3: Excepciones y polimorfismo
- Excepción `DuplicateAssignmentError` como subclase de `DomainError`.
- En `assign()` se rechaza asignar el mismo técnico que ya tiene el ticket.
- Implementación `WebhookNotifier` como polimorfismo de `Notifier`, almacenando payloads en memoria.
- **Pruebas:** 
  - Al reasignar al mismo técnico se lanza la excepción.
  - Al asignar correctamente se guarda el payload en `sent_payloads`.

---

## ✅ Estado de pruebas
Todas las pruebas pasan correctamente:
