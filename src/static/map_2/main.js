import GeoJSON from 'https://cdn.skypack.dev/ol/format/GeoJSON.js';
import Map from 'https://cdn.skypack.dev/ol/Map.js';
import VectorLayer from 'https://cdn.skypack.dev/ol/layer/Vector.js';
import View from 'https://cdn.skypack.dev/ol/View.js';
import { transform } from 'https://cdn.skypack.dev/ol/proj.js';
import {
  Select,
  Translate,
  defaults as defaultInteractions,
} from 'https://cdn.skypack.dev/ol/interaction.js';
import Vector from 'https://cdn.skypack.dev/ol/source/Vector.js';
import MousePosition from 'https://cdn.skypack.dev/ol/control/MousePosition.js';
import { toStringHDMS } from 'https://cdn.skypack.dev/ol/coordinate.js';
import Overlay from 'https://cdn.skypack.dev/ol/Overlay.js';
import ScaleLine from 'https://cdn.skypack.dev/ol/control/ScaleLine.js';
import Draw from 'https://cdn.skypack.dev/ol/interaction/Draw.js';
import { Fill, Stroke, Style, Circle as CircleStyle } from 'https://cdn.skypack.dev/ol/style.js';
import XYZ from 'https://cdn.skypack.dev/ol/source/XYZ.js';
import Control from 'https://cdn.skypack.dev/ol/control/Control.js';
import { razvexpLayer } from func.js

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

// Добавление контейнера с кнопками в элемент управления на карту

// Оверлей отображения длины линейки
const lengthOverlay = new Overlay({
  element: document.getElementById('length-display'),
  positioning: 'bottom-center',
  stopEvent: false,
});

function updateLengthOverlay(length) {
  const lengthFormatted = new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 2 }).format(length / 1000);
  lengthOverlay.getElement().innerText = `Длина: ${lengthFormatted} км`;
  lengthOverlay.setPosition(map.getCoordinateFromPixel(drawLine.sketchCoords_[0]));
  console.log(lengthFormatted);
}

// слой рисования линейки
const drawLayer = new VectorLayer({
  source: new Vector(),
  style: new Style({
    fill: new Fill({
      color: 'rgba(255, 255, 255, 0.2)',
    }),
    stroke: new Stroke({
      color: '#ffcc33',
      width: 2,
    }),
    image: new CircleStyle({
      radius: 7,
      fill: new Fill({
        color: '#ffcc33',
      }),
    }),
  }),
});

const drawLine = new Draw({
  source: drawLayer.getSource(),
  type: 'LineString',
});
drawLine.setActive(false);

// Событие начала рисования линии
drawLine.on('drawstart', function (event) {
  // Добавляем слушатель события pointermove при начале рисования
  map.on('pointermove', pointerMoveHandler);
});

// Событие завершения рисования линии
drawLine.on('drawend', function (event) {
  // Удаляем слушатель события pointermove после завершения рисования
  map.un('pointermove', pointerMoveHandler);

  const feature = event.feature;
  const geometry = feature.getGeometry();
  const length = geometry.getLength();
  updateLengthOverlay(length);
});
// Обработчик события pointermove при рисовании линии
function pointerMoveHandler(evt) {
  const feature = drawLine.sketchFeature_;
  if (feature) {
    const geometry = feature.getGeometry();
    const length = geometry.getLength();
    updateLengthOverlay(length);
  }
}
// обработчки для кнопки рисования линейки
let measure = false;

document.getElementById('drawLineButton').addEventListener('click', function () {
  measure = !measure;
  document.getElementById('drawLineButton').innerText = measure ? 'Выключить линейку' : 'Линейка';
  updateMeasureState();
});

function updateMeasureState() {
  if (measure) {
    drawLine.setActive(true);
    select.setActive(false);
    translate.setActive(false);
    document.getElementById('length-display').innerText = '';
  } else {
    drawLine.setActive(false);
    select.setActive(true);
  }
}

// масштабная линейка и анимация карты
const scaleLineControl = new ScaleLine({
  units: 'metric',
  steps: 1,
  minWidth: 100,
  maxWidth: 150,
});

function animate() {
  map.render();
  window.requestAnimationFrame(animate);
}
// добавление слоев для точек
const vectorSource = new Vector({
  url: '/map/points',
  format: new GeoJSON(),
  wrapX: true,
});

const baseStyle = new Style({
  stroke: new Stroke({
    color: 'black',
    width: 4,
  }),
  image: new CircleStyle({
    radius: 5,
    fill: new Fill({
      color: [255, 0, 0, 0.7],
    }),
  }),
});
const exploStyle = new Style({
  image: new CircleStyle({
    radius: 5,
    fill: new Fill({
      color: [17, 30, 108, 0.7],
    }),
  }),
});
const razvStyle = new Style({
  image: new CircleStyle({
    radius: 5,
    fill: new Fill({
      color: [14, 77, 146, 0.7],
    }),
  }),
});
const regStyle = new Style({
  image: new CircleStyle({
    radius: 5,
    fill: new Fill({
      color: [0, 128, 255, 0.7],
    }),
  }),
});
const razvexpStyle = new Style({
  image: new CircleStyle({
    radius: 5,
    fill: new Fill({
      color: [0, 49, 82, 0.7],
    }),
  }),
});
const minStyle = new Style({
  image: new CircleStyle({
    radius: 5,
    fill: new Fill({
      color: [0, 128, 129, 0.7],
    }),
  }),
});

