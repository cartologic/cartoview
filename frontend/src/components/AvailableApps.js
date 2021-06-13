import React, {Fragment, useContext} from 'react';
import AppsContext from "../store/apps-context";
import { Link } from 'react-router-dom';
import classes from '../css/AvailableApps.module.css';
import AppInstance from "./AppInstance";

const AvailableApps = (props) => {
    const appsContext = useContext(AppsContext);
    const loadingState = appsContext.isLoading;
    const installedApps = appsContext.installedApps;

    const activeInstalledApps = installedApps.filter(app =>  app.active === true)
    //console.log('active apps',activeInstalledApps);


    return (
       <Fragment>
           <div className='container'>
               <div className='row header'>
                    <div className='col-md-9 col-sm-7 col-xs-12'>
                        <h2>Explore Apps</h2>
                    </div>
                   <div className={`${classes['manage-btn']} col-md-3 col-sm-5 col-xs-12`}>
                       <Link to='/frontend/manage'>
                            <button type='button' className={` btn-primary btn`}>Manage Apps</button>
                       </Link>
                   </div>
               </div>

               <div className={`row ${classes.content}`}>
                   {loadingState && <h2>Loading...</h2>}
                   {installedApps.length === 0 && <h2>No Installed Apps</h2>}

                   {!loadingState && installedApps.length > 0 &&
                    activeInstalledApps.map(app => {return <AppInstance key={app.id} app={app}/>})
                   }
               </div>

           </div>
       </Fragment>
    );
};

export default AvailableApps;
