import React, { useState, useContext } from 'react';
import classes from '../css/ReorderModal.module.css';
import Box from "./Box";
import { csrftoken } from '../../static/app_manager/js/csrf_token';
import AppsContext from "../store/AppsContext";

const ReorderModal = (props) => {
    const appsContext = useContext(AppsContext);

    const { apps, handleConfirm, handleToggle} = props;
    const { setError } = appsContext;

    // local states
    const [dragId, setDragId] = useState();
    const [boxes, setBoxes] = useState(apps);

    /**
     * handles Drag app
     * @param event
     */
    const handleDrag = (event) => {
        setDragId(event.currentTarget.id);
    }

    /**
     * handles Drop app (swap orders of apps)
     * @param event
     */
    const handleDrop = (event) => {
        const dragBox = boxes.find((box) => box.id == dragId);
        const dropBox = boxes.find((box) => box.id == event.currentTarget.id);
        const dragBoxOrder = dragBox.order;
        const dropBoxOrder = dropBox.order;

        const newBoxState = boxes.map((box) => {
          if (box.id == dragId) {
            box.order = dropBoxOrder;
          }
          if (box.id == event.currentTarget.id) {
            box.order = dragBoxOrder;
          }

          return box;
        });
        setBoxes(newBoxState);
    }

    /**
     * Reorders apps from the backend
     * payload: array contains apps ids
     */
    const reorderApps = () => {
        const reorderURL = '../rest/app_manager/app/reorder/';
        const appsIds = apps.map( app => {return app.id});
        //console.log(apps);
        // here fetch reorder apps url
        fetch(reorderURL, {
            method: 'POST',
            headers: {
                "Accept": 'application/json',
                'Content-Type': 'application/json',
                "X_CSRFToken": csrftoken
            },
            body: JSON.stringify({
                apps: appsIds
            })
        })
        .then(response => {
            if(!response.ok){
                throw new Error('Error Reordering installed apps');
            }
            else{
                return response.json();
            }
        })
        .then(data => {
            if(data){
                console.log(data);
                handleToggle();
            }
            else{
                throw new Error('Error Reordering installed apps');
            }
        })
        .catch(error => {
            setError(error.message);
        });

    }

    return (
        <div>
            <div className={classes.backdrop} onClick={handleToggle}/>
            <div className={classes.Modal}>
                <header className='header'>
                    <h4>Reorder Installed Apps</h4>
                </header>
                <div className={classes.content}>
                    {apps.sort((a, b) => a.order - b.order)
                        .map(app =>  {
                        return <Box
                            key={app.id}
                            app={app}
                            boxNum={app.id}
                            handleDrag={handleDrag}
                            handleDrop={handleDrop}
                        />}
                    )}
                </div>
                <footer className={classes.actions}>
                    <button type='button' className='btn btn-primary' onClick={reorderApps}>Save Order</button>
                    <button type='button' className='btn btn-warning' onClick={handleToggle}>Cancel</button>
                </footer>
             </div>
        </div>
    );
};

export default ReorderModal;