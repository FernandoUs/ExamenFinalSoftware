# ExamenFinalSoftware
# Pregunta 3 - Mejoras al Sistema de Mensajería

## Pregunta
Se requiere realizar un cambio en el software para adicionar una validación del máximo número de contactos y la eliminación de contactos y de usuarios (considerar que los mensajes ya enviados a contactos que serán eliminados deben mantenerse).

### Subpreguntas
- Qué cambiaría en el código (Clases / Métodos) - No implementación
- Nuevos casos de prueba a adicionar
- ¿Cuánto riesgo hay de "romper" lo que ya funciona?

## Respuesta

### Cambios en Clases y Métodos
**Clase Usuario:**
- Se podría agregar un nuevo atributo (max_contac): En caso la cantidad máxima de contactos dependa de cada usuario
- Dentro del método de agregar contactos se tendría que hacer modificaciones para que valide el límite de contactos antes de verificar si los datos que se envían son correctos
- Por otro lado, para eliminar contacto y usuario se agregarían 2 nuevos métodos: 
  - `eliminacion_contacto(alias_contacto)`: Para eliminar un contacto específico
  - `eliminar_usuario()`: Para eliminar completamente un usuario del sistema

### Lógica Adicional
Además, dentro de los controladores del servicio de mensajería, se añadiría un sistema de guardar mensajes pasados, ya habiendo eliminado el usuario, no sería óptimo guardar todos los mensajes de la lista, además que una vez eliminado el contacto, se vería la lógica de si aparece el nombre del alias que se tenía o se elimina completamente todo lo que se tiene del contacto

### Nuevos Casos de Prueba
Al agregar nuevos métodos, también se tendría que añadir nuevos casos de prueba, como:
- Agregar un nuevo contacto cuando el límite ya se ha alcanzado
- Agregar un nuevo contacto cuando aún no se alcanza el límite
- Eliminar un contacto existente con éxito
- Intentar eliminar un contacto que no existe (caso de fracaso)
- Verificar la visualización de mensajes
- Para el usuario: 
  - Eliminar el usuario completamente
  - Verificar que el usuario no exista en la base de datos
  - Verificar que los mensajes anteriores se conserven

### Evaluación de Riesgo
En este caso, no hay tanto riesgo, ya que se añade y modifica los métodos ya implementados y no rompe la lógica de lo que está hecho, solo se añadiría lógica como se explicó anteriormente. 

Lo único que se tendría que tener cuidado es la conservación de datos, tanto usuarios, contactos y hasta mensajes. De manera general, dependiendo a qué tan grande sean los cambios que se quiere hacer al software ya desarrollado y si se modifica en gran medida los datos, lógica y dependencia entre métodos, se evaluaría el riesgo.