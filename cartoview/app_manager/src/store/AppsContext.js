import React, { createContext, useState, useEffect } from "react";
import { appsURL } from "../config";

const restURL = '../rest/app_manager/app/';

/**
 * React Context for global States
 */
const AppsContext = createContext({
  isLoading: false,
  cartoviewCurrentVersion: '',
  installedApps: [],
  availableApps: [],
  error: null,
  setInstalledApps: (apps) => { },
  setAvailableApps: (apps) => { },
  toggleIsLoading: () => { },
  setCartoViewCurrentVersion: (version) => { },
  setError: (message) => { }

});

/**
 * fetches the cartoview version from the backend .....
 * @returns string
 */
function fetchCartoviewVersion() {
  // required to get the cartoview version from backend
  // this is for test only
  const cartoviewVersion = '1.31.0';
  return cartoviewVersion;
};


export const AppsContextProvider = props => {
  const [installedApps, setInstalledApps] = useState([]);
  const [availableApps, setAvailableApps] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [cartoviewCurrentVersion, setCartoViewCurrentVersion] = useState('');
  const [error, setError] = useState(null);

  /**
   * fetches installed apps from the appstore
   * @returns array contains installed apps
   */
  function fetchInstalledApps() {
    // console.log('fetching installed apps');
    let installedApps = [];
    toggleIsLoading();
    fetch(restURL, {
      method: 'GET'
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Error Fetching installed apps!');
        }
        else {
          return response.json();
        }
      })
      .then(data => {
        if (data) {
          data.objects.map(app => {
            installedApps.push(app);
          });
          toggleIsLoading();
        }
        else {
          throw new Error('Error fetching installed apps');
        }
      })
      .catch(error => {
        //console.log('catch error here', error);
        toggleIsLoading();
        setError(error.message);
      })
    return installedApps;
    ;
  }


  /**
   * fetches available apps from apps api and set it to context
   */
  function fetchAvailableApps() {
    const version = fetchCartoviewVersion();
    setCartoViewCurrentVersion(version);

    toggleIsLoading();
    // console.log('fetching available apps');
    fetch(appsURL)
      .then(response => {
        if (!response.ok) {
          throw new Error('Error fetching Available apps!');
        }
        return response.json();
      })
      .then(data => {
        if (data) {
          const apps = data.objects.map(app => {
            return app;
          });

          // filter the apps depending on cartoview version
          const filteredApps = apps.filter(app => {
            // if app is compatible with only one version of cartoview
            if (app.latest_version.cartoview_version.length === 1) {
              return (app.latest_version.cartoview_version[0].version === version);
            }

            // check for multiple versions
            else {
              let versions = app.latest_version.cartoview_version;
              for (var i = 0; i < versions.length; ++i) {
                if (versions[i].version && versions[i].version === version) {
                  //console.log('Found one compatible', versions[i].version);
                  return true;
                }
              }
              return false;
            }
          });
          toggleIsLoading();
          //console.log('filtered', filteredApps);
          setAvailableApps(filteredApps);
        }
        // error handling
        else {
          throw new Error('Error fetching available apps');
        }
      })
      .catch(error => {
        toggleIsLoading();
        setError(error.message);
      })
    ;

  }

  /**
   * sets Error Message in the context
   * @param message
   */
  const errorHandler = (message) => {
    setError(message);
  }

  /**
   * calls fetchInstalledApps() and set installed apps in the context
   */
  const installedAppsHandler = () => {
    const installedApps = fetchInstalledApps();
    setInstalledApps(installedApps);
  }


  /**
   * toggles loading state
   */
  const toggleIsLoading = () => {
    setIsLoading(prevState => !prevState);
  }

  /**
   * calls fetchCartoViewVersion() ans set version in the context
   */
  const cartoviewVersionHandler = () => {
    const version = fetchCartoviewVersion();
    setCartoViewCurrentVersion(version);
  }


  const contextValue = {
    isLoading,
    cartoviewCurrentVersion,
    installedApps,
    availableApps,
    error,
    toggleIsLoading: toggleIsLoading,
    setError: errorHandler,
  }

  useEffect(() => {
    installedAppsHandler();
    fetchAvailableApps();
  }, []);

  return (<AppsContext.Provider value={contextValue}>
    {props.children}
  </AppsContext.Provider>)
};

export default AppsContext;
