import { Fragment } from "react";
import { Breadcrumbs, LayerGallery } from "../../components";

const Home = () => {
    return (
        <Fragment>
            <h2>Layer Attachments</h2>
            <Breadcrumbs />
            <LayerGallery />
        </Fragment>
    );
};

export default Home;
