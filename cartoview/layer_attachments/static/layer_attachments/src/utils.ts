import { Attachment } from "./types";

/**
 * format byte count into human readable format
 * @param bytes number of bytes to format
 * @param decimals base of formatting (default 2)
 * @returns humand readable format
 */
export const formatBytes = (bytes = 0, decimals = 2) => {
    if (bytes === 0) return "0 Bytes";

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
};

/**
 * calculate the total size of an array of attachments
 * @param attachmentList the array of attachments
 * @returns the total size in human readable format
 */
export const calculateAttachmentListTotalSize = (
    attachmentList: Attachment[]
) => {
    let result = 0;
    attachmentList.forEach(
        (singleAttachment) => (result += singleAttachment.size)
    );
    return result;
};
