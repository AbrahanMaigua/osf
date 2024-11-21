// Función para calcular el fondo de emergencia en tiempo real
function calcularFondo() {
  const costoVida = parseFloat(document.getElementById("costoVida").value) || 0;
  const mesesRespaldo = parseInt(document.getElementById("mesesRespaldo").value);

  const fondoDeEmergencia = costoVida * mesesRespaldo;
  document.getElementById("fondoResultado").textContent = fondoDeEmergencia.toFixed(2);

  // Muestra el resultado solo si el costo de vida es mayor a 0
  if (costoVida > 0) {
    document.getElementById("resultado").classList.remove("is-hidden");
  } else {
    document.getElementById("resultado").classList.add("is-hidden");
  }
}

// Agregar eventos de cambio en tiempo real
document.getElementById("costoVida").addEventListener("input", calcularFondo);
document.getElementById("mesesRespaldo").addEventListener("change", calcularFondo);