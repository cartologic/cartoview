import React from "react";
import classes from '../css/RestartLoadingModal.module.css';
const RestartLoadingModal = (props) => {
    return(
      <div>
        <div className={classes.backdrop} />
        <div className={classes.Modal}>

            <div className='alert alert-danger'>
                <i className={`fa fa-refresh ${classes.rotating}`}></i> Restarting Server, Please Wait...
            </div>

         </div>
    </div>
    );
};

export default RestartLoadingModal;

