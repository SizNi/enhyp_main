import { map } from "./main.js";

// Добавление контролов Zoom
const zoomInButton = document.createElement("button");
zoomInButton.innerHTML = "+";
zoomInButton.addEventListener("click", function () {
    const view = map.getView();
    const currentZoom = view.getZoom();
    view.setZoom(currentZoom + 1);
});

const zoomOutButton = document.createElement("button");
zoomOutButton.innerHTML = "-";
zoomOutButton.addEventListener("click", function () {
    const view = map.getView();
    const currentZoom = view.getZoom();
    view.setZoom(currentZoom - 1);
});

const zoomButtonsContainer = document.createElement("div");
zoomButtonsContainer.id = "zoom-buttons-container";
zoomButtonsContainer.className = "ol-control ol-unselectable";
zoomButtonsContainer.appendChild(zoomInButton);
zoomButtonsContainer.appendChild(zoomOutButton);

// добавление выделения прямоугольником
const selectLayer = new ol.layer.Vector({
    source: new ol.source.Vector(),
    style: new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'rgba(0, 0, 255, 1.0)',
            width: 2,
        }),
        fill: new ol.style.Fill({
            color: 'rgba(0, 0, 255, 0.1)',
        }),
    }),
});

const dragBox = new ol.interaction.DragBox({
    condition: ol.events.condition.platformModifierKeyOnly,
});

dragBox.on('boxend', function () {
    // Получите границы прямоугольника выделения
    const extent = dragBox.getGeometry().getExtent();

    // Очистите предыдущие выделенные объекты
    selectLayer.getSource().clear();

    // Переберите все объекты на карте и проверьте, пересекается ли объект с прямоугольником выделения
    map.getLayers().forEach(function (layer) {
        if (layer instanceof ol.layer.Vector) {
            layer.getSource().forEachFeatureIntersectingExtent(extent, function (feature) {
                // Добавьте объект на слой выделения
                selectLayer.getSource().addFeature(feature);
            });
        }
    });
});


export { zoomButtonsContainer, selectLayer, dragBox };