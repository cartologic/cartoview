import { DocumentAttachmentsProps } from "../../types";
import { calculateAttachmentListTotalSize, formatBytes } from "../../utils";

const DocumentAttachments = (props: DocumentAttachmentsProps) => {
    const { attachmentList } = props;

    return (
        <div className="panel panel-info">
            <div className="panel-heading">
                <h4>{`Documents (${
                    attachmentList.length
                }) - Total Size (${formatBytes(
                    calculateAttachmentListTotalSize(attachmentList)
                )})`}</h4>
            </div>
            <div className="panel-body">
                <ol>
                    {attachmentList.map((singleAttachment) => (
                        <li key={`document-attachment-${singleAttachment.id}`}>
                            <a
                                target="_blank"
                                rel="noreferrer"
                                href={singleAttachment.file}
                            >
                                {singleAttachment.file.split("/").pop()}
                            </a>
                            &nbsp;({singleAttachment.created_by} -{" "}
                            {singleAttachment.created_at.split("T")[0]} -{" "}
                            {formatBytes(singleAttachment.size)})
                        </li>
                    ))}
                </ol>
            </div>
        </div>
    );
};

export default DocumentAttachments;
