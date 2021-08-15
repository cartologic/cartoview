import { useContext } from "react";
import { useHistory } from "react-router-dom";

import { Manager } from "../../context";
import "./FeaturesTable.css";

const FeaturesTable = () => {
    const { activeLayer, setActiveFeatureId } = useContext(Manager);
    const history = useHistory();

    return (
        <div className="table-wrapper">
            <table className="table table-striped table-responsive">
                <thead>
                    <tr>
                        <th>Index</th>
                        <th>ID</th>
                        {activeLayer &&
                            activeLayer.layerAttributes.map((tableHeader) => (
                                <th key={tableHeader}>{tableHeader}</th>
                            ))}
                    </tr>
                </thead>
                <tbody>
                    {activeLayer &&
                        activeLayer.geojson &&
                        activeLayer.geojson.features.map(
                            (singleFeature, index) => (
                                <tr
                                    key={`${singleFeature.id}`}
                                    className="cursor-hand text-primary"
                                    onClick={() => {
                                        history.push(
                                            `/${activeLayer?.name}/${singleFeature.id}/`
                                        );
                                        setActiveFeatureId(
                                            singleFeature.id
                                        );
                                    }}
                                >
                                    <th style={{ color: "green" }}>
                                        {index + 1}
                                    </th>
                                    <th style={{ color: "green" }}>
                                        {singleFeature.id}
                                    </th>
                                    {activeLayer &&
                                        activeLayer.layerAttributes.map(
                                            (tableHeader, index) => (
                                                <th
                                                    key={`row-entry-${singleFeature.id}-${index}`}
                                                >
                                                    {
                                                        singleFeature
                                                            .properties[
                                                        tableHeader
                                                        ]
                                                    }
                                                </th>
                                            )
                                        )}
                                </tr>
                            )
                        )}
                </tbody>
            </table>
        </div>
    );
};

export default FeaturesTable;
