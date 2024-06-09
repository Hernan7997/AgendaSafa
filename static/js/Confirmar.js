// Espera a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", function () {

    // Capturar el clic en los enlaces de confirmacion
    let enviar = document.querySelectorAll(".confirmar");

    // Agregar un evento de clic a cada enlace
    enviar.forEach(function (boton) {
        boton.addEventListener("click", function (event) {

            // Prevenir el comportamiento predeterminado del enlace (parar la navegacion)
            event.preventDefault();

            // Mostrar la alerta
            Swal.fire({
                title: "Quieres guardar los cambios?",
                showDenyButton: true,
                showCancelButton: true,
                icon: "question",
                confirmButtonText: "Guardar",
                denyButtonText: "No guardar"
            }).then((result) => {
                /* Read more about isConfirmed, isDenied below */
                if (result.isConfirmed) {
                    Swal.fire("Guardado!", "", "success");
                    //Si se confirma, envia el formulario
                    event.target.form.submit();
                } else if (result.isDenied) {
                    Swal.fire("Cambios no guardados", "", "error");
                    //Si se niega, redirige al usuario a la pagina anterior
                    window.location.href = document.referrer;
                }
            });
        });
    });
});