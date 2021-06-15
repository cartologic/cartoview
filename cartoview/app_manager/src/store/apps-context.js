import React, { createContext, useState } from "react";

const AppsContext = createContext({
    isLoading: false,
    cartoviewCurrentVersion: '',
    installedApps: [],
    availableApps: [],
    setInstalledApps: (apps) => {},
    setAvailableApps: (apps) => {},
    toggleIsLoading: () => {},
    setCartoViewCurrentVersion: (version) => {}


});

export const AppsContextProvider = props => {
    const [installedApps, setInstalledApps] = useState([]);
    const [availableApps, setAvailableApps] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [cartoviewCurrentVersion, setCartoViewCurrentVersion] = useState('');

    const installedAppsHandler = (apps) => {
        setInstalledApps(apps);
    }

     const availableAppsHandler = (apps) => {
        setAvailableApps(apps);
    }

    const toggleIsLoading = () => {
        setIsLoading(prevState => !prevState);
    }

    const cartoviewVersionHandler = (version) => {
        setCartoViewCurrentVersion(version);
    }

    const contextValue = {
        isLoading,
        cartoviewCurrentVersion,
        installedApps,
        availableApps,
        setAvailableApps: availableAppsHandler,
        setInstalledApps: installedAppsHandler,
        setCartoViewCurrentVersion: cartoviewVersionHandler,
        toggleIsLoading: toggleIsLoading,
    }

    return (<AppsContext.Provider value={contextValue}>
        {props.children}
    </AppsContext.Provider>)
};

export default AppsContext;
