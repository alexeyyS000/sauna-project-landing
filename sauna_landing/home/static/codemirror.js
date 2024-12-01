document.addEventListener("DOMContentLoaded", function () {
    const textareas = document.querySelectorAll(".codemirror-textarea");
    textareas.forEach((textarea) => {
        CodeMirror.fromTextArea(textarea, {
            mode: "htmlmixed",
            lineNumbers: true,
            lineWrapping: true,
            theme: "default", // Или любой другой доступный стиль
        });
    });
});
