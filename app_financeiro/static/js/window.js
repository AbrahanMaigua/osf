// Obtener elementos
var loginModal = document.getElementById("loginModal");
var signupModal = document.getElementById("signupModal");

var loginBtn = document.getElementById("loginBtn");
var signupBtn = document.getElementById("signupBtn");

var closeButtons = document.getElementsByClassName("close");

// Mostrar el modal de Iniciar Sesión
loginBtn.onclick = function() {
    loginModal.style.display = "block";
}

// Mostrar el modal de Crear Cuenta
signupBtn.onclick = function() {
    signupModal.style.display = "block";
}

// Cerrar los modales cuando se hace clic en la 'X'
for (let i = 0; i < closeButtons.length; i++) {
    closeButtons[i].onclick = function() {
        let modalId = this.getAttribute('data-modal');
        document.getElementById(modalId).style.display = "none";
    }
}

// Cerrar el modal si se hace clic fuera de él
window.onclick = function(event) {
    if (event.target == loginModal) {
        loginModal.style.display = "none";
    }
    if (event.target == signupModal) {
        signupModal.style.display = "none";
    }
}