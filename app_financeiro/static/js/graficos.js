document.addEventListener('DOMContentLoaded', () => { 
    const url = 'api/transacciones/'; // Cambia esta URL según tu configuración

    const getTransacciones = async () => {
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}` // Ajusta según tu método de autenticación
                }
            });

            if (!response.ok) {
                throw new Error('Error en la red');
            }

            const transacciones = await response.json();
            generarGraficos(transacciones.transacciones);
        } catch (error) {
            console.error('Error al obtener transacciones:', error);
        }
    };

    const generarGraficos = (transacciones) => {
        const categoriasActualMes = {};
        const gastosMensuales = new Array(6).fill(0); // Para los últimos 6 meses
        const meses = generarUltimosMeses(6); // Genera etiquetas para los últimos 6 meses
        const mesActual = new Date().getMonth();
        const anioActual = new Date().getFullYear();

        // Procesar transacciones para categorías del mes actual y gastos mensuales
        transacciones.forEach(transaccion => {
            const fecha = new Date(transaccion.fecha);
            const mes = fecha.getMonth();
            const anio = fecha.getFullYear();
            const cantidad = parseFloat(transaccion.cantidad);

            if (transaccion.tipo === 'gasto') {
                // Sumar a la categoría correspondiente para el mes actual
                if (mes === mesActual && anio === anioActual) {
                    const categoriaNombre = transaccion.categoria_nombre || 'Sin Categoría';
                    categoriasActualMes[categoriaNombre] = (categoriasActualMes[categoriaNombre] || 0) + cantidad;
                }

                // Agregar al gasto mensual si corresponde a los últimos 6 meses
                const mesesDesdeActual = mesActual - mes + (anioActual - anio) * 12;
                if (mesesDesdeActual >= 0 && mesesDesdeActual < 6) {
                    gastosMensuales[5 - mesesDesdeActual] += cantidad;
                }
            }
        });

        // Preparar datos para el gráfico de categorías del mes actual
        const labels = Object.keys(categoriasActualMes);
        const data = Object.values(categoriasActualMes);

        // Verificar si hay gastos para el mes actual
        const hayGastos = data.length > 0 && data.reduce((total, value) => total + value, 0) > 0;

        const gastosData = {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    "rgba(255, 99, 132, 0.7)",
                    "rgba(54, 162, 235, 0.7)",
                    "rgba(255, 206, 86, 0.7)",
                    "rgba(75, 192, 192, 0.7)"
                ],
                hoverOffset: 4
            }]
        };

        // Plugin para mostrar texto en el centro cuando no hay datos
        const centerTextPlugin = {
            id: 'centerText',
            afterDraw: (chart) => {
                if (!hayGastos) {
                    const ctx = chart.ctx;
                    const width = chart.width;
                    const height = chart.height;

                    ctx.restore();
                    ctx.font = '20px Arial';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillStyle = 'gray';
                    ctx.fillText('No hay gastos para este mes', width / 2, height / 2);
                    ctx.save();
                }
            }
        };

        // Configurar y crear el gráfico de categorías del mes actual
        const gastosConfig = {
            type: 'doughnut',
            data: gastosData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Gastos del Mes Actual por Categoría'
                    }
                }
            },
            plugins: [centerTextPlugin]
        };
        new Chart(document.getElementById('gastosChart'), gastosConfig);

        // Preparar datos para el gráfico de gastos mensuales de los últimos 6 meses
        const gastosMensualesData = {
            labels: meses,
            datasets: [{
                label: "Gastos",
                data: gastosMensuales,
                backgroundColor: 'rgba(0, 209, 178, 0.7)',
                borderColor: 'rgba(0, 209, 178, 1)',
                borderWidth: 1
            }]
        };

        // Configurar y crear el gráfico de gastos mensuales
        const config = {
            type: 'bar',
            data: gastosMensualesData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Cantidad'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Mes'
                        }
                    }
                }
            }
        };
        new Chart(document.getElementById('gastosMensualesChart'), config);
    };

    // Función para generar los últimos n meses en formato de nombre de mes
    const generarUltimosMeses = (n) => {
        const nombresMeses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
        const mesActual = new Date().getMonth();
        return Array.from({ length: n }, (_, i) => nombresMeses[(mesActual - i + 12) % 12]).reverse();
    };

    getTransacciones(); // Llamar a la función al cargar la página
});
