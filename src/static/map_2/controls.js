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

export { zoomButtonsContainer };