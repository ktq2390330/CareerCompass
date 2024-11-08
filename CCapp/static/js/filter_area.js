function showArea(areaId) {
    // すべてのエリア詳細を非表示にする
    const areaDetails = document.querySelectorAll('.area-details');
    areaDetails.forEach(detail => {
        detail.style.display = 'none';
    });

    // 選択されたエリア詳細を表示する
    const selectedArea = document.getElementById(areaId);
    if (selectedArea) {
        selectedArea.style.display = 'block';
    }
}


function selectAll(areaId, select) {
    // 指定したエリアのチェックボックスを取得
    const checkboxes = document.getElementById(areaId).querySelectorAll('input[type="checkbox"]');
    
    // すべてのチェックボックスを選択または解除
    checkboxes.forEach(checkbox => checkbox.checked = select);
}

