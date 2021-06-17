import React from 'react';

const Box = (props) => {
    const {app, boxNum, handleDrag, handleDrop} = props;
    return (
        <h5
            id={boxNum}
            draggable={true}
            onDragStart={handleDrag}
            onDrop={handleDrop}
            onDragOver={(ev) => ev.preventDefault()}
        >{app.name} </h5>
    );
};
export default Box;