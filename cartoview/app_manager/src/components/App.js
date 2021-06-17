import React, { useEffect, useState, useContext } from "react";
import { render } from "react-dom";
import ManageApps from "./ManageApps";
import {AppsContextProvider} from "../store/AppsContext";
import AppContext from "../store/AppsContext";
import ErrorModal from "./ErrorModal";


const App = (props) => {
    const appsContext = useContext(AppContext);
    const { error } = appsContext;

    const loadingState = appsContext.isLoading;
    return (
        <div>
            {error && <ErrorModal errorMessage={error}/>}
            {loadingState && <h2>Loading...</h2>}
            {!loadingState && <ManageApps />}
        </div>
    );
};

export default App;

const container = document.getElementById("app");
render(<AppsContextProvider><App /></AppsContextProvider>, container);

