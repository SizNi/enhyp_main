import { Fill, Stroke, Style, Circle as CircleStyle } from 'https://cdn.skypack.dev/ol/style.js';
import VectorLayer from 'https://cdn.skypack.dev/ol/layer/Vector.js';

const mapboxAccessToken = 'pk.eyJ1Ijoib3ZlY2hrYSIsImEiOiJjbHBqd3B2N2kwM3RnMmlvN3dpbGNraTMxIn0.ofTpuRpIq2Ex47kZ-RC8Ig';
// Данные с точками
const pointSource = new ol.source.Vector({
    url: '/map/points',
    format: new ol.format.GeoJSON(),
    wrapX: true,
});
// слои для точек
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
    source: pointSource,
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
    source: pointSource,
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
    source: pointSource,
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
    source: pointSource,
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
    source: pointSource,
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
    source: pointSource,
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

// оверлей для отображения номеров скважин
const labelLayer = new VectorLayer({
    // source: pointSource,
});
// карта абсолютных отметок
const terrainStyle = new Style({
    fill: new ol.style.Fill({
        color: 'rgba(66, 100, 251, 0.3)',
    }),
    stroke: new ol.style.Stroke({
        color: 'rgba(66, 100, 251, 1)',
    })

});

const terrainLayer = new ol.layer.Tile({
    source: new ol.source.XYZ({
        url: `https://api.mapbox.com/v4/mapbox.mapbox-terrain-v2/{z}/{x}/{y}.pngraw?access_token=${mapboxAccessToken}`,
        attributions: '© <a href="https://www.mapbox.com/map-feedback/">Mapbox</a>',
    }),
})

export { exploLayer, razvLayer, regLayer, razvexpLayer, minLayer, otherLayer, pointSource, labelLayer, terrainLayer };