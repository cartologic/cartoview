import React, { useContext } from 'react';
import classes from "../css/RestartLoadingModal.module.css";
import AppsContext from "../store/apps-context";




const ErrorModal = (props) => {
    const appsContext = useContext(AppsContext);

    const closeModal = () => {
        appsContext.setError(null);
    }

    return (
        <div>
            <div className={classes.backdrop} onClick={closeModal}/>
            <div className={classes.Modal}>

                <div className='alert alert-danger'>
                    <h5>{props.errorMessage}</h5>
                </div>

             </div>
        </div>
    )
};

export default ErrorModal;