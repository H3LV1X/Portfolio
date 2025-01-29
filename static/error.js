document.addEventListener("DOMContentLoaded", function () {
    const flashDataElement = document.getElementById("flash-data");
    const modal = document.getElementById("error-modal");
    const closeModalButton = document.querySelector(".close-btn");
    const modalMessage = document.getElementById("modal-message");

    // Получение flash-сообщений
    if (flashDataElement) {
        const flashData = flashDataElement.getAttribute("data-flash");
        try {
            const messages = JSON.parse(flashData);
            if (messages && messages.length > 0) {
                messages.forEach(([category, message]) => {
                    if (category === "danger") {
                        modalMessage.textContent = message;
                        modal.style.display = "block";
                    }
                });
            }
        } catch (error) {
            console.error("Ошибка при обработке flash-сообщений:", error, "Flash Data:", flashData);
        }
    }

    // Закрытие модального окна
    if (closeModalButton) {
        closeModalButton.addEventListener("click", function () {
            modal.style.display = "none";
        });
    }

    // Закрытие при клике вне модального окна
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});
