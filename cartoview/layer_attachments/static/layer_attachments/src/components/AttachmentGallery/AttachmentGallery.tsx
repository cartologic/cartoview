import { useContext, useEffect, useState } from "react";
import axios from "axios";

import { DjangoProps, Attachment } from "../../types";
import "./AttachmentGallery.css";
import ImageAttachments from "./ImageAttachments";
import VideoAttachments from "./VideoAttachments";
import DocumentAttachments from "./DocumentAttachments";
import { calculateAttachmentListTotalSize, formatBytes } from "../../utils";
import { Manager } from "../../context";

declare const djangoProps: DjangoProps;

const AttachmentGallery = () => {
    const { activeLayer, activeFeatureId } = useContext(Manager);
    const [showLoading, setShowLoading] = useState(false);
    const [imageAttachmentList, setImageAttachmentList] = useState<
        Attachment[]
    >([]);
    const [videoAttachmentList, setVideoAttachmentList] = useState<
        Attachment[]
    >([]);
    const [documentAttachmentList, setDocumentAttachmentList] = useState<
        Attachment[]
    >([]);

    useEffect(() => {
        const imageAttachmentExtensions = ["jpg", "jpeg", "png"];
        const videoAttachmentExtensions = ["mp4", "mov"];
        const documentAttachmentExtensions = ["doc", "docx", "pdf"];

        const fetchData = async () => {
            if (activeLayer && activeFeatureId) {
                setShowLoading(true);
                axios.defaults.baseURL = djangoProps.baseURL;
                const attachmentsResponse = await axios.get(
                    `api/layer_attachments/attachments/`,
                    {
                        params: {
                            layer__name: activeLayer.name,
                            feature_id: activeFeatureId,
                        },
                    }
                );
                const tempImageAttachmentList: Attachment[] = [];
                const tempVideoAttachmentList: Attachment[] = [];
                const tempDocumentAttachmentList: Attachment[] = [];
                attachmentsResponse.data.forEach(
                    (singleAttachment: Attachment) => {
                        const extension =
                            singleAttachment.file.split(".").pop() || "";
                        if (imageAttachmentExtensions.includes(extension)) {
                            tempImageAttachmentList.push(singleAttachment);
                        } else if (
                            videoAttachmentExtensions.includes(extension)
                        ) {
                            tempVideoAttachmentList.push(singleAttachment);
                        } else if (
                            documentAttachmentExtensions.includes(extension)
                        ) {
                            tempDocumentAttachmentList.push(singleAttachment);
                        }
                    }
                );
                setImageAttachmentList(tempImageAttachmentList);
                setVideoAttachmentList(tempVideoAttachmentList);
                setDocumentAttachmentList(tempDocumentAttachmentList);
                setShowLoading(false);
            }
        };
        fetchData();
    }, [activeFeatureId, activeLayer]);

    /**
     * Count the number of total attachments (image - video - document)
     * @returns the total number of attachments
     */
    const countTotalAttachments = () => {
        return (
            imageAttachmentList.length +
            videoAttachmentList.length +
            documentAttachmentList.length
        );
    };

    /**
     * Calculate the total size of all attachments (image - video - document)
     * @returns the total size in humand readable format
     */
    const sizeTotalAttachments = () => {
        const imagesSize =
            calculateAttachmentListTotalSize(imageAttachmentList);
        const videosSize =
            calculateAttachmentListTotalSize(videoAttachmentList);
        const documentsSize = calculateAttachmentListTotalSize(
            documentAttachmentList
        );
        return formatBytes(imagesSize + videosSize + documentsSize);
    };

    return (
        <div className="gallery-container">
            <div className="panel panel-info">
                <div className="panel-heading">
                    <h4 className="attachment-title">
                        Attachments ({countTotalAttachments()}) - Size (
                        {sizeTotalAttachments()})
                    </h4>
                    {showLoading && (
                        <div className="loader attachment-title pull-right"></div>
                    )}
                    {showLoading === false &&
                        (imageAttachmentList.length > 0 ||
                            videoAttachmentList.length > 0 ||
                            documentAttachmentList.length > 0) && (
                            <a
                                href={`${djangoProps.baseURL}api/layer_attachments/download/?layer_name=${activeLayer?.name}&feature_id=${activeFeatureId}`}
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
            {imageAttachmentList.length !== 0 && (
                <ImageAttachments attachmentList={imageAttachmentList} />
            )}
            {videoAttachmentList.length !== 0 && (
                <VideoAttachments attachmentList={videoAttachmentList} />
            )}
            {documentAttachmentList.length !== 0 && (
                <DocumentAttachments attachmentList={documentAttachmentList} />
            )}
        </div>
    );
};

export default AttachmentGallery;
