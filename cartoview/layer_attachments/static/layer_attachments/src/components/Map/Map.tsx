import { LatLngExpression } from "leaflet";
import { MapContainer, TileLayer, LayersControl } from "react-leaflet";

import VersionControl from "./versioncontrol";
import "./Map.css";

const MapComponent = () => {
    const position: LatLngExpression = [30, 30];
    const zoom = 6;

    return (
        <MapContainer center={position} zoom={zoom}>
            <LayersControl position="topright">
                <LayersControl.BaseLayer checked name="Open Street Map">
                    <TileLayer
                        attribution='<a href="http://osm.org/copyright">OpenStreetMap</a>'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />
                </LayersControl.BaseLayer>
                <LayersControl.BaseLayer name="Satellite">
                    <TileLayer
                        attribution='<a href="https://www.esri.com/en-us/home">ESRI</a>'
                        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
                    />
                </LayersControl.BaseLayer>
                <LayersControl.BaseLayer name="Topographic">
                    <TileLayer
                        attribution='<a href="https://www.esri.com/en-us/home">ESRI</a>'
                        url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}"
                    />
                </LayersControl.BaseLayer>
            </LayersControl>
            <VersionControl />
        </MapContainer>
    );
};

export default MapComponent;
