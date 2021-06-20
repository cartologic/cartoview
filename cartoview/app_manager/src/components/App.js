import React, {  useState, useContext } from "react";
import { render } from "react-dom";
import ManageApps from "./ManageApps";
import {AppsContextProvider} from "../store/AppsContext";
import AppContext from "../store/AppsContext";
import ErrorModal from "./ErrorModal";
import ReorderModal from "./ReorderModal";


const App = (props) => {
    const appsContext = useContext(AppContext);
    const { error, installedApps } = appsContext;

    // local states
    const [showReorderModal, setShowReorderModal] = useState(false);

    /**
     * toggles Reorder installed apps modal
     */
    const toggleShowReorderModal = () => {
        setShowReorderModal(prevState => {return !prevState});
    }

    const loadingState = appsContext.isLoading;

    return (
        <div>
            <div className='container'>
                <div className='row manage'>
                        <button type='button' className='btn-primary btn' onClick={toggleShowReorderModal}>Reorder Installed Apps</button>
                </div>
                {showReorderModal && <ReorderModal apps={installedApps} handleToggle={toggleShowReorderModal} handleConfirm={() => {console.log('reorder')}}/>}
                {error && <ErrorModal errorMessage={error}/>}
                {loadingState && <h2>Loading...</h2>}
                {!loadingState && <ManageApps />}
            </div>
        </div>
    );
};

export default App;

const container = document.getElementById("app");
render(<AppsContextProvider><App /></AppsContextProvider>, container);

