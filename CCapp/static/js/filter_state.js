document.addEventListener('DOMContentLoaded', () => {
    const pageKey = document.body.dataset.pageKey;

    // エラーハンドリングを追加
    if (!pageKey) {
        console.error("Error: data-page-key is not set on the <body> element.");
        return;
    }

    console.log("Page key:", pageKey);

    // 保存
    function saveCheckboxState() {
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        const state = {};
    
        checkboxes.forEach(checkbox => {
            state[checkbox.value] = checkbox.checked;
            console.log(`Saving - Value: ${checkbox.value}, Checked: ${checkbox.checked}`);
        });
    
        sessionStorage.setItem(pageKey, JSON.stringify(state));
        console.log("Saved State:", state);
    }
    

    // 復元
    function restoreCheckboxState() {
        console.log("Restoring checkbox state...");
        const state = JSON.parse(sessionStorage.getItem(pageKey)) || {};
    
        console.log("State loaded:", state);
        const checkboxes = document.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            if (state.hasOwnProperty(checkbox.value)) {
                checkbox.checked = state[checkbox.value];
                console.log(`Restored ${checkbox.value}: ${checkbox.checked}`);
            }
        });
    }
    

    // イベントリスナー
    document.addEventListener('change', event => {
        if (event.target.type === 'checkbox') {
            console.log(`Checkbox Changed - Value: ${event.target.value}, Checked: ${event.target.checked}`);
            saveCheckboxState();
        }
    });
    

    document.addEventListener('DOMContentLoaded', restoreCheckboxState);

});