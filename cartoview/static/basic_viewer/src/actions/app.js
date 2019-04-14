import {
    SET_APP_SETTINGS,
    UPDATE_APP_SETTINGS
} from './constants'
export function setAppSettingsAction( settings ) {
    return {
        type: SET_APP_SETTINGS,
        payload: settings
    }
}
export function updateAppSettingsAction( settings ) {
    return {
        type: UPDATE_APP_SETTINGS,
        payload: settings
    }
}
