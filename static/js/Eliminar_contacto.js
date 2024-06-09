// Espera a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", function () {

    // Capturar el clic en los enlaces de eliminación de contacto
    let eliminarContactoLinks = document.querySelectorAll(".eliminar-contacto");
    eliminarContactoLinks.forEach(function(link) {

        // Agregar un evento de clic a cada enlace
        link.addEventListener("click", function (event) {

            // Prevenir el comportamiento predeterminado del enlace (es decir, la navegación)
            event.preventDefault();

            // Obtener la URL de la vista del atributo de datos en el html
            let eliminarContactoUrl = this.getAttribute("data-url");

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
                    window.location.href = eliminarContactoUrl;
                }
            });
        });
    });
});