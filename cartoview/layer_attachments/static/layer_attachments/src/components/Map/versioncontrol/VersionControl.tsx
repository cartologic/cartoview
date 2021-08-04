import { DjangoProps } from "../../../types";

declare const djangoProps: DjangoProps;

const VerionControl = () => {
    return (
        <div className="leaflet-bottom leaflet-left">
            <div className="leaflet-control-attribution leaflet-control">
                Version - {djangoProps.appVersion}
            </div>
        </div>
    );
};

export default VerionControl;
