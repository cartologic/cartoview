import React, { useState } from 'react';
import classes from '../css/ReorderModal.module.css';
import Box from "./Box";
const ReorderModal = (props) => {
    const { apps, handleConfirm, handleToggle} = props;
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
        let apps = [];
        boxes.forEach(box => {
            apps.push(box.id);
        })
        console.log(apps);
        // here fetch reorder apps url

    }
    return (
        <div>
            <div className={classes.backdrop} onClick={handleToggle}/>
            <div className={classes.Modal}>
                <header className='header'>
                    <h4>Reorder Installed Apps</h4>
                </header>
                <div className={classes.content}>
                    {boxes.sort((a, b) => a.order - b.order)
                        .map(box =>  {
                        return <Box
                            key={box.id}
                            app={box}
                            boxNum={box.id}
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