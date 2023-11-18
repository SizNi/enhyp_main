import GeoJSON from 'https://cdn.skypack.dev/ol/format/GeoJSON.js';
import Map from 'https://cdn.skypack.dev/ol/Map.js';
import View from 'https://cdn.skypack.dev/ol/View.js';
import Overlay from 'https://cdn.skypack.dev/ol/Overlay.js';
import TileLayer from 'https://cdn.skypack.dev/ol/layer/Tile.js';
import OSM from 'https://cdn.skypack.dev/ol/source/OSM.js';
import {transform} from 'https://cdn.skypack.dev/ol/proj.js';
import Vector from 'https://cdn.skypack.dev/ol/source/Vector.js';
import WebGLPointsLayer from 'https://cdn.skypack.dev/ol/layer/WebGLPoints.js';
import {
  Modify,
  Select,
  defaults as defaultInteractions,
} from 'https://cdn.skypack.dev/ol/interaction.js';
import {createStringXY, toStringHDMS, format as formatHDMS} from 'https://cdn.skypack.dev/ol/coordinate.js';
import {defaults as defaultControls, FullScreen} from 'https://cdn.skypack.dev/ol/control.js';
import MousePosition from 'https://cdn.skypack.dev/ol/control/MousePosition.js';


const vectorSource = new Vector({
  url: '/map/points',
  format: new GeoJSON(),
  wrapX: true,
});

const mousePositionControl = new MousePosition({
  //coordinateFormat: createStringXY(4),
  //coordinateFormat: toStringHDMS,
  coordinateFormat: function(coordinate) {
    return toStringHDMS(coordinate, 4);
  },
  projection: 'EPSG:4326',
  // comment the following two lines to have the mouse position
  // be placed within the map.
  className: 'custom-mouse-position',
  target: document.getElementById('mouse-position'),
});

const select = new Select({
  wrapX: false,
});

const modify = new Modify({
  features: select.getFeatures(),
});

const predefinedStyles = {
  icons: {
    'icon-src': 'data/icon.png',
    'icon-width': 18,
    'icon-height': 28,
    'icon-color': 'lightyellow',
    'icon-rotate-with-view': false,
    'icon-displacement': [0, 9],
  },
  triangles: {
    'shape-points': 3,
    'shape-radius': 9,
    'shape-fill-color': [
      'interpolate',
      ['linear'],
      ['get', 'population'],
      20000,
      '#5aca5b',
      300000,
      '#ff6a19',
    ],
    'shape-rotate-with-view': true,
  },
  'triangles-latitude': {
    'shape-points': 3,
    'shape-radius': [
      'interpolate',
      ['linear'],
      ['get', 'population'],
      40000,
      6,
      2000000,
      12,
    ],
    'shape-fill-color': [
      'interpolate',
      ['linear'],
      ['get', 'latitude'],
      -60,
      '#ff14c3',
      -20,
      '#ff621d',
      20,
      '#ffed02',
      60,
      '#00ff67',
    ],
    'shape-opacity': 0.95,
  },
  circles: {
    'circle-radius': [
      'interpolate',
      ['linear'],
      ['get', 'population'],
      40000,
      4,
      2000000,
      14,
    ],
    'circle-fill-color': ['match', ['get', 'hover'], 1, '#ff3f3f', '#006688'],
    'circle-rotate-with-view': false,
    'circle-displacement': [0, 0],
    'circle-opacity': [
      'interpolate',
      ['linear'],
      ['get', 'population'],
      40000,
      0.6,
      2000000,
      0.92,
    ],
  },
  'circles-zoom': {
    // by using an exponential interpolation with a base of 2 we can make it so that circles will have a fixed size
    // in world coordinates between zoom level 5 and 15
    'circle-radius': [
      'interpolate',
      ['exponential', 2],
      ['zoom'],
      5,
      1.5,
      15,
      1.5 * Math.pow(2, 10),
    ],
    'circle-fill-color': ['match', ['get', 'hover'], 1, '#ff3f3f', '#006688'],
    'circle-displacement': [0, 0],
    'circle-opacity': 0.95,
  },
  'rotating-bars': {
    'shape-rotation': ['*', ['time'], 0.13],
    'shape-points': 4,
    'shape-radius1': 4,
    'shape-radius2': 4 * Math.sqrt(2),
    'shape-scale': [
      'array',
      1,
      ['interpolate', ['linear'], ['get', 'population'], 20000, 1, 300000, 7],
    ],
    'shape-fill-color': [
      'interpolate',
      ['linear'],
      ['get', 'population'],
      20000,
      '#ffdc00',
      300000,
      '#ff5b19',
    ],
    'shape-displacement': [
      'array',
      0,
      ['interpolate', ['linear'], ['get', 'population'], 20000, 2, 300000, 14],
    ],
  },
};
const map = new Map({
  interactions: defaultInteractions().extend([select, modify]),
  controls: defaultControls().extend([mousePositionControl, new FullScreen({
    source: 'fullscreen',
  })]),
  target: 'map',
  layers: [
    new TileLayer({
      source: new OSM(),
    }),
  ],
  view: new View({

    center: transform([ 36.1874, 51.7373], 'EPSG:4326', 'EPSG:3857'),
    zoom: 8,
  }),
});
let literalStyle;
let pointsLayer;

