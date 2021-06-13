import React, {Fragment, useState } from 'react';
import Modal from './Modal';
import classes from '../css/AppWrapper.module.css';
import { csrftoken } from '../../static/js/csrf_token';

const AppWrapper = (props) => {
    const REST_URL = 'http://localhost:8000/apps/rest/app_manager/';
    const appstore_id = 1;

    const {app} = props;

    const [isActive, setIsActive] = useState(app.active);
    const [showModal, setShowModal] = useState(false);
    const [uninstalling, setUninstalling] = useState(false);

    const toggleModal = () => {
        setShowModal(prevState => !prevState);
    }

    // toggle active state of an app (active or suspended)
    const toggleActivate = () => {
        isActive ? suspendApp() : activateApp();
        setIsActive(prevState => { return !prevState});
    }

    const toggleUninstalling = () => {
        setUninstalling(preState => { return !preState});;
    }

    // suspend active app
    const suspendApp = () =>{
        fetch(  REST_URL + `app/${app.store_id}/suspend/`, {
            method: 'POST',
             headers: {
                     "Content-Type": "application/json",
              },

        })
        .then(response => {
            return response.json()
        })
        .then(data => {
            console.log(data);
        })

    }

    // activate suspended app
    const activateApp = () => {
        fetch( REST_URL + `app/${app.store_id}/activate/`, {
            method: 'POST',
             headers: {
                     "Content-Type": "application/json",
              },
        })
        .then(response => {return response.json()})
        .then(data => console.log(data))
    }

    // install app
    // Url = 'http://localhost:8000/api/app/install/'
    // payload = {apps: [{'app_name', 'version', 'store_id'}], restart: false}
    const installApp = (app_name, app_version, store_id) => {
        fetch( '../api/app/install/',{
            method: 'POST',
            headers:{
                "Accept": 'application/json',
                'Content-Type': 'application/json',
                "X_CSRFToken": csrftoken
            },
            body: JSON.stringify({
                apps:[
                    {
                        "app_name": app_name,
                        "version": app_version,
                        "store_id": store_id
                    }
                    ],
                restart: false,
            })
        })
        .then(response => {return response.json()})
        .then(data => {console.log(data)});
    }

    // uninstall app
    // url = 'http://localhost:8000/apps/uninstall/:store_id/:app_name'
    const uninstallApp = (app_name, store_id) => {
         // this url need to be updated
        fetch(`../apps/uninstall/${store_id}/${app_name}/`, {
            method: 'POST',
              headers: {
                     "Accept": 'application/json',
                     "Content-Type": "application/json",
                       "X-CSRFToken": csrftoken
              },
        })
        .then(response => {return response.json()})
        .then(data => {
            console.log(data);
            toggleUninstalling();
        });

    }

    // handleInstall
    const handleInstall = () =>{
        installApp(app.name, app.latest_version.version, appstore_id);
    }

    const handleUninstall = () => {
        toggleModal();
        toggleUninstalling();

        // get dependencies of the app to be uninstalled also
        let dependencies = app.latest_version.dependencies;
        dependencies = Object.keys(dependencies);

        // first uninstall the app
        uninstallApp(app.name, appstore_id);

        // uninstall dependencies if exist
        if(dependencies.length > 0){
            for(var i = 0 ; i < dependencies.length ; ++i){
                console.log('uninstalling ', dependencies[i]);
                uninstallApp(dependencies[i], appstore_id);
                console.log('finished uninstalling ', dependencies[i]);
            }
        }

    }

    // available app actions content
    const available = <button type='button' className='btn btn-default' onClick={handleInstall}>
                        <span className="glyphicon glyphicon-download-alt" aria-hidden="true"></span>
                        Install
                        </button> ;

    // installed apps actions content
    const installed = <>{uninstalling ?  <button type='button' className='btn btn-danger'>Loading</button>:
                 <button type='button' className='btn btn-danger' onClick={toggleModal}>
                     <span className="glyphicon glyphicon-remove" aria-hidden="true"></span>
                     Uninstall</button>

                 }
                    {isActive ?
                    <button type='button' className='btn btn-warning' onClick={toggleActivate}>
                        <span className="glyphicon glyphicon-pause" aria-hidden="true"></span>
                        Suspend</button> :
                    <button type='button' className='btn-success' onClick={toggleActivate}>
                        <span className="glyphicon glyphicon-play" aria-hidden="true"></span>
                                Activate</button>
                    }</>;

    return(
        <Fragment>
            {showModal && <Modal app={app} toggleModal={toggleModal} handleConfirm={handleUninstall}/>}
            <div className={`${classes.card} col-md-6 col-sm-12 col-xs-12`}>
                <div className={classes['app-description']}>
                    <img src={app.latest_version.logo}/>
                    <h3>{app.title}</h3>
                    {app.description.length > 150 ?  <p>{app.description.slice(0, 150) + '...'}</p> :
                     <p>{app.description}</p>
                    }

                </div>

                <div className={classes['app-actions']}>
                    {app.installed ? installed: available}
                </div>

                <div className={classes['app-info']}>
                    <ul>
                        <li><b>Rating: </b> <span> {app.stars} / 5</span></li>
                        <li><b>Latest version: </b> <span>V {app.latest_version.version}</span></li>
                        <li><b>Installed Version:</b> <span>V {app.installed ? app.latest_version.version:''}</span></li>
                        <li><b>Installation:</b>{app.downloads}</li>
                        <li><b>By: </b>{app.author}</li>
                    </ul>
                </div>
            </div>
        </Fragment>
    )
};

export default AppWrapper;


