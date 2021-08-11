import { Fragment, useContext, useEffect } from "react";
import { RouteComponentProps } from "react-router-dom";

import {
    AttachmentGallery,
    Breadcrumbs,
    MapComponent,
    SingleFeatureTable,
} from "../../components";
import {
    FeatureDetailsPageParams,
    Layer,
    LayerFeaturesRemoteResponse,
} from "../../types";
import { Manager } from "../../context";
import axios, { AxiosResponse } from "axios";

const FeatureDetails = ({
    match,
}: RouteComponentProps<FeatureDetailsPageParams>) => {
    const {
        activeLayer,
        availableLayers,
        setActiveLayer,
        activeFeatureId,
        setActiveFeatureId,
    } = useContext(Manager);
    const { layerName, featureId } = match.params;

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

    useEffect(() => {
        setActiveFeatureId(featureId);
    }, [featureId, setActiveFeatureId]);

    return (
        <Fragment>
            <h2>
                {activeLayer?.title} - {activeFeatureId}
            </h2>
            <Breadcrumbs />
            <div className="row">
                <div className="col-md-6">
                    <MapComponent />
                </div>
                <div className="col-md-6">
                    <SingleFeatureTable />
                </div>
            </div>
            <AttachmentGallery />
        </Fragment>
    );
};

export default FeatureDetails;
