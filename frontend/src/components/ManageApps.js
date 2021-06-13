import React, { Fragment, useContext } from 'react';
import AppWrapper from "./AppWrapper";
import AppsContext from "../store/apps-context";
import '../css/ManageApps.css';

const ManageApps = (props) => {
    const appsContext = useContext(AppsContext);

    // get both installed and available apps from context
    const installedApps = appsContext.installedApps;
    const availableApps = appsContext.availableApps;


    const installedAppsNames = {};
    for(var i = 0 ; i < installedApps.length; ++i){
        let app = installedApps[i];
        installedAppsNames[app.name] = true;
    }

    // merge available and installed apps to be rendered and extract some data included in installed apps
    const currentApps = [];
    for(var i = 0; i < availableApps.length ;++i){
        let app = availableApps[i];
        if(installedAppsNames[app.name]){
            app.installed = true;

            // get store_id to activate, suspend, install and uninstall apps
            app.store_id = installedApps.find(element => element.name == app.name).id;
        }
        else{
            app.installed = false;
        }

        currentApps.push(app);
    }
    console.log('from manage apps');
    // console.log('available', availableApps);
    // console.log('installed', installedAppsNames);
    console.log(currentApps);


    return (
        <Fragment>

            <div className='container'>
                <div className='row manage'>
                    <button type='button' className='btn-primary btn'>Reorder Installed Apps</button>
                </div>
                 <form className="search">
                    <input type="text" placeholder="Search For an App" name="search2" />
                    <span className='input-group-addon' >Search</span>
                </form>

                <div className='apps-container'>
                {currentApps && currentApps.map(app => {
                    return <AppWrapper key={app.id} app={app} />
                })}

                </div>
            </div>
        </Fragment>
    )
};

export default ManageApps;