import {
    ADD_MAP_LAYERS,
    DELETE_MAP_LAYERS,
    SET_MAP_LAYERS,
    SET_MAP_VIEW,
    SET_WEB_MAP,
    UPDATE_MAP_VIEW,
    UPDATE_WEB_MAP
} from '../actions/constants'
let mapInitialState = {
    name: "Web Map",
    layers: [],
    view: {
        center: [ 0, 0 ],
        constrainRotation: true,
        enableRotation: true,
        rotation: 0,
        extent: undefined,
        maxZoom: 28,
        minZoom: 0,
        projection: "EPSG:3857",
        zoomFactor: 2,
        zoom: 6
    },
    renderOptions: {},
    loadTilesWhileAnimating: false,
    loadTilesWhileInteracting: false,
    moveTolerance: 1,
}
export function map( state = mapInitialState, action ) {
    switch ( action.type ) {
    case SET_WEB_MAP:
        return action.payload
    case UPDATE_MAP_VIEW:
        return { ...state, view: { ...state.view, ...action.payload } }
    case SET_MAP_VIEW:
        return { ...state, view: action.payload }
    case SET_MAP_LAYERS:
        return { ...state, layers: action.payload }
    case ADD_MAP_LAYERS:
        return { ...state, layers: [ ...state.layers, ...action.payload ] }
    case UPDATE_WEB_MAP:
        return { ...state, ...action.payload }
    case DELETE_MAP_LAYERS:
        return {
            ...state,
            layers: state.layers.filter( lyr => !action.payload.includes( lyr.id ) )
        }
    default:
        return state
    }
}
