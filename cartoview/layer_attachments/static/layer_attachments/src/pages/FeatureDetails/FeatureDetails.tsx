import { Fragment, useContext, useEffect } from "react";
import { RouteComponentProps } from "react-router-dom";

import { Breadcrumbs, MapComponent } from "../../components";
import { FeatureDetailsPageParams, Layer } from "../../types";
import { Manager } from "../../context";

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
        if (!activeLayer && availableLayers && layerName) {
            const activeLayer: Layer = availableLayers.filter(
                (layer) => layer.name === layerName
            )[0];
            setActiveLayer(activeLayer);
        }
    }, [availableLayers, activeLayer, setActiveLayer, layerName]);

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
            </div>
        </Fragment>
    );
};

export default FeatureDetails;
