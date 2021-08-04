import axios, { AxiosResponse } from "axios";
import { useEffect, useState } from "react";

import { DjangoProps, Layer, LayerRemoteResponse } from "../../types";
import Manager from "./Manager";

declare const djangoProps: DjangoProps;

const ManagerProvider: React.FC = (props) => {
    const [showLoadingSpinner, setShowLoadingSpinner] =
        useState<boolean>(false);
    const [availableLayers, setAvailableLayers] = useState<Layer[]>([]);
    const [activeLayer, setActiveLayer] = useState<Layer | undefined>();
    const [activeFeatureId, setActiveFeatureId] = useState("");

    useEffect(() => {
        async function fetchAvailableLayers() {
            const availableLayersResponse: AxiosResponse<
                LayerRemoteResponse[]
            > = await axios.get(
                `${djangoProps.baseURL}api/layer_attachments/layers/`
            );
            const tempAvailableLayers: Layer[] =
                availableLayersResponse.data.map((layerResponse) => {
                    return {
                        id: layerResponse.id,
                        name: layerResponse.name,
                        title: layerResponse.title,
                        typeName: layerResponse.typename,
                        owsUrl: layerResponse.ows_url,
                        date: layerResponse.date,
                        thumbnailUrl: layerResponse.thumbnail_url,
                        layerAttributes: layerResponse.layer_attributes,
                    };
                });
            setAvailableLayers(tempAvailableLayers);
        }
        fetchAvailableLayers();
    }, []);

    return (
        <Manager.Provider
            value={{
                activeLayer,
                availableLayers,
                setActiveLayer,
                activeFeatureId,
                setActiveFeatureId,
                showLoadingSpinner,
                setShowLoadingSpinner,
            }}
        >
            {props.children}
        </Manager.Provider>
    );
};

export default ManagerProvider;
