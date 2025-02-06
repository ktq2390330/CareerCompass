document.addEventListener("DOMContentLoaded", function () {
    const progressBar = document.getElementById("progress-bar");
    const progressText = document.getElementById("progress-text");
    const statusText = document.getElementById("status-text");
    const spinner = document.getElementById("spinner");

    fetch("{% url 'CCapp:self_analy_processing' %}", {
        method: "POST",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        body: new FormData(document.getElementById("assessment-form")),
    })
    .then(response => response.json())
    .then(data => {
        const processingTime = data.processing_time * 1000; // 秒 → ミリ秒
        const updateInterval = processingTime / 10; // 進捗バーを10回更新

        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            progressBar.style.width = progress + "%";
            progressText.innerText = `現在の進捗：${progress}%`;

            if (progress >= 100) {
                clearInterval(interval);
                spinner.style.display = "none";
                statusText.innerText = "判定が完了しました！";

                // 1秒後にリダイレクト
                setTimeout(() => {
                    window.location.href = "{% url 'CCapp:self_analy' %}";
                }, 1000);
            }
        }, updateInterval);
    })
    .catch(error => console.error("Error:", error));
});

// CSRFトークンを取得する関数
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
