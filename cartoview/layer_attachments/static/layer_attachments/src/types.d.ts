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

export interface FeaturesTableProps {
    tableHeaders: string[] | undefined;
    tableRows: any[];
}

export interface LayerFeatureRemoteResponse {
    properties: {
        fid: number;
    };
}

export interface LayerFeaturesRemoteResponse {
    features: LayerFeatureRemoteResponse[];
}
