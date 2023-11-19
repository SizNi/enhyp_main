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
import TileLayer from 'https://cdn.skypack.dev/ol/layer/Tile.js';
import OSM from 'https://cdn.skypack.dev/ol/source/OSM.js';
import Vector from 'https://cdn.skypack.dev/ol/source/Vector.js';
import MousePosition from 'https://cdn.skypack.dev/ol/control/MousePosition.js';
import { toStringHDMS } from 'https://cdn.skypack.dev/ol/coordinate.js';
import Overlay from 'https://cdn.skypack.dev/ol/Overlay.js';
import ScaleLine from 'https://cdn.skypack.dev/ol/control/ScaleLine.js';
import Draw from 'https://cdn.skypack.dev/ol/interaction/Draw.js';
import { LineString } from 'https://cdn.skypack.dev/ol/geom.js';
import { Fill, Stroke, Style, Circle as CircleStyle } from 'https://cdn.skypack.dev/ol/style.js';


// Создание оверлея для отображения длины линейки
const lengthOverlay = new Overlay({
  element: document.getElementById('length-display'), // Замените 'length-overlay' на ID вашего элемента
  positioning: 'bottom-center',
  stopEvent: false,
});
// Обновление длины линейки на оверлее
function updateLengthOverlay(length) {
  const lengthFormatted = new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 2 }).format(length / 1000);
  lengthOverlay.getElement().innerText = `Длина: ${lengthFormatted} км`;
}
// слой для рисования линейки
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
// Создание инструмента рисования линий
const drawLine = new Draw({
  source: drawLayer.getSource(),
  type: 'LineString',
});

// Событие завершения рисования линии
drawLine.on('drawend', function (event) {
  const feature = event.feature;
  const geometry = feature.getGeometry();
  const length = geometry.getLength();
  updateLengthOverlay(length);
});

let measure = false;

// Обработчик для кнопки рисования линии
document.getElementById('drawLineButton').addEventListener('click', function () {
  measure = !measure;
  console.log(measure);
  document.getElementById('drawLineButton').innerText = measure ? 'Выключить линейку' : 'Линейка';
  updateMeasureState();
});

function updateMeasureState() {
  if (measure) {
    // Включаем режим рисования линии
    drawLine.setActive(true);

    // Выключаем другие режимы
    select.setActive(false);
    translate.setActive(false);
    document.getElementById('length-display').innerText = '';
  } else {
    // Выключаем режим рисования линии
    drawLine.setActive(false);

    // Включаем режим выбора
    select.setActive(true);
  }
}

// масштабная линейка
const scaleLineControl = new ScaleLine({
  units: 'metric', // Используйте метрические единицы измерения
  // bar: true,       // Отобразить панель с линейкой
  steps: 1,        // Количество шагов на линейке
  // text: true,      // Отобразить текст с масштабом
  minWidth: 100,   // Минимальная ширина панели
  maxWidth: 150,   // Максимальная ширина панели
});

// animate the map
function animate() {
  map.render();
  window.requestAnimationFrame(animate);
}

// добавление точек
const vectorSource = new Vector({
  url: '/map/points',
  format: new GeoJSON(),
  wrapX: true,
});

const vectorLayer = new VectorLayer({
  source: vectorSource,
});

// координаты
const mousePositionControl = new MousePosition({
  coordinateFormat: function (coordinate) {
    return toStringHDMS(coordinate, 4);
  },
  projection: 'EPSG:4326',
  className: 'custom-mouse-position',
  target: document.getElementById('mouse-position'),
});
// переменные для выбора и перетаскивания
let select = new Select();
let translate = new Translate({
  features: select.getFeatures(),
});
select.setActive(true);     // изначально выбор выключен
translate.setActive(false);  // изначально перетаскивание выключен

let editingEnabled = false;

// Событие по клику на кнопку "Редактировать"
document.getElementById('editButton').addEventListener('click', function () {
  editingEnabled = !editingEnabled;
  console.log(editingEnabled)
  editButton.innerText = editingEnabled ? 'Выключить редактирование' : 'Редактировать';
  updateEditingState();
});
// в зависимости от нажатия кнопки - включается и открючается режим редактирования
function updateEditingState() {
  if (editingEnabled) {
    translate.setActive(true);
  } else {
    translate.setActive(false);
    select.getFeatures().clear(); // Очистка выбранных объектов
  }
}
console.log(editingEnabled)

