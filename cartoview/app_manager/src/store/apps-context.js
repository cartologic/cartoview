import React, { createContext, useState } from "react";

const AppsContext = createContext({
    isLoading: false,
    cartoviewCurrentVersion: '',
    installedApps: [],
    availableApps: [],
    error: null,
    setInstalledApps: (apps) => {},
    setAvailableApps: (apps) => {},
    toggleIsLoading: () => {},
    setCartoViewCurrentVersion: (version) => {},
    setError: (message) => {}

});

export const AppsContextProvider = props => {
    const [installedApps, setInstalledApps] = useState([]);
    const [availableApps, setAvailableApps] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [cartoviewCurrentVersion, setCartoViewCurrentVersion] = useState('');
    const [error, setError] = useState('error');


    const errorHandler = (message) => {
        setError(message);
    }
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
        error,
        setAvailableApps: availableAppsHandler,
        setInstalledApps: installedAppsHandler,
        setCartoViewCurrentVersion: cartoviewVersionHandler,
        toggleIsLoading: toggleIsLoading,
        setError: errorHandler,
    }

    return (<AppsContext.Provider value={contextValue}>
        {props.children}
    </AppsContext.Provider>)
};

export default AppsContext;
