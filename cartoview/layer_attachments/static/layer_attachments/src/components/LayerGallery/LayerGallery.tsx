import { useContext } from "react";
import { Link } from "react-router-dom";

import { Manager } from "../../context";
import "./LayerGallery.css";

const LayerGallery = () => {
    const { availableLayers } = useContext(Manager);

    return (
        <div className="layer-gallery panel panel-default">
            <div className="panel-body">
                <div className="row">
                    {availableLayers.map((layer) => (
                        <div key={`layer-${layer.id}`} className="col-md-3">
                            <div className="thumbnail">
                                <Link to={`/${layer.name}/`}>
                                    <img
                                        className="layer-img"
                                        src={layer.thumbnailUrl}
                                        alt="Layer"
                                    />
                                </Link>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default LayerGallery;
