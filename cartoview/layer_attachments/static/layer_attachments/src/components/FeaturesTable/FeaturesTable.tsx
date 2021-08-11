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
                        <th>index</th>
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
                                    key={`row-${singleFeature.properties.fid}`}
                                    className="cursor-hand text-primary"
                                    onClick={() => {
                                        history.push(
                                            `/${activeLayer?.name}/${singleFeature.properties.fid}/`
                                        );
                                        setActiveFeatureId(
                                            singleFeature.properties.fid
                                        );
                                    }}
                                >
                                    <th style={{ color: "green" }}>
                                        {index + 1}
                                    </th>
                                    {activeLayer &&
                                        activeLayer.layerAttributes.map(
                                            (tableHeader, index) => (
                                                <th
                                                    key={`row-entry-${singleFeature.properties.fid}-${index}`}
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
