import axios, { AxiosResponse } from "axios";
import { Fragment, useContext, useEffect } from "react";
import { RouteComponentProps } from "react-router-dom";

import {
    Breadcrumbs,
    DownloadAttachments,
    FeatureTable,
    MapComponent,
} from "../../components";
import { Manager } from "../../context";
import {
    Layer,
    LayerDetailsPageParams,
    LayerFeaturesRemoteResponse,
} from "../../types";

const LayerDetails = ({
    match,
}: RouteComponentProps<LayerDetailsPageParams>) => {
    const layerName = match.params.layerName;
    const { availableLayers, setActiveLayer, activeLayer } =
        useContext(Manager);

    useEffect(() => {
        const fetchLayerDetails = async () => {
            if (layerName && availableLayers.length && !activeLayer) {
                const tempActiveLayer: Layer = availableLayers.filter(
                    (layer) => layer.name === layerName
                )[0];
                const params = {
                    service: "WFS",
                    request: "GetFeature",
                    outputFormat: "application/json",
                    srsName: "EPSG:4326",
                    typenames: tempActiveLayer?.typeName,
                };
                try {
                    const layerFeaturesResponse: AxiosResponse<LayerFeaturesRemoteResponse> =
                        await axios.get(tempActiveLayer.owsUrl, { params });
                    tempActiveLayer.geojson = layerFeaturesResponse.data;
                    setActiveLayer(tempActiveLayer);
                } catch (error) {
                    console.log(error);
                }
            }
        };

        fetchLayerDetails();
    }, [activeLayer, availableLayers, layerName, setActiveLayer]);

    return (
        <Fragment>
            <h2>{activeLayer?.title}</h2>
            <Breadcrumbs />
            <MapComponent />
            <FeatureTable />
            <DownloadAttachments />
        </Fragment>
    );
};

export default LayerDetails;
