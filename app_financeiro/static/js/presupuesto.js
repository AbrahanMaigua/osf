// Función para validar el presupuesto en tiempo real y actualizar el DOM
function validarPresupuesto() {
    // Obtener el ingreso total disponible
    const ingresoTotal = parseFloat(document.getElementById('disponible').textContent) || 0;

    // Seleccionar todos los inputs de presupuesto
    const inputs = document.querySelectorAll('input[name^="presupuesto_"]');

    // Seleccionar el botón y el contenedor del mensaje de error
    const btn = document.getElementById('btn-1');
    const mensajeError = document.getElementById('mensaje_error');
    const mensajeErrorContainer = document.getElementById('mensaje_error_container');

    let totalPresupuestos = 0;
    let esValido = true;

    // Calcular el total de presupuestos y verificar cada input
    inputs.forEach(input => {
        const presupuesto = parseFloat(input.value) || 0;
        totalPresupuestos += presupuesto;

        // Si el presupuesto individual excede el ingreso, marcar el input como inválido
        if (presupuesto > ingresoTotal) {
            input.classList.add('is-danger');
            esValido = false;
        } else {
            input.classList.remove('is-danger');
        }
    });

    // Mostrar el mensaje de error si el total excede el ingreso disponible
    if (totalPresupuestos > ingresoTotal) {
        mensajeError.textContent = "El presupuesto total excede el ingreso total.";
        mensajeErrorContainer.classList.remove('is-hidden'); // Mostrar el contenedor del mensaje de error
        esValido = false;
    } else {
        mensajeError.textContent = ""; // Limpiar el mensaje de error
        mensajeErrorContainer.classList.add('is-hidden'); // Ocultar el contenedor del mensaje de error cuando es válido
    }

    // Actualizar el estado del botón de guardar
    btn.disabled = !esValido;

    return esValido;
}

// Agregar listeners a los inputs de presupuesto para actualizar el DOM en tiempo real
document.addEventListener("DOMContentLoaded", function() {
    const inputs = document.querySelectorAll('input[name^="presupuesto_"]');
    inputs.forEach(input => {
        input.addEventListener('input', validarPresupuesto);
    });
});
