import { map, pointSource, updateEditingState } from "./main.js";
import { platformModifierKeyOnly } from 'https://cdn.skypack.dev/ol/events/condition.js';
import { getWidth } from 'https://cdn.skypack.dev/ol/extent.js';

// статус кнопки редактирования
let editingEnabled = false;

// масштабная линейка и анимация карты
const scaleLineControl = new ol.control.ScaleLine({
    units: 'metric',
    steps: 1,
    minWidth: 100,
    maxWidth: 150,
});

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
// инструмент выделения
let select = new ol.interaction.Select();
// выбор прямоугольником
const selectedFeatures = select.getFeatures();

const dragBox = new ol.interaction.DragBox({
    condition: platformModifierKeyOnly,
});

dragBox.on('boxend', function () {
    const boxExtent = dragBox.getGeometry().getExtent();

    // if the extent crosses the antimeridian process each world separately
    const worldExtent = map.getView().getProjection().getExtent();
    const worldWidth = getWidth(worldExtent);
    const startWorld = Math.floor((boxExtent[0] - worldExtent[0]) / worldWidth);
    const endWorld = Math.floor((boxExtent[2] - worldExtent[0]) / worldWidth);

    for (let world = startWorld; world <= endWorld; ++world) {
        const left = Math.max(boxExtent[0] - world * worldWidth, worldExtent[0]);
        const right = Math.min(boxExtent[2] - world * worldWidth, worldExtent[2]);
        const extent = [left, boxExtent[1], right, boxExtent[3]];

        const boxFeatures = pointSource
            .getFeaturesInExtent(extent)
            .filter(
                (feature) =>
                    !selectedFeatures.getArray().includes(feature) &&
                    feature.getGeometry().intersectsExtent(extent)
            );

        // features that intersect the box geometry are added to the
        // collection of selected features

        // if the view is not obliquely rotated the box geometry and
        // its extent are equalivalent so intersecting features can
        // be added directly to the collection
        const rotation = map.getView().getRotation();
        const oblique = rotation % (Math.PI / 2) !== 0;
        // when the view is obliquely rotated the box extent will
        // exceed its geometry so both the box and the candidate
        // feature geometries are rotated around a common anchor
        // to confirm that, with the box geometry aligned with its
        // extent, the geometries intersect
        if (oblique) {
            const anchor = [0, 0];
            const geometry = dragBox.getGeometry().clone();
            geometry.translate(-world * worldWidth, 0);
            geometry.rotate(-rotation, anchor);
            const extent = geometry.getExtent();
            boxFeatures.forEach(function (feature) {
                const geometry = feature.getGeometry().clone();
                geometry.rotate(-rotation, anchor);
                if (geometry.intersectsExtent(extent)) {
                    selectedFeatures.push(feature);
                }
            });
        } else {
            selectedFeatures.extend(boxFeatures);
        }
    }
});
// clear selection when drawing a new box and when clicking on the map
dragBox.on('boxstart', function () {
    selectedFeatures.clear();
});
// добавление кнопки режим редактирования
const editbuttonStyle = 'width: 22px; height: 22px; margin: 11px; font-size: 14px; margin-top: 60px; ';

function updateButtonStyle() {
    if (editingEnabled) {
        editButton.style.backgroundColor = 'red'; // Цвет при нажатии
    } else {
        editButton.style.backgroundColor = ''; // Цвет по умолчанию
    }
}

const editButton = document.createElement('button');
editButton.innerHTML = 'Р';
editButton.className = 'btn btn-primary';
editButton.style = editbuttonStyle;
editButton.addEventListener('click', function () {
    editingEnabled = !editingEnabled;
    updateButtonStyle();
    updateEditingState();
});
const customControls = document.createElement('div');
customControls.className = 'ol-control custom-controls';
customControls.appendChild(editButton);

export { zoomButtonsContainer, select, dragBox, customControls, editingEnabled, scaleLineControl };