import React, { useEffect, useState, useContext } from "react";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import { render } from "react-dom";
import ManageApps from "./ManageApps";
import {AppsContextProvider} from "../store/apps-context";
import AppsContext from "../store/apps-context";

let cartoview_version = null ;

const App = (props) => {
    const appsContext = useContext(AppsContext);
    const REST_URL = 'http://localhost:8000/apps/rest/app_manager/';
    const APPS_URL = 'https://appstore.cartoview.net/api/v1/app/';




    // fetch cartoview current version
    function fetchCartoviewVersion(){
        // here fetch cartoview version from backend
        // fetch('http://localhost:8000/frontend/get_version')
        // .then(response => {
        //     return response.json();
        // })
        // .then(data => {
        //     if(data) {
        //         cartoview_version = data.version;
        //         appsContext.setCartoViewCurrentVersion(data.version);
        //         //console.log('version::', version);
        //     }
        //     else{
        //         console.log('error fetching version');
        //     }
        // });

        // this is for test only

       cartoview_version = '1.31.0';
       appsContext.setCartoViewCurrentVersion(cartoview_version);

    }


    // fetch all the available apps based on cartoview version
    function fetchAvailableApps(){
        appsContext.toggleIsLoading();

        // console.log('fetching available apps');
        // first fetch cartoview current version
        fetchCartoviewVersion();
        fetch( APPS_URL )
        .then(response => {
            return response.json();
        })
        .then(data => {
            if(data) {

                const apps = data.objects.map(app => {
                    return app
                });

                // filter the apps depending on cartoview version
                const available_apps = apps.filter(app => {
                    // if app is compatible with only one version of cartoview
                   if(app.latest_version.cartoview_version.length === 1){
                       return (app.latest_version.cartoview_version[0].version === cartoview_version);
                   }

                   // check for multiple versions
                   else{
                       let versions = app.latest_version.cartoview_version;
                       for(var i = 0 ; i < versions.length; ++i){
                           if(versions[i].version && versions[i].version === cartoview_version){
                               //console.log('Found one compatible', versions[i].version);
                               return true;
                           }
                       }

                       return false;

                   }
                });

                //console.log('available: ', available_apps);
                appsContext.setAvailableApps(available_apps);
                appsContext.toggleIsLoading();
            }
            // error handling
            else{
                console.log('error fetching available apps');
            }
        });
    }


    // fetch all installed apps from the appstore
    function fetchInstalledApps () {
        // console.log('fetching installed apps');
        appsContext.toggleIsLoading();
        fetch(REST_URL + 'app', {
            method: 'GET'
        }).then(response => {
            return response.json();
        }).then(data => {
            if(data) {
                const apps = data.objects.map(app => {
                    return app
                });
                appsContext.setInstalledApps(apps);
                appsContext.toggleIsLoading();
            }
            else{
                console.log('error fetching installed apps');
            }
        });
    }

    // load data once at the first rendering
    useEffect(() => {
        //fetchCartoviewVersion();
        fetchAvailableApps();
        fetchInstalledApps();
    }, []);

    const loadingState = appsContext.isLoading;
    return (

        <div>
                {loadingState && <h2>Loading...</h2>}
                {!loadingState && <ManageApps />}
        </div>
    );
};


export default App;

const container = document.getElementById("app");
render(<AppsContextProvider><App /></AppsContextProvider>, container);

