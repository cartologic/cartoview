import React from 'react';
import classes from '../css/RestartServer.module.css';
const RestartServer = (props) => {
    return(
        <div className={`row alert alert-info ${classes['restart-server']}`}>
                    <h4><span className="fa fa-exclamation"></span>Server restart is required</h4>
                    <p>
                        In order to have the effect of the recently installed apps please restart the server.
                    </p>
                    <p>
                        Please notice:
                    </p>
                    <ol>
                        <li>This may take several minutes</li>
                        <li>The server will drop all the connections and tasks during the restart</li>
                        <li>Ask the administrator to restart GeoNode Service if the app does not appear in the installed
                            apps
                        </li>
                    </ol>
                    <button className="btn btn-default manager-actions-btn" onClick={props.handleRestartButton}>
                        <span className="glyphicon glyphicon-repeat" aria-hidden="true"></span>
                        Restart Server
                    </button>
                </div>
    );
};

export default RestartServer;

