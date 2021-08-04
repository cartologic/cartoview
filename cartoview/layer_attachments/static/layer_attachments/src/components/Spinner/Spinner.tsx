import { useContext } from "react";
import { Manager } from "../../context";

import "./Spinner.css";

const Spinner = () => {
    const { showLoadingSpinner } = useContext(Manager);

    return showLoadingSpinner ? (
        <div className="loader pull-right"></div>
    ) : null;
};

export default Spinner;
