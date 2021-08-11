import axios from "axios";
import { useState, useEffect, useContext } from "react";
import { Manager } from "../../context";
import { DjangoProps } from "../../types";
import { calculateAttachmentListTotalSize, formatBytes } from "../../utils";

declare const djangoProps: DjangoProps;

const DownloadAttachments = () => {
    const { activeLayer } = useContext(Manager);
    const [showLoading, setShowLoading] = useState(false);
    const [totalAttachmentsCount, setTotalAttachmentsCount] = useState(0);
    const [totalAttachmentsSize, setTotalAttachmentsSize] = useState("");

    useEffect(() => {
        const fetchData = async () => {
            if (activeLayer) {
                setShowLoading(true);
                axios.defaults.baseURL = djangoProps.baseURL;
                const collectionRecordAttachmentsResponse = await axios.get(
                    `api/layer_attachments/attachments/`,
                    {
                        params: {
                            layer__name: activeLayer.name,
                        },
                    }
                );
                setTotalAttachmentsCount(
                    collectionRecordAttachmentsResponse.data.length
                );
                setTotalAttachmentsSize(
                    formatBytes(
                        calculateAttachmentListTotalSize(
                            collectionRecordAttachmentsResponse.data
                        )
                    )
                );
                setShowLoading(false);
            }
        };
        fetchData();
    }, [activeLayer]);

    return (
        <div className="panel panel-info gallery-container">
            <div className="panel-heading">
                <h4 className="attachment-title">
                    Attachments ({totalAttachmentsCount}) - Size (
                    {totalAttachmentsSize})
                </h4>
                {showLoading && (
                    <div className="loader attachment-title pull-right"></div>
                )}
                {showLoading === false && totalAttachmentsCount > 0 && (
                    <a
                        href={`${djangoProps.baseURL}api/layer_attachments/download/?layer_name=${activeLayer?.name}`}
                        target="_blank"
                        rel="noreferrer"
                        className="btn btn-primary pull-right"
                    >
                        <span className="glyphicon glyphicon-cloud-download"></span>
                        &nbsp;Download
                    </a>
                )}
            </div>
        </div>
    );
};

export default DownloadAttachments;
