## Documentación de Modelos

### Modelo: `Categoria`

El modelo **`Categoria`** define las categorías utilizadas para clasificar tanto los gastos como los ingresos de los usuarios. Es importante para organizar las transacciones bajo distintas etiquetas, lo que ayuda a los usuarios a realizar un seguimiento más detallado de sus finanzas.

- **Campos**:
  - `nombre`: (CharField) El nombre de la categoría. Ejemplos: "Alimentación", "Transporte", "Salario".
  - `descripcion`: (TextField, opcional) Un campo opcional para proporcionar una descripción adicional de la categoría.

- **Métodos**:
  - `__str__()`: Devuelve el nombre de la categoría como su representación en formato de cadena, útil para la interfaz de administración y otros lugares donde se necesite visualizar la categoría.

- **Uso**: 
  Este modelo permite agrupar las transacciones según categorías, lo que es útil para análisis y reportes financieros, así como para organizar los gastos e ingresos de manera clara.

**Ejemplo**:

```python
categoria = Categoria(nombre="Alimentación", descripcion="Gastos en alimentos y bebidas")
categoria.save()
```

---

### Modelo: `Transaccion`

El modelo **`Transaccion`** es el principal modelo de la aplicación. Almacena todas las transacciones financieras (gastos e ingresos) de los usuarios y unifica los registros para que se gestionen de manera similar a los movimientos de una cuenta bancaria.

- **Campos**:
  - `usuario`: (ForeignKey) Relación con el modelo `User`, lo que permite registrar a qué usuario pertenece cada transacción.
  - `categoria`: (ForeignKey) Relación con el modelo `Categoria`, que indica a qué categoría pertenece la transacción.
  - `subcategoria`: (ForeignKey) (opcional) Relación con el modelo `Subcategoria`, que indica a qué subcategoría pertenece la transacción.
  - `cantidad`: (DecimalField) La cantidad de dinero involucrada en la transacción. La precisión está configurada con hasta 10 dígitos y 2 decimales.
  - `fecha`: (DateTimeField) La fecha y hora en la que se registró la transacción. El valor se genera automáticamente en el momento en que se crea el registro.
  - `tipo`: (CharField) Define si la transacción es un **gasto** o un **ingreso**. Las opciones son `'gasto'` o `'ingreso'`.
  - `descripcion`: (TextField, opcional) Un campo opcional para describir detalles adicionales sobre la transacción (por ejemplo, "Pago de factura de electricidad").

- **Métodos**:
  - `__str__()`: Devuelve una representación en formato de cadena de la transacción, mostrando su tipo (gasto o ingreso), la cantidad, la categoría y la fecha. Esto es útil en la interfaz de administración y para depuración.
  
  - **Método `calcular_balance`**: Este es un método estático que calcula el balance total de un usuario. Para hacerlo, suma todos los ingresos del usuario y resta todos los gastos. Se puede usar este método en cualquier vista o template para mostrar el balance actual del usuario.
    - Parámetros: `usuario` (el usuario para el que se quiere calcular el balance).
    - Retorno: La diferencia entre los ingresos y los gastos del usuario.

- **Meta**:
  - **`ordering`**: Establece que las transacciones se ordenen por fecha, de manera descendente. Esto garantiza que las transacciones más recientes aparezcan primero, similar a como funcionan los extractos bancarios.

**Ejemplo**:

```python
# Crear una transacción de ingreso
transaccion_ingreso = Transaccion(usuario=user, categoria=categoria, cantidad=1000, tipo='ingreso')
transaccion_ingreso.save()

# Crear una transacción de gasto
transaccion_gasto = Transaccion(usuario=user, categoria=categoria, cantidad=200, tipo='gasto')
transaccion_gasto.save()
```

---

### Método Estático: `calcular_balance`

El método **`calcular_balance`** es una función estática dentro del modelo `Transaccion`. Su propósito es calcular el balance total de un usuario, sumando los ingresos y restando los gastos.

- **Parámetros**:
  - `usuario`: El usuario para el cual se está calculando el balance.
  
- **Lógica**:
  1. Filtra todas las transacciones del tipo `'ingreso'` para el usuario y suma las cantidades.
  2. Filtra todas las transacciones del tipo `'gasto'` para el usuario y suma las cantidades.
  3. Devuelve la diferencia entre ingresos y gastos, lo que representa el balance actual del usuario.

- **Retorno**: 
  Un valor decimal que representa el balance total del usuario.

**Ejemplo de uso**:

```python
balance_usuario = Transaccion.calcular_balance(user)
print(f"El balance actual del usuario es: {balance_usuario}")
```

---

### Relaciones entre Modelos

