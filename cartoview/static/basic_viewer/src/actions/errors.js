import {
    ADD_ERRORS,
    DELETE_ERROR,
    SET_ERRORS
} from './constants'
export function setErrors( errors ) {
    return {
        type: SET_ERRORS,
        payload: errors
    }
}
export function deleteError( error ) {
    return {
        type: DELETE_ERROR,
        payload: error
    }
}
export function addError( errors ) {
    return {
        type: ADD_ERRORS,
        payload: errors
    }
}