const exploLayer = new VectorLayer({
  source: vectorSource,
  style: function (feature) {
    const typo = feature.get('typo');
    if (typo === 'эксплуатационный') {
      const combinedStyle = new Style({
        stroke: baseStyle.getStroke(),
        image: exploStyle.getImage(),
      });
      return combinedStyle
    } else {
      return null; // Возвращаем null для скрытия точек других типов
    }
  },
});

const razvLayer = new VectorLayer({
  source: vectorSource,
  style: function (feature) {
    const typo = feature.get('typo');
    if (typo === 'разведочный') {
      const combinedStyle = new Style({
        stroke: baseStyle.getStroke(),
        image: razvStyle.getImage(),
      });
      return combinedStyle
    } else {
      return null; // Возвращаем null для скрытия точек других типов
    }
  },
});
const regLayer = new VectorLayer({
  source: vectorSource,
  style: function (feature) {
    const typo = feature.get('typo');
    if (typo === 'режимный') {
      const combinedStyle = new Style({
        stroke: baseStyle.getStroke(),
        image: regStyle.getImage(),
      });
      return combinedStyle
    } else {
      return null; // Возвращаем null для скрытия точек других типов
    }
  },
});
const razvexpLayer = new VectorLayer({
  source: vectorSource,
  style: function (feature) {
    const typo = feature.get('typo');
    if (typo === 'разведочно-эксплуатационный') {
      const combinedStyle = new Style({
        stroke: baseStyle.getStroke(),
        image: razvexpStyle.getImage(),
      });
      return combinedStyle
    } else {
      return null; // Возвращаем null для скрытия точек других типов
    }
  },
});
const minLayer = new VectorLayer({
  source: vectorSource,
  style: function (feature) {
    const typo = feature.get('typo');
    if (typo === 'минеральный') {
      const combinedStyle = new Style({
        stroke: baseStyle.getStroke(),
        image: minStyle.getImage(),
      });
      return combinedStyle
    } else {
      return null; // Возвращаем null для скрытия точек других типов
    }
  },
});
const otherLayer = new VectorLayer({
  source: vectorSource,
  style: function (feature) {
    const types = ['эксплуатационный', 'разведочный', 'режимный', 'минеральный'];
    const typo = feature.get('typo');

    if (types.includes(typo)) {
      return null;
    } else {
      return baseStyle;
    }
  },
});

// настройка координат
const mousePositionControl = new MousePosition({
  coordinateFormat: function (coordinate) {
    return toStringHDMS(coordinate, 4);
  },
  projection: 'EPSG:4326',
  className: 'custom-mouse-position',
  target: document.getElementById('mouse-position'),
});

// настройка выбора и перетаскивания
let select = new Select();
let translate = new Translate({
  features: select.getFeatures(),
});

select.setActive(true);
translate.setActive(false);

let editingEnabled = false;

document.getElementById('editButton').addEventListener('click', function () {
  editingEnabled = !editingEnabled;
  editButton.innerText = editingEnabled ? 'Выключить редактирование' : 'Редактировать';
  updateEditingState();
});

function updateEditingState() {
  if (editingEnabled) {
    translate.setActive(true);
  } else {
    translate.setActive(false);
    select.getFeatures().clear();
  }
}


