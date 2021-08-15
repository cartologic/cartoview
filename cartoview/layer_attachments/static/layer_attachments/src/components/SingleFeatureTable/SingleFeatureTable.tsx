import { useContext, useEffect, useState } from "react";
import { Manager } from "../../context";
import { GeoJsonFeature } from "../../types";

const SingleFeatureTable = () => {
    const { activeLayer, activeFeatureId } = useContext(Manager);
    const [activeFeature, setActiveFeature] = useState<GeoJsonFeature>();

    useEffect(() => {
        if (activeFeatureId && activeLayer && activeLayer.geojson) {
            const tempActiveFeature = activeLayer.geojson.features.filter(
                (feature) => feature.id == activeFeatureId
            )[0];
            setActiveFeature(tempActiveFeature);
        }
    }, [activeFeatureId, activeLayer]);

    return (
        <table className="table table-striped table-responsive">
            <tbody>
                <tr style={{ color: "green" }}>
                    <th>ID</th>
                    <td>
                        {activeFeature?.id}
                    </td>
                </tr>
                {activeFeature &&
                    activeLayer &&
                    activeLayer.geojson &&
                    activeLayer.layerAttributes.map((layerAttribute, index) => (
                        <tr key={`feature-attribute-${index}`}>
                            <th scope="row">{layerAttribute}</th>
                            <td>
                                {activeFeature.properties &&
                                    activeFeature.properties[layerAttribute]}
                            </td>
                        </tr>
                    ))}
            </tbody>
        </table>
    );
};

export default SingleFeatureTable;
