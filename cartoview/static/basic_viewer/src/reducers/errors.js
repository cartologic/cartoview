import {
    ADD_ERRORS,
    DELETE_ERROR,
    SET_ERRORS,
} from '../actions/constants'
let errorsInitailState = {
    errors: [],
}
export function appErrors( state = errorsInitailState, action ) {
    switch ( action.type ) {
    case ADD_ERRORS:
        return { ...state, errors: [ ...state.errors, ...action.payload ] }
    case DELETE_ERROR:
        return {
            ...state,
            errors: state.errors.filter( error => error !== action.payload )
        }
    case SET_ERRORS:
        return { ...state, errors: action.payload }
    default:
        return state
    }
}
