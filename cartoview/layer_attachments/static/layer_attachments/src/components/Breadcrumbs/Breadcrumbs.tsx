import { useContext } from "react";
import { Link } from "react-router-dom";

import { Manager } from "../../context";

const Breadcrumbs = () => {
    const { activeLayer, setActiveLayer, activeFeatureId, setActiveFeatureId } =
        useContext(Manager);

    const allLayersClickHandler = () => {
        setActiveLayer(undefined);
        setActiveFeatureId("");
    };
    const activeLayerClickHandler = () => {
        setActiveFeatureId("");
    };

    return (
        <nav aria-label="breadcrumb">
            <ol className="breadcrumb">
                {!activeLayer && !activeFeatureId ? (
                    <li className="breadcrumb-item">All Layers</li>
                ) : (
                    <li className="breadcrumb-item">
                        <Link to="/" onClick={allLayersClickHandler}>
                            All Layers
                        </Link>
                    </li>
                )}
                {activeLayer && activeFeatureId ? (
                    <>
                        <li className="breadcrumb-item">
                            <Link
                                to={`/${activeLayer.name}/`}
                                onClick={activeLayerClickHandler}
                            >
                                {activeLayer.title}
                            </Link>
                        </li>
                        <li className="breadcrumb-item">{activeFeatureId}</li>
                    </>
                ) : activeLayer ? (
                    <li className="breadcrumb-item">{activeLayer.title}</li>
                ) : null}
            </ol>
        </nav>
    );
};

export default Breadcrumbs;
