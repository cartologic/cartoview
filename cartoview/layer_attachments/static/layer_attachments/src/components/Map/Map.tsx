import { useEffect, useRef, useState, useContext } from "react";
import L, {
    GeoJSON as LeafletGeoJSON,
    LatLng,
    LatLngExpression,
    Map as LeafletMap,
} from "leaflet";
import { MapContainer, TileLayer, LayersControl, GeoJSON } from "react-leaflet";

import icon from "../../assets/images/marker-icon.png";
import iconShadow from "../../assets/images/marker-shadow.png";
import VersionControl from "./versioncontrol";
import { Manager } from "../../context";
import "./Map.css";

const DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
});

L.Marker.prototype.options.icon = DefaultIcon;

const MapComponent = () => {
    const position: LatLngExpression = [30, 30];
    const zoom = 6;
    const [leafletMap, setLeafletMap] = useState<LeafletMap>();
    const geojsonRef = useRef<LeafletGeoJSON>(null);
    const { activeLayer } = useContext(Manager);

    const fitMapToGeojson = () => {
        if (activeLayer && activeLayer.geojson && geojsonRef && leafletMap) {
            const southWestCorner = geojsonRef.current
                ?.getBounds()
                .getSouthWest();
            const northEastCorner = geojsonRef.current
                ?.getBounds()
                .getNorthEast();
            const corner1 = new LatLng(
                southWestCorner?.lat || 0,
                southWestCorner?.lng || 0
            );
            const corner2 = new LatLng(
                northEastCorner?.lat || 0,
                northEastCorner?.lng || 0
            );
            const mapBounds = L.latLngBounds(corner1, corner2);
            leafletMap.fitBounds(mapBounds);
        }
    };

    useEffect(fitMapToGeojson, [geojsonRef, activeLayer, leafletMap]);

    return (
        <MapContainer
            center={position}
            zoom={zoom}
            whenCreated={(mapInstance) => setLeafletMap(mapInstance)}
        >
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
            {activeLayer && activeLayer.geojson && (
                <GeoJSON data={activeLayer.geojson} ref={geojsonRef} />
            )}
        </MapContainer>
    );
};

export default MapComponent;
