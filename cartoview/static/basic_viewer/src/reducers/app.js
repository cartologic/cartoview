import {
    SET_APP_SETTINGS,
    UPDATE_APP_SETTINGS
} from '../actions/constants'
let appInitialState = {
    keywords: [],
    bookmarks: [],
    showLegend: true,
    geocodingKey: null,
    enableHistory: true,
    showExportMap: true,
    showLayerSwitcher: true,
    enableFeatureTable: true,
    boundlessGeoCodingEnabled: false
}
export function appSettings( state = appInitialState, action ) {
    switch ( action.type ) {
    case SET_APP_SETTINGS:
        return action.payload
    case UPDATE_APP_SETTINGS:
        return { ...state, ...action.payload }
    default:
        return state
    }
}
