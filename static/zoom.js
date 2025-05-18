// OrgChart を描画したあと（drawChartWithData() の最後など）に呼び出す
const chartDiv = document.getElementById('chart_div');

// Panzoom インスタンスを作成
const panzoom = Panzoom(chartDiv, {
    maxScale: 10,    // 最大ズーム倍率
    minScale: 0.01,  // 最小ズーム倍率
    zoomSpeed: 0.02, // ← 感度を低くする（デフォルトは 0.065）
    contain: 'outside' // 内容がはみ出さないよう内部に制限
});

// ホイール／トラックパッドズームを有効化
chartDiv.parentElement.addEventListener('wheel', panzoom.zoomWithWheel);

// タッチやマウスドラッグでパンを有効化
chartDiv.parentElement.addEventListener('pointerdown', panzoom.handlePointerDown, { passive: false });