import { VideoAttachmentsProps } from "../../types";
import { calculateAttachmentListTotalSize, formatBytes } from "../../utils";

const VideoAttachments = (props: VideoAttachmentsProps) => {
    const { attachmentList } = props;

    return (
        <div className="panel panel-info">
            <div className="panel-heading">
                <h4>{`Videos (${
                    attachmentList.length
                }) - Total Size (${formatBytes(
                    calculateAttachmentListTotalSize(attachmentList)
                )})`}</h4>
            </div>
            <div className="panel-body">
                <div className="row">
                    {attachmentList.map((singleAttachment) => (
                        <div
                            key={`video-attachment-${singleAttachment.id}`}
                            className="col-md-6"
                        >
                            <div className="thumbnail">
                                <a
                                    target="_blank"
                                    rel="noreferrer"
                                    href={singleAttachment.file}
                                >
                                    <video
                                        className="attachment-video"
                                        src={singleAttachment.file}
                                        controls
                                    >
                                        <track kind="captions" />
                                    </video>
                                </a>
                                <span className="label label-info credits-user">
                                    <span className="glyphicon glyphicon-user"></span>{" "}
                                    {singleAttachment.created_by}
                                </span>
                                <span className="label label-info credits-date">
                                    <span className="glyphicon glyphicon-calendar"></span>{" "}
                                    {singleAttachment.created_at.split("T")[0]}
                                </span>
                                <span className="label label-info credits-size">
                                    {formatBytes(singleAttachment.size)}
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default VideoAttachments;