- **Transaccion - Usuario**: Cada transacción está asociada con un usuario, lo que permite registrar qué usuario realizó cada gasto o ingreso.
- **Transaccion - Categoria**: Cada transacción pertenece a una categoría, lo que permite clasificar y organizar los gastos e ingresos en distintos grupos.

---

## Documentación de Vistas

### Vista: `historial`

Esta vista muestra el historial de todas las transacciones realizadas por el usuario actual. Incluye tanto ingresos como gastos, y permite ver el balance total del usuario usando el método `calcular_balance`.

- **Lógica**:
  - Filtra todas las transacciones del usuario.
  - Calcula el balance usando el método `calcular_balance`.
  - Renderiza la plantilla `'history.html'` con las transacciones y el balance.

```python
def historial(request):
    transacciones = Transaccion.objects.filter(usuario=request.user)
    balance = Transaccion.calcular_balance(request.user)
    return render(request, 'history.html', {'transacciones': transacciones, 'balance': balance})
```

---

### Vista: `gastos`

Esta vista filtra y muestra solo las transacciones del tipo `'gasto'` para el usuario actual. Es útil para que los usuarios revisen exclusivamente los gastos que han realizado.

- **Lógica**:
  - Filtra las transacciones del tipo `'gasto'` para el usuario.
  - Renderiza la plantilla `'gastos.html'` con las transacciones filtradas.

```python
def gastos(request):
    gastos = Transaccion.objects.filter(usuario=request.user, tipo='gasto')
    return render(request, 'gastos.html', {'gastos': gastos})
```

---

### Vista: `metas`

Esta vista está diseñada para mostrar las metas financieras del usuario. 

```python
def metas(request):
    # Aquí puedes integrar lógica para metas financieras si está separada.
    return render(request, 'metas.html')
```

---

## Conclusión

Este código está diseñado para simular una aplicación financiera similar a un banco, donde los usuarios pueden registrar y ver tanto sus ingresos como sus gastos, categorizarlos y calcular su balance total. El modelo unificado de transacciones simplifica la estructura de datos y mejora la eficiencia del sistema. Además, proporciona una base sólida para extender la aplicación con funcionalidades como reportes financieros, visualizaciones y metas financieras.

### Modelo: `MetaFinanciera`
El modelo **`MetaFinanciera`** permite a los usuarios establecer metas financieras que quieran alcanzar, como ahorrar una cierta cantidad para un proyecto o pagar una deuda.

- **Campos**:
  - `usuario`: (ForeignKey) Relación con el usuario que ha establecido la meta.
  - `nombre`: (CharField) El nombre de la meta. Ejemplo: "Ahorro para vacaciones".
  - `cantidad_objetivo`: (DecimalField) La cantidad que el usuario desea alcanzar.
  - `cantidad_acumulada`: (DecimalField, por defecto `0`) La cantidad que el usuario ha logrado acumular hasta el momento.
  - `fecha_meta`: (DateField) La fecha límite para alcanzar la meta.

- **Uso**:
  Este modelo permite que los usuarios creen y realicen un seguimiento de sus metas financieras, ayudándoles a controlar su progreso.

---



## Relaciones entre Modelos

1. **Transaccion - Usuario**: Un usuario puede tener múltiples Transaccion asociados a él/ella. Los gastos o ingreso pueden estar categorizados.

2. **MetaFinanciera - Usuario**: Cada usuario puede tener varias metas financieras que quiera alcanzar. Estas metas son independientes entre sí.

3. **Categoria - Transaccion**: Cada Transaccion tiene una cartegoria asociada para relizar saber en que fue gastao o ingresado dicha Transaccion
## Consideraciones Adicionales

- **Relaciones con el Usuario**: Todos los modelos principales (Gasto, MetaFinanciera) están relacionados con el modelo `User`, lo que permite que cada usuario tenga su propio conjunto de datos.
- **Manejo de Categorías**: El modelo `Categoria` es un componente clave en la clasificación tanto de los gastos como de las transacciones en general. Esto facilita el análisis financiero.

## Ejemplo de Consulta

### Obtener gastos por categoría

```python
from .models import Gasto

# Obtener todos los gastos de una categoría específica
categoria = Categoria.objects.get(nombre="Alimentación")
gastos = Gasto.objects.filter(categoria=categoria)
```

### Obtener metas del usuario

```python
from .models import MetaFinanciera

# Obtener todas las metas de un usuario
metas = MetaFinanciera.objects.filter(usuario=request.user)
```

### Obtener historial de transacciones

```python
from .models import HistorialTransaccion


```

---

Con esta documentación, tienes una guía clara para comprender el propósito de cada modelo, sus campos, y cómo interactúan entre sí. ¡Listo para usar en tu aplicación de finanzas!