let selected = null;

map.on('pointermove', function (ev) {
  if (selected !== null) {
    selected.set('hover', 0);
    selected = null;
  }

  map.forEachFeatureAtPixel(ev.pixel, function (feature) {
    feature.set('hover', 1);
    selected = feature;
    return true;
  });
});

function refreshLayer(newStyle) {
  const previousLayer = pointsLayer;
  pointsLayer = new WebGLPointsLayer({
    source: vectorSource,
    style: newStyle,
  });
  map.addLayer(pointsLayer);

  if (previousLayer) {
    map.removeLayer(previousLayer);
    previousLayer.dispose();
  }
  literalStyle = newStyle;
}

const spanValid = document.getElementById('style-valid');
const spanInvalid = document.getElementById('style-invalid');
function setStyleStatus(errorMsg) {
  const isError = typeof errorMsg === 'string';
  spanValid.style.display = errorMsg === null ? 'initial' : 'none';
  spanInvalid.firstElementChild.innerText = isError ? errorMsg : '';
  spanInvalid.style.display = isError ? 'initial' : 'none';
}

const editor = document.getElementById('style-editor');
editor.addEventListener('input', function () {
  const textStyle = editor.value;
  try {
    const newLiteralStyle = JSON.parse(textStyle);
    if (JSON.stringify(newLiteralStyle) !== JSON.stringify(literalStyle)) {
      refreshLayer(newLiteralStyle);
    }
    setStyleStatus(null);
  } catch (e) {
    setStyleStatus(e.message);
  }
});

const select_style = document.getElementById('style-select');
select_style.value = 'circles';
function onSelectChange() {
  const style = select_style.value;
  const newLiteralStyle = predefinedStyles[style];
  editor.value = JSON.stringify(newLiteralStyle, null, 2);
  try {
    refreshLayer(newLiteralStyle);
    setStyleStatus();
  } catch (e) {
    setStyleStatus(e.message);
  }
}
onSelectChange();
select_style.addEventListener('change', onSelectChange);

// animate the map
function animate() {
  map.render();
  window.requestAnimationFrame(animate);
}

//const projectionSelect = document.getElementById('projection');
//projectionSelect.addEventListener('change', function (event) {
//  mousePositionControl.setProjection(event.target.value);
//});

//const precisionInput = document.getElementById('precision');
//precisionInput.addEventListener('change', function (event) {
//  //const format = createStringXY(event.target.valueAsNumber);
//  const format = toStringHDMS(event.target.valueAsNumber);
//  mousePositionControl.setCoordinateFormat;
//});

var tooltipContainer = document.getElementById('tooltip');
var tooltipContent = document.getElementById('tooltip-content');

var tooltip = new Overlay({
  element: tooltipContainer,
  autoPan: true,
  autoPanAnimation: {
    duration: 250
  }
});
map.addOverlay(tooltip);

var featureId = '';

map.on('pointermove', function(evt) {
  var feature = map.forEachFeatureAtPixel(evt.pixel, function(feature) {
    if (featureId == feature.get('pk')) {
      return feature;
    };
    featureId = feature.get('pk');
    var coordinates = feature.getGeometry().getCoordinates();
    tooltipContent.innerHTML = 'You are over point<br>id:' + featureId + '<br>' + 'name: ' + feature.get('name') + '<br>' + 'тип: ' + feature.get('typo') + '<br>' + 'водозабор: ' + feature.get('intake')+ '<br>' + 'Месторождение: ' + feature.get('field') + '<br>' + 'extra (ГВК): ' + feature.get('extra').name_gwk + '<br>';
    console.log(feature.get('extra'))
    tooltip.setPosition(coordinates);
    return feature;
  });
  if (!feature && (featureId != '')) {
    featureId = '';
    tooltip.setPosition(undefined);
  };
});

animate();