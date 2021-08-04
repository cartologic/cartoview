import { useContext } from "react";
import { useHistory } from "react-router-dom";

import { Manager } from "../../context";
import { FeaturesTableProps } from "../../types";
import "./FeaturesTable.css";

const FeaturesTable = (props: FeaturesTableProps) => {
    const { activeLayer, setActiveFeatureId } = useContext(Manager);
    const history = useHistory();
    const { tableHeaders, tableRows } = props;

    return (
        <div className="table-wrapper">
            <table className="table table-striped table-responsive">
                <thead>
                    <tr>
                        <th>index</th>
                        {tableHeaders &&
                            tableHeaders.map((tableHeader) => (
                                <th key={tableHeader}>{tableHeader}</th>
                            ))}
                    </tr>
                </thead>
                <tbody>
                    {tableHeaders &&
                        tableRows &&
                        tableRows.map((tableRow, index) => (
                            <tr
                                key={`row-${tableRow.fid}`}
                                className="cursor-hand text-primary"
                                onClick={() => {
                                    history.push(
                                        `/${activeLayer?.name}/${tableRow.fid}/`
                                    );
                                    setActiveFeatureId(tableRow.fid);
                                }}
                            >
                                <th style={{ color: "green" }}>{index + 1}</th>
                                {tableHeaders.map((tableHeader, index) => (
                                    <th
                                        key={`row-entry-${tableRow.fid}-${index}`}
                                    >
                                        {tableRow[tableHeader]}
                                    </th>
                                ))}
                            </tr>
                        ))}
                </tbody>
            </table>
        </div>
    );
};

export default FeaturesTable;
