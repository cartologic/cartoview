import { useEffect, useRef, useState, useContext } from "react";
import L, {
    GeoJSON as LeafletGeoJSON,
    LatLng,
    LatLngExpression,
    Map as LeafletMap,
    PathOptions,
    StyleFunction,
} from "leaflet";
import { Feature, GeometryObject } from "geojson";
import { MapContainer, TileLayer, LayersControl, GeoJSON } from "react-leaflet";

import defaultMarkerIcon from "../../assets/images/default-marker-icon.png";
import customMarkerIcon from "../../assets/images/custom-marker-icon.png";
import markerShadow from "../../assets/images/marker-shadow.png";
import VersionControl from "./versioncontrol";
import { Manager } from "../../context";
import "./Map.css";

const MapComponent = () => {
    const position: LatLngExpression = [30, 30];
    const zoom = 6;
    const [leafletMap, setLeafletMap] = useState<LeafletMap>();
    const geojsonRef = useRef<LeafletGeoJSON>(null);
    const { activeLayer, activeFeatureId } = useContext(Manager);

    const geojsonStylePolygon: StyleFunction = (feature): PathOptions => {
        if (
            activeFeatureId &&
            feature &&
            feature.properties &&
            activeFeatureId == feature.properties.fid
        ) {
            return { fillColor: "#FF4848", color: "#B61919", weight: 2 };
        } else {
            return { fillColor: "#6E85B2", color: "#0F52BA", weight: 2 };
        }
    };

    const geojsonStylePoint = (
        feature: Feature<GeometryObject>,
        latlng: LatLng
    ) => {
        const defaultMapMarker = L.icon({
            iconUrl: defaultMarkerIcon,
            shadowUrl: markerShadow,
        });
        const highlightMapMarker = L.icon({
            iconUrl: customMarkerIcon,
            shadowUrl: markerShadow,
        });

        if (
            activeFeatureId &&
            feature &&
            feature.properties &&
            activeFeatureId == feature.properties.fid
        ) {
            return L.marker(latlng, { icon: highlightMapMarker });
        } else {
            return L.marker(latlng, { icon: defaultMapMarker });
        }
    };

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
                <GeoJSON
                    data={activeLayer.geojson}
                    ref={geojsonRef}
                    style={geojsonStylePolygon}
                    pointToLayer={geojsonStylePoint}
                />
            )}
        </MapContainer>
    );
};

export default MapComponent;
