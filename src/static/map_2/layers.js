import { vectorSource }from './main.js';

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
export { razvexpLayer }