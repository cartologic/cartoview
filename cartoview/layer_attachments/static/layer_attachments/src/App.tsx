import { HashRouter as Router, Route, Switch } from "react-router-dom";

import { Home, LayerDetails, FeatureDetails } from "./pages";

export const App = () => {
    return (
        <div className="container-fluid">
            <Router>
                <Switch>
                    <Route exact path="/" component={Home} />
                    <Route exact path="/:layerName/" component={LayerDetails} />
                    <Route
                        exact
                        path="/:layerName/:featureId/"
                        component={FeatureDetails}
                    />
                </Switch>
            </Router>
        </div>
    );
};
