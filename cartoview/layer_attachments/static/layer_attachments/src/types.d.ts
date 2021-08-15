export interface GeoJsonFeature {
    type: "Feature";
    properties: GeoJsonProperties;
}

interface GeoJson extends GeoJsonObject {
    type:
        | "Point"
        | "MultiPoint"
        | "LineString"
        | "MultiLineString"
        | "Polygon"
        | "MultiPolygon"
        | "GeometryCollection"
        | "Feature"
        | "FeatureCollection";
    features: Feature[];
}

export interface DjangoProps {
    baseURL: string;
    collectionTaskId: string;
    accessToken: string;
    appVersion: string;
}

export interface Layer {
    id: number;
    name: string;
    title: string;
    typeName: string;
    owsUrl: string;
    thumbnailUrl: string;
    date: string;
    layerAttributes: string[];
    geojson?: GeoJson;
}

export interface LayerRemoteResponse {
    id: number;
    name: string;
    title: string;
    typename: string;
    ows_url: string;
    thumbnail_url: string;
    date: string;
    layer_attributes: string[];
}

export type LayerDetailsPageParams = { layerName: string };

export type FeatureDetailsPageParams = { layerName: string; featureId: string };

export interface LayerFeatureRemoteResponse {
    properties: {
        fid: number;
    };
}

export interface LayerFeaturesRemoteResponse {
    type:
        | "Point"
        | "MultiPoint"
        | "LineString"
        | "MultiLineString"
        | "Polygon"
        | "MultiPolygon"
        | "GeometryCollection"
        | "Feature"
        | "FeatureCollection";
    features: LayerFeatureRemoteResponse[];
}

export interface Attachment {
    id: string;
    file: string;
    created_by: string;
    created_at: string;
    size: number;
}

export interface ImageAttachmentsProps {
    attachmentList: Attachment[];
}

export interface VideoAttachmentsProps {
    attachmentList: Attachment[];
}
export interface DocumentAttachmentsProps {
    attachmentList: Attachment[];
}
