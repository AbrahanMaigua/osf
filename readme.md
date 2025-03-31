**Descripción de la Web App de Finanzas**

Nuestra aplicación de finanzas está diseñada para facilitar la gestión de tus ingresos, gastos y metas financieras a través de una plataforma sencilla y eficiente. puedes acceder a todas las funciones desde cualquier dispositivo conectado, lo que te permite controlar tus finanzas en todo momento. 

**Funcionalidades Principales**:

1. **Menú**: Navega de manera intuitiva entre las diferentes secciones de la app para acceder a toda la información financiera que necesitas.

2. **Perfil**: Personaliza tu experiencia, ajusta tus preferencias y mantén un registro de tu actividad financiera.

3. **Categorías**: Organiza tus gastos e ingresos en diferentes categorías para tener un control más detallado de tus finanzas.

4. **Gastos**: Registra y clasifica tus gastos de manera rápida, permitiéndote realizar un seguimiento de cada movimiento financiero.

5. **Metas**: Establece objetivos financieros y sigue tu progreso hacia ellos, asegurando que cumplas tus metas de ahorro y gasto.

6. **Cover (Resumen)**: Visualiza un resumen de tu situación financiera actual, con una vista general de tus gastos, metas y balances.

7. **Gastos Totales**: Accede a un informe detallado de tus gastos acumulados, para saber exactamente en qué has invertido tu dinero.

8. **Dinero Disponible**: Consulta el saldo disponible de manera clara y precisa, lo que te permitirá tomar decisiones financieras informadas.

9. **Data (Análisis de Datos)**: Obtén análisis y gráficos de tus movimientos financieros para una visión más profunda de tus hábitos de gasto.

10. **Card / Historial**: Revisa un historial completo de transacciones, donde podrás ver tarjetas con los detalles de cada gasto o ingreso registrado.

    - **Títulos**: Clasificación de la transacción.
    - **Categoría**: Identificación del tipo de gasto o ingreso.
    - **Fecha**: Registro del día en que se realizó la transacción.
    - **Cantidad Gastada/Adicionada**: Detalle de las cantidades manejadas en cada operación.

---

Este enfoque integral te permite gestionar tus finanzas personales de manera efectiva, manteniendo todo en un solo lugar y accesible en cualquier momento.


### run local

1. create virtual enviroment

    ```"python -m venv env" ```
    ```env\Scripts\activate.bat```


2. isntall dependecias

    ```pip install -r requierement.txt ```

3. run app
    ```
    cd app_finaciera 
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver