import axios, { AxiosResponse } from "axios";
import { Fragment, useContext, useEffect, useState } from "react";
import { RouteComponentProps } from "react-router-dom";

import { Breadcrumbs, FeatureTable, MapComponent } from "../../components";
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
    const [layerFeatures, setLayerFeatures] = useState<any>([]);

    useEffect(() => {
        if (layerName && availableLayers.length) {
            const activeLayer: Layer = availableLayers.filter(
                (layer) => layer.name === layerName
            )[0];
            setActiveLayer(activeLayer);
        }
    }, [availableLayers, layerName, setActiveLayer]);

    useEffect(() => {
        async function fetchLayerFeatures() {
            if (activeLayer) {
                const params = {
                    service: "WFS",
                    request: "GetFeature",
                    outputFormat: "application/json",
                    typenames: activeLayer?.typeName,
                };
                try {
                    const layerFeaturesResponse: AxiosResponse<LayerFeaturesRemoteResponse> =
                        await axios.get(activeLayer.owsUrl, { params });
                    const tempLayerFeatures =
                        layerFeaturesResponse.data.features.map(
                            (feature) => feature.properties
                        );
                    setLayerFeatures(tempLayerFeatures);
                } catch (error) {
                    console.log(error);
                }
            }
        }
        fetchLayerFeatures();
    }, [activeLayer]);

    return (
        <Fragment>
            <h2>{activeLayer?.title}</h2>
            <Breadcrumbs />
            <MapComponent />
            <FeatureTable
                tableHeaders={activeLayer?.layerAttributes}
                tableRows={layerFeatures}
            />
        </Fragment>
    );
};

export default LayerDetails;
