import React from 'react';
import classes from "../css/RestartLoadingModal.module.css";

const ErrorModal = (props) => {
    return (
        <div>
            <div className={classes.backdrop} onClick={props.handleToggle}/>
            <div className={classes.Modal}>

                <div className='alert alert-danger'>
                    <h2>{props.errorMessage}</h2>
                </div>

             </div>
        </div>
    )
};

export default ErrorModal;