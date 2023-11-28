import Map from 'https://cdn.skypack.dev/ol/Map.js';
import View from 'https://cdn.skypack.dev/ol/View.js';
import { transform } from 'https://cdn.skypack.dev/ol/proj.js';
import {
  defaults as defaultInteractions,
} from 'https://cdn.skypack.dev/ol/interaction.js';
import { toStringHDMS } from 'https://cdn.skypack.dev/ol/coordinate.js';
import { exploLayer, razvLayer, regLayer, razvexpLayer, minLayer, otherLayer, pointSource, labelLayer } from './layers.js';
import { zoomButtonsContainer, select, dragBox } from './controls.js';
import { fieldsLayer } from './fields.js';
import { VZULayer } from './VZU.js';

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
const scaleLineControl = new ol.control.ScaleLine({
  units: 'metric',
  steps: 1,
  minWidth: 100,
  maxWidth: 150,
});

function animate() {
  map.render();
  window.requestAnimationFrame(animate);
}

// настройка отображения координат
const mousePositionControl = new ol.control.MousePosition({
  coordinateFormat: function (coordinate) {
    return toStringHDMS(coordinate, 4);
  },
  projection: 'EPSG:4326',
  className: 'custom-mouse-position',
  target: document.getElementById('mouse-position'),
});

// настройка выбора и перетаскивания

let translate = new ol.interaction.Translate({
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

// Инструемент для редактирования полигонов (всех)
const modify = new ol.interaction.Modify({ source: fieldsLayer.getSource() });
modify.setActive(false);
// Реакция инструментов на кнопку "Редактировать"
function updateEditingState() {
  if (editingEnabled) {
    translate.setActive(true);
    modify.setActive(true);
  } else {
    translate.setActive(false);
    modify.setActive(false);
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
      visible: false,
      fold: 'close',
      layers: [
        new ol.layer.Group({
          title: 'ArcGIS',
          layers: [
            new ol.layer.Tile({
              source: new ol.source.XYZ({
                url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                maxZoom: 19, // Уровень максимального масштаба
              }),
            }),
          ]
        }),
        new ol.layer.Group({
          title: 'Google',
          layers: [
            new ol.layer.Tile({
              source: new ol.source.XYZ({
                url: 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                maxZoom: 20,
              }),
            }),
          ]
        }),
      ]
    }),
    new ol.layer.Group({
      title: 'Дополнительные слои',
      visible: false,
      fold: 'close',
      layers: [
        new ol.layer.Group({
          title: 'Абсолютные отметки (пока нету)',
          layers: [
          ]
        }),
      ]
    }),
    new ol.layer.Group({
      title: 'Данные',
      fold: 'open',
      layers: [
        new ol.layer.Group({
          title: 'Месторождения',
            layers: [
              fieldsLayer,
          ]
        }),
        new ol.layer.Group({
          title: 'Водозаборы',
          layers: [
            VZULayer,
          ]
        }),        
        new ol.layer.Group({
          title: 'Скважины',
          fold: 'close',
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

let tooltip = new ol.Overlay({
  element: tooltipContainer,
  autoPan: false,
  autoPanAnimation: {
    duration: 250,
  },
});

map.on('pointermove', function (evt) {
  if (measure || editingEnabled) {
    return;
  }

  let features = map.getFeaturesAtPixel(evt.pixel);

  if (features && features.length > 0) {
    let tooltipText = '<b>Краткая информация:</b><br>';

    features.forEach((feature) => {
      let coordinates;
      let extra;
      let nameGwk;

      if (feature.getGeometry().getType() === 'Point') {
        coordinates = feature.getGeometry().getCoordinates();
        extra = feature.get('extra');
        nameGwk = extra?.name_gwk || 'Н/Д';
        tooltipText += '<b>Номер:</b> ' + feature.get('name') + '<br>' +
          '<b>Тип:</b> ' + feature.get('typo') + '<br>' +
          '<b>ГВК:</b> ' + nameGwk + '<br>';
      } else if (feature.getGeometry().getType() === 'Polygon' || feature.getGeometry().getType() === 'MultiPolygon') {
        coordinates = evt.coordinate;
        const properties = feature.getProperties();

        if ('field_name' in properties) {
          tooltipText += '<b>Месторождение:</b> ' + feature.get('field_name') + '<br>';
        } else if ('intake_name' in properties) {
          tooltipText += '<b>Владелец ВЗУ:</b> ' + feature.get('intake_name') + '<br>';
        }
      }
      tooltip.setPosition(coordinates);
    });

    tooltipContent.innerHTML = tooltipText;
  } else {
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
      <h2>Информация:</h2>
      <hr>
      ${selectedFeatures.map((selectedFeature) => {
      const featureProperties = selectedFeature.getProperties();
      let nameGwk = featureProperties.extra && featureProperties.extra.name_gwk ? featureProperties.extra.name_gwk : 'Н/Д';

      let info = '';
      if (featureProperties.geometry.getType() === 'Point') {
        // Если точка
        info += `
            <strong>Номер ГВК:</strong> ${nameGwk}<br>
            <strong>Внутренний номер:</strong> ${featureProperties.name}<br>
            <strong>Тип:</strong> ${featureProperties.typo}<br>
            <strong>А.О. устья:</strong> ${featureProperties.head}<br>
            <strong>Водозабор:</strong> ${featureProperties.intake}<br>
            <strong>Месторождение:</strong> ${featureProperties.field}<br>
            <hr>
          `;
      } else if (featureProperties.geometry.getType() === 'Polygon' || featureProperties.geometry.getType() === 'MultiPolygon') {
        // Если полигон
        if ('field_name' in featureProperties) {
          // Если есть свойство field_name, значит это полигон с информацией о месторождении
          info += `
              <strong>Месторождение:</strong> ${featureProperties.field_name}<br>
              <hr>
            `;
        } else if ('intake_name' in featureProperties) {
          // Если есть свойство intake_name, значит это полигон с информацией о ВЗУ
          info += `
              <strong>Владелец ВЗУ:</strong> ${featureProperties.intake_name}<br>
              <hr>
            `;
        }
      }

      return info;
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

map.addControl(new ol.control.Control({ element: zoomButtonsContainer }));
map.addControl(layerSwitcher);
map.addOverlay(tooltip);
map.addInteraction(modify);
map.addControl(scaleLineControl);
map.addInteraction(dragBox);
map.addLayer(labelLayer);
animate();
export { map, pointSource }
