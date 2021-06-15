import React, { Fragment, useContext, useState, useEffect } from 'react';
import AppWrapper from "./AppWrapper";
import AppsContext from "../store/apps-context";
import '../css/ManageApps.css';

const ManageApps = (props) => {
    // local states
    const [searchInput, setSearchInput] = useState('');
    const [buttonStatus, setButtonStatus] = useState(false);


    const appsContext = useContext(AppsContext);

    // get both installed and available apps from context
    const installedApps = appsContext.installedApps;
    const availableApps = appsContext.availableApps;

    // search input handler
    const changeHandler = (event) => {
        event.preventDefault();
        setSearchInput(event.target.value);
    }

    // toggle button status (disabled / enabled)
    const toggleButtonStatus = () => {
        setButtonStatus((prevState) => {
            return !prevState
        });
    }

    const installedAppsNames = {};
    installedApps.forEach(app => {
        installedAppsNames[app.name] = true;
    });


    // merge available and installed apps to be rendered and extract some data included in installed apps
    let currentApps = [];
    availableApps.forEach(app => {
        if(installedAppsNames[app.name]){
            app.installed = true;

            // get store_id to activate, suspend, install and uninstall apps
            app.store_id = installedApps.find(element => element.name == app.name).id;
            app.active = installedApps.find(element => element.name == app.name).active;
        }
        else {
            app.installed = false;
        }
        currentApps.push(app);
    });

    // handle search input
    if(searchInput) {
        let key = searchInput.toLowerCase();
        currentApps = currentApps.filter(app => {
            return app.title.toLowerCase().includes(key);
        });
    }

    //console.log('from manage apps');
    // console.log('available', availableApps);
    // console.log('installed', installedAppsNames);
    // console.log(currentApps);

    return (
        <Fragment>
            <div className='container'>
                <div className='row manage'>
                    <button type='button' className='btn-primary btn'>Reorder Installed Apps</button>
                </div>
                 <form className="search">
                    <input type="text" placeholder="Search For an App" name="search2"  onChange={changeHandler}/>
                    <span className='input-group-addon' >Search</span>
                </form>

                <div className='apps-container'>
                {currentApps && currentApps.map(app => {
                    return <AppWrapper key={app.id} app={app}  buttonStatus={buttonStatus} toggleButtonStatus={toggleButtonStatus}/>
                })}

                </div>
            </div>
        </Fragment>
    )
};

export default ManageApps;