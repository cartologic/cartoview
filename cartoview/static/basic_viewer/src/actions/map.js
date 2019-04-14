import {
    ADD_MAP_LAYERS,
    DELETE_MAP_LAYERS,
    SET_MAP_LAYERS,
    SET_MAP_VIEW,
    SET_WEB_MAP,
    UPDATE_MAP_VIEW,
    UPDATE_WEB_MAP
} from './constants'
export function setWebMapAction( map ) {
    return {
        type: SET_WEB_MAP,
        payload: map
    }
}
export function updateWebMapAction( map ) {
    return {
        type: UPDATE_WEB_MAP,
        payload: map
    }
}
export function setMapViewAction( view ) {
    return {
        type: SET_MAP_VIEW,
        payload: view
    }
}
export function updateMapViewAction( view ) {
    return {
        type: UPDATE_MAP_VIEW,
        payload: view
    }
}
export function setMapLayersAction( layers ) {
    return {
        type: SET_MAP_LAYERS,
        payload: layers
    }
}
export function addMapLayersAction( layers ) {
    return {
        type: ADD_MAP_LAYERS,
        payload: layers
    }
}
export function deleteMapLayers( layerIDS ) {
    return {
        type: DELETE_MAP_LAYERS,
        payload: layerIDS
    }
}
