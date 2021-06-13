import React from 'react';
import classes from "../css/AvailableApps.module.css";

const AppInstance = (props) => {
    console.log('app', props.app);

    return(
        <div className={`col-md-3 col-sm-10 col-xs-12 ${classes['app-card']}`}>
                       <img
                           src="https://lh3.googleusercontent.com/0dZdu3mhvsx-UM0et0RNJ6yl4LO_JGoki9oU3kEmiaRkwcaK9bXZ8oDg4TosUMWWId-d=w250-h250-rwa"
                           alt='app logo'/>
                       <h3>{props.app.title}</h3>
                        <p>{props.app.description}</p>
                       <div className={classes.actions}>
                           <button type='button' className={`btn btn-primary`}>Explore</button>
                           <button type='button' className={`btn btn-primary`}>Create New</button>
                       </div>
                   </div>
    )
};

export default AppInstance;