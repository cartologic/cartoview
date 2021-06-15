import React, {Fragment, useState } from 'react';
import '../css/Modal.css';

const Modal = props => {
    const {app} = props;

    let dependencies = app.latest_version.dependencies;
    // {
    // "cartoview_attachment_manager": "1.1.8"
    // };

    dependencies = Object.keys(dependencies);
    //console.log(dependencies);

    return (
        <div>
            <div className='backdrop' onClick={props.handleToggle}/>
            <div className='Modal'>
                <header className='header'>
                    {props.flag === 'uninstalling' && <h2>Uninstall App</h2>}
                    {props.flag === 'installing' && <h2>Installing App</h2>}

                </header>
                <div className='content'>
                    {props.flag === 'uninstalling' && <div><p>This will uninstall the following app</p><h4>{app.title}</h4></div>}
                    {props.flag === 'installing' && <p>This app requires to install the flowing apps</p>}

                    {dependencies.length > 0 && dependencies.map(element =>  {return <h4 key={element}>{element}</h4>})}


                    <h5>Do You Want to proceed?</h5>
                </div>
                <footer className='actions'>
                    <button type='button' className='btn btn-primary' onClick={props.handleConfirm}>Okay</button>
                    <button type='button' className='btn btn-warning' onClick={props.handleToggle}>Cancel</button>
                </footer>
             </div>
        </div>
    )

};
export default Modal;

