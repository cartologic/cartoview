/* eslint-disable eslint-comments/disable-enable-pair */
/* eslint-disable @typescript-eslint/no-empty-function */
import React from "react";

import { Layer } from "../../types";

interface Context {
    showLoadingSpinner: boolean;
    availableLayers: Layer[];
    activeLayer: Layer | undefined;
    setActiveLayer: (activeLayer: Layer | undefined) => void;
    activeFeatureId: string;
    setActiveFeatureId: (activeFeatureId: string) => void;
    setShowLoadingSpinner: (showLoadingSpinner: boolean) => void;
}

const Manager = React.createContext<Context>({
    showLoadingSpinner: false,
    activeLayer: undefined,
    availableLayers: [],
    setActiveLayer: () => {},
    activeFeatureId: "",
    setActiveFeatureId: () => {},
    setShowLoadingSpinner: () => {},
});

export default Manager;
