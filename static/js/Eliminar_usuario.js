// Este script se encarga de mostrar una alerta de confirmación al usuario antes de eliminar su cuenta

// Espera a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", function () {

    // Capturar el clic en los enlaces
    let eliminarUsuarioLinks = document.querySelectorAll(".eliminar-usuario");
    eliminarUsuarioLinks.forEach(function(link) {

        // Agregar un evento de clic a cada enlace
        link.addEventListener("click", function (event) {
            // Prevenir el comportamiento predeterminado del enlace (es decir, la navegación)
            event.preventDefault();

            // Obtener la URL de la vista del atributo de datos en el html
            let eliminarUsuarioUrl = this.getAttribute("data-url");

            // Mostrar la alerta
            Swal.fire({
                title: "¿Estás seguro?",
                text: "No podrás revertir los cambios",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
                confirmButtonText: "Eliminar"
            }).then((result) => {

                if (result.isConfirmed) {
                    // Si se confirma la eliminación, redirige al usuario a la URL de eliminación
                    window.location.href = eliminarUsuarioUrl;
                    console.log("Usuario eliminado");
                }
            });
        });
    });
});