const map = new Map({
  interactions: defaultInteractions().extend([select, translate]),
  controls: defaultInteractions().extend([mousePositionControl, scaleLineControl]),
  target: 'map',
  layers: [
    new TileLayer({
      source: new OSM(),
    }),
  ],
  view: new View({
    center: transform([36.1874, 51.7373], 'EPSG:4326', 'EPSG:3857'),
    zoom: 10,
  }),
});


// всплывающие подсказки для скважин
var tooltipContainer = document.getElementById('tooltip');
var tooltipContent = document.getElementById('tooltip-content');

var tooltip = new Overlay({
  element: tooltipContainer,
  autoPan: false,
  autoPanAnimation: {
    duration: 250
  }
});

var featureId = '';
// условие отображения подсказки
map.on('pointermove', function (evt) {
  var feature = map.forEachFeatureAtPixel(evt.pixel, function (feature) {
    if (featureId == feature.get('pk')) {
      return feature;
    };
    featureId = feature.get('pk');
    var coordinates = feature.getGeometry().getCoordinates();
    // Проверка наличия свойства extra
    var extra = feature.get('extra');
    var nameGwk = extra?.name_gwk || 'Н/Д';
    tooltipContent.innerHTML = '<b>Краткая информация<br>Номер:</b> ' + feature.get('name') + '<br>' + '<b>Тип:</b> ' + feature.get('typo') + '<br>' + '<b>ГВК:</b> ' + nameGwk + '<br>';
    console.log(feature.get('extra'))
    tooltip.setPosition(coordinates);
    return feature;
  });
  if (!feature && (featureId != '')) {
    featureId = '';
    tooltip.setPosition(undefined);
  };
});

// информационная панель
const infoPanel = document.getElementById('info-panel');
select.getFeatures().on('add', function (event) {
  updateInfoPanel();
});

select.getFeatures().on('remove', function (event) {
  updateInfoPanel();
});

// добавление информции на информационную панель
function updateInfoPanel() {
  const selectedFeatures = select.getFeatures().getArray();
  if (selectedFeatures.length > 0) {
    // Генерируем HTML с информацией о каждом выбранном объекте
    const infoHTML = `
      <h2>Информация</h2>
      <hr> <!-- Черта для отделения текста -->
      ${selectedFeatures.map((selectedFeature) => {
      const featureProperties = selectedFeature.getProperties();

      // Проверка наличия свойства extra и name_gwk
      var nameGwk = featureProperties.extra && featureProperties.extra.name_gwk ? featureProperties.extra.name_gwk : 'Н/Д';

      return `
          <strong>Номер ГВК:</strong> ${nameGwk}<br>
          <strong>Внутренний номер:</strong> ${featureProperties.name}<br>
          <strong>Тип:</strong> ${featureProperties.typo}<br>
          <strong>А.О. устья:</strong> ${featureProperties.head}<br>
          <strong>Водозабор:</strong> ${featureProperties.intake}<br>
          <strong>Месторождение:</strong> ${featureProperties.field}<br>
          <hr> <!-- Черта для отделения текста -->
        `;
    }).join('')}
    `;

    // Вставляем информацию в панель
    infoPanel.innerHTML = infoHTML;

    // Показываем панель
    infoPanel.style.display = 'block';
  } else {
    // Если ничего не выбрано, скрываем панель
    infoPanel.style.display = 'none';
  }
}
translate.on('translateend', function (event) {
  // Получите измененные объекты
  const features = event.features.getArray();

  // Выведите новые координаты в консоль
  features.forEach(function (feature) {
    const coordinates = transform(feature.getGeometry().getCoordinates(), 'EPSG:3857', 'EPSG:4326');
    console.log('Новые координаты точки:', coordinates);
    const featureId = feature.get('pk');
    updateCoordinates(featureId, coordinates);
  });
});
// обновление координат
function updateCoordinates(featureId, coordinates) {
  const url = `/base/api/wells/${featureId}`; // Путь к серверному эндпоинту
  const data = {
    coordinates: coordinates,
  };
  console.log(url)
  console.log('Отправляемый запрос:', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
}
map.addOverlay(lengthOverlay);
map.addInteraction(drawLine);
map.addLayer(drawLayer);
map.addLayer(vectorLayer);
map.addOverlay(tooltip);
map.addControl(scaleLineControl);
animate();