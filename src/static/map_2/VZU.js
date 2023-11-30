// Создание отдельного слоя для водозаборов
const VZULayer = new ol.layer.Vector({
    source: new ol.source.Vector(),
});

// Создание стиля для полигонов
const polygonStyle = new ol.style.Style({
    fill: new ol.style.Fill({
        color: 'rgba(0, 0, 128, 0.4)', // Цвет заливки
    }),
    stroke: new ol.style.Stroke({
        color: 'blue', // Цвет обводки
        width: 1, // Ширина обводки
    }),
});
// Функция для добавления полигона на карту
function addPolygonToLayer(item, layer) {
    const format = new ol.format.WKT();

    // Проверяем наличие геометрии и обрезаем первые 5 символов перед передачей в WKT
    if (item.geom && item.geom.length > 10) {
        const croppedGeom = item.geom.substring(10);
        const feature = format.readFeature(croppedGeom, {
            dataProjection: 'EPSG:4326',
            featureProjection: 'EPSG:3857',
        });

        // Добавление свойств в объект полигона
        feature.setProperties({
            intake_name: item.intake_name,
            pk: item.id,
        });
        feature.setStyle(polygonStyle);

        layer.getSource().addFeature(feature);
    }
}

// Асинхронный запрос к серверу для получения данных
fetch('/map/vzu')
    .then(response => response.json())
    .then(data => {
        // Добавление каждого полигона в слой
        data.forEach(item => {
            addPolygonToLayer(item, VZULayer);
        });
    })
    .catch(error => console.error('Error fetching data:', error));

export { VZULayer }