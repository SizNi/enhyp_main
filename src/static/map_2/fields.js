// Создание отдельного слоя для полигонов
const fieldsLayer = new ol.layer.Vector({
    source: new ol.source.Vector(),
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
            field_name: item.field_name,
            pk: item.id
            // Другие свойства, если необходимо
        });

        layer.getSource().addFeature(feature);
    }
}

// Асинхронный запрос к серверу для получения данных
fetch('/map/fields')
    .then(response => response.json())
    .then(data => {
        // Добавление каждого полигона в слой
        data.forEach(item => {
            addPolygonToLayer(item, fieldsLayer);
        });
    })
    .catch(error => console.error('Error fetching data:', error));

export { fieldsLayer }