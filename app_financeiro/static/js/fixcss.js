document.addEventListener("DOMContentLoaded", function() {
    let a = document.getElementsByClassName('subcategoria-title');
    let b = document.getElementsByClassName('end-text');

    for (let i = 0; i < a.length; i++) {
        let nun = a[i].textContent.length;
        let discount = nun * 20;  // Ajusta este valor según el descuento que quieras aplicar
        b[i].style.marginLeft = `${discount}px`;
    }
});
