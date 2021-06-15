import React from 'react';
import classes from "../css/AppInstance.module.css";

const AppInstance = (props) => {
    console.log('app', props.app);

    return(
        <div className={`col-md-3 col-sm-10 col-xs-12 ${classes['app-card']}`}>
                       <img src={props.app.logo} />
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