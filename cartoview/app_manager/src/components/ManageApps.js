import React, { Fragment, useContext, useState, useEffect } from 'react';
import AppWrapper from "./AppWrapper";
import AppContext from "../store/AppsContext";
import RestartServer from "./RestartServer";
import RestartLoadingModal from "./RestartLoadingModal";
import '../css/ManageApps.css';

const ManageApps = (props) => {
    const RESTART_SERVER_URL = '../../api/app/restart-server/';

    // local states
    const [searchInput, setSearchInput] = useState('');
    const [buttonStatus, setButtonStatus] = useState(false);
    const [showRestartServer, setShowRestartServer] = useState(false);
    const [showRestartLoadingModal, setShowRestartLoadingModal] = useState(false);

    const appsContext = useContext(AppContext);


    const { installedApps, availableApps, setError} = appsContext;

    /**
     * handles search input change
     * @param event
     */
    const changeHandler = (event) => {
        event.preventDefault();
        setSearchInput(event.target.value);
    }

    /**
     * toggles the Restarting server UI state
     */
    const toggleRestartServerStatus = () => {
        setShowRestartServer(prevState => {
            return !prevState;
        })
    }

    /**
     * toggles Restart server modal UI state
     */
    const toggleRestartLoadingModal = () => {
        setShowRestartLoadingModal(prevState => {return !prevState});
    }


    /**
     * toggles Button UI state (disabled or enabled)
     */
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


    // filter available apps based on the search input
    if(searchInput) {
        let key = searchInput.toLowerCase();
        currentApps = currentApps.filter(app => {
            return app.title.toLowerCase().includes(key);
        });
    }


    /**
     * restarts the backend server then reload the app
     * @param event
     */
    const restartServer = (event) => {
        event.preventDefault();
        toggleRestartLoadingModal();
        fetch(RESTART_SERVER_URL)
        .then(response => {
            if(!response.ok){
                throw new Error('Error Restarting Server!');
            }
            return response.json()})
        .then(data => {
            if(data) {
                console.log(data);
                // reload page after server is restarted
                window.location.reload();
            }
            else{
                throw new Error('Error Restaring Server!');
            }
        })
        .catch(error => {
            toggleRestartLoadingModal();
            setError(error.message);
        })
    }

    return (
        <Fragment>
            {showRestartLoadingModal && <RestartLoadingModal />}
            <div className='container'>
                {showRestartServer && <RestartServer handleRestartButton={restartServer}/>}
                <div className='row manage'>
                    <button type='button' className='btn-primary btn'>Reorder Installed Apps</button>
                </div>
                 <form className="search">
                    <input type="text" placeholder="Search For an App" name="search2"  onChange={changeHandler}/>
                    <span className='input-group-addon' >Search</span>
                </form>

                <div className='apps-container'>
                {currentApps && currentApps.map(app => {
                    return <AppWrapper key={app.id} app={app} toggleRestartServer={toggleRestartServerStatus}  buttonStatus={buttonStatus} toggleButtonStatus={toggleButtonStatus}/>
                })}

                </div>
            </div>

        </Fragment>
    )
};

export default ManageApps;
