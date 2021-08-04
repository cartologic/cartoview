import ReactDOM from "react-dom";
import "leaflet/dist/leaflet.css";

import { App } from "./App";
import { ManagerProvider } from "./context";

const app = (
    <ManagerProvider>
        <App />
    </ManagerProvider>
);

ReactDOM.render(app, document.getElementById("root"));