// инициализация карты
const map = new Map({
  interactions: defaultInteractions().extend([select, translate]),
  controls: defaultInteractions().extend([mousePositionControl, scaleLineControl]),
  target: 'map',
  layers: [
    new ol.layer.Group({
      title: 'Картографическая основа',
      layers: [
        new ol.layer.Group({
          title: 'OSM',
          type: 'base',
          combine: false,
          visible: true,
          layers: [
            new ol.layer.Tile({
              source: new ol.source.OSM(),
            }),
          ]
        }),
      ]
    }),
    new ol.layer.Group({
      title: 'Спутниковые снимки',
      layers: [
        new ol.layer.Group({
          title: 'ArcGIS',
          type: 'sputnik',
          combine: false,
          visible: true,
          layers: [
            new ol.layer.Tile({
              source: new XYZ({
                url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                maxZoom: 19, // Уровень максимального масштаба
              }),
            }),
          ]
        }),
      ]
    }),
    new ol.layer.Group({
      title: 'Данные',
      layers: [
        new ol.layer.Group({
          title: 'Скважины',
          layers: [
            new ol.layer.Group({
              title: 'Эксплуатационные',
              type: 'well',
              combine: false,
              visible: true,
              layers: [
                exploLayer,
              ]
            }),
            new ol.layer.Group({
              title: 'Разведочные',
              type: 'well',
              combine: false,
              visible: true,
              layers: [
                razvLayer,
              ]
            }),
            new ol.layer.Group({
              title: 'Разведочно-эксплуатационные',
              type: 'well',
              combine: false,
              visible: true,
              layers: [
                razvexpLayer,
              ]
            }),
            new ol.layer.Group({
              title: 'Режимные',
              type: 'well',
              combine: false,
              visible: true,
              layers: [
                regLayer,
              ]
            }),
            new ol.layer.Group({
              title: 'Минеральные',
              type: 'well',
              combine: false,
              visible: true,
              layers: [
                minLayer,
              ]
            }),
            new ol.layer.Group({
              title: 'Другие',
              type: 'well',
              combine: false,
              visible: true,
              layers: [
                otherLayer,
              ]
            }),
          ]
        }),
      ]
    }),
  ],
  view: new View({
    center: transform([36.1874, 51.7373], 'EPSG:4326', 'EPSG:3857'),
    zoom: 10,
  }),
});

var layerSwitcher = new ol.control.LayerSwitcher({
  collapsed: true,
  groupSelectStyle: 'group',
  tipLabel: 'Legend', // Optional label for button

});

let tooltipContainer = document.getElementById('tooltip');
let tooltipContent = document.getElementById('tooltip-content');

let tooltip = new Overlay({
  element: tooltipContainer,
  autoPan: false,
  autoPanAnimation: {
    duration: 250,
  },
});

let featureId = '';

map.on('pointermove', function (evt) {
  if (measure) {
    // Если рисование линии активно, не выполняем код для скважин
    return;
  }
  let feature = map.forEachFeatureAtPixel(evt.pixel, function (feature) {
    if (featureId == feature.get('pk')) {
      return feature;
    }
    featureId = feature.get('pk');
    let coordinates = feature.getGeometry().getCoordinates();
    let extra = feature.get('extra');
    let nameGwk = extra?.name_gwk || 'Н/Д';
    tooltipContent.innerHTML = '<b>Краткая информация<br>Номер:</b> ' + feature.get('name') + '<br>' + '<b>Тип:</b> ' + feature.get('typo') + '<br>' + '<b>ГВК:</b> ' + nameGwk + '<br>';
    tooltip.setPosition(coordinates);
    return feature;
  });
  if (!feature && featureId !== '') {
    featureId = '';
    tooltip.setPosition(undefined);
  }
});

const infoPanel = document.getElementById('info-panel');
select.getFeatures().on('add', function (event) {
  updateInfoPanel();
});

select.getFeatures().on('remove', function (event) {
  updateInfoPanel();
});

function updateInfoPanel() {
  const selectedFeatures = select.getFeatures().getArray();
  if (selectedFeatures.length > 0) {
    const infoHTML = `
      <h2>Информация</h2>
      <hr>
      ${selectedFeatures.map((selectedFeature) => {
      const featureProperties = selectedFeature.getProperties();
      let nameGwk = featureProperties.extra && featureProperties.extra.name_gwk ? featureProperties.extra.name_gwk : 'Н/Д';
      return `
          <strong>Номер ГВК:</strong> ${nameGwk}<br>
          <strong>Внутренний номер:</strong> ${featureProperties.name}<br>
          <strong>Тип:</strong> ${featureProperties.typo}<br>
          <strong>А.О. устья:</strong> ${featureProperties.head}<br>
          <strong>Водозабор:</strong> ${featureProperties.intake}<br>
          <strong>Месторождение:</strong> ${featureProperties.field}<br>
          <hr>
        `;
    }).join('')}
    `;
    infoPanel.innerHTML = infoHTML;
    infoPanel.style.display = 'block';
  } else {
    infoPanel.style.display = 'none';
  }
};

translate.on('translateend', function (event) {
  const features = event.features.getArray();
  features.forEach(function (feature) {
    const coordinates = transform(feature.getGeometry().getCoordinates(), 'EPSG:3857', 'EPSG:4326');
    console.log('Новые координаты точки:', coordinates);
    const featureId = feature.get('pk');
    updateCoordinates(featureId, coordinates);
  });
});

function updateCoordinates(featureId, coordinates) {
  const url = `/base/api/wells/${featureId}`;
  const data = {
    coordinates: coordinates,
  };
  console.log(url);
  console.log('Отправляемый запрос:', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
}
map.addControl(new Control({ element: zoomButtonsContainer }));
map.addControl(layerSwitcher);
// map.addLayer(satelliteLayer);
map.addOverlay(lengthOverlay);
map.addInteraction(drawLine);
map.addLayer(drawLayer);
// map.addLayer(vectorLayer);
map.addOverlay(tooltip);
map.addControl(scaleLineControl);
animate();

export { vectorSource }
