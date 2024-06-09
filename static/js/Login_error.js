// El script se encarga de mostrar una alerta
// de confirmación antes de enviar un formulario.
window.onload = function () {
    // Capturar el error
    let error = document.getElementById('error-message').innerText;

    // Si hay un error, muestra una alerta
    if (error) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: error,
        })
    }
}