# Documentación de la Vista: `calcular_presupuesto_categorias`

## Descripción
La vista `calcular_presupuesto_categorias` permite a los usuarios autenticados gestionar y visualizar su presupuesto mensual en categorías de gastos. Calcula los gastos realizados en los últimos 30 días y muestra el ingreso total y disponible del usuario.

## Método HTTP
- **POST:** Para actualizar el presupuesto mensual de cada categoría.
- **GET:** Para mostrar la información actual del presupuesto y gastos.

## URL
```plaintext
/path/to/view/
```

## Requisitos
- El usuario debe estar autenticado (decorador `@login_required`).
- El modelo `Transaccion` debe estar definido y contener datos de gastos e ingresos.
- El modelo `Categoria` debe estar definido y asociado al usuario.

## Parámetros
- **request (HttpRequest):** 
  - Contiene la información sobre la solicitud HTTP.
  - Incluye datos enviados a través de un formulario para actualizar el presupuesto.

## Respuesta
- **Contexto enviado al template:**
    - `categorias_presupuesto`: 
      - Lista de diccionarios que contienen:
        - `categoria`: Instancia de la categoría.
        - `total_gastos`: Total de gastos en los últimos 30 días para la categoría (Decimal).
        - `presupuesto_restante`: Presupuesto mensual menos el total de gastos (Decimal).
    - `ingreso_total`: 
      - Suma total de ingresos del usuario en los últimos 30 días (Decimal).
    - `ingreso_disponible`: 
      - Ingreso total menos el total de gastos en los últimos 30 días (Decimal).

## Detalles de Implementación
1. **Cálculo de Fechas:**
   - Se establece una fecha límite de 30 días para calcular los gastos.

2. **Cálculo de Ingresos y Gastos:**
   - Se utilizan los métodos `total_ingresos` y `total_gastos` del modelo `Transaccion` para obtener los totales correspondientes.

3. **Actualización del Presupuesto:**
   - Si la solicitud es de tipo POST, se actualiza el presupuesto mensual de cada categoría según los datos enviados en el formulario.

4. **Preparación de Datos:**
   - Se agregan datos de gastos y presupuestos a la lista `categorias_presupuesto`.

## Ejemplo de Uso
Para acceder a esta vista, el usuario debe estar autenticado. En el formulario de la interfaz de usuario, el usuario puede ingresar un nuevo presupuesto mensual para cada categoría. Al enviar el formulario, la vista procesa los datos y redirige al usuario a la misma página con la información actualizada.

## Consideraciones
- Si no hay gastos registrados en una categoría en los últimos 30 días, el valor total de gastos se mostrará como 0.
- Asegúrate de que el modelo `Categoria` contenga un campo `tipo` solo se filtran las categorias de gastos no las de ingreso
- Manejo de excepciones y validaciones adicionales pueden ser necesarias para mejorar la robustez de la vista.

-