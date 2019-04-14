import {
    appErrors,
} from './errors'
import {
    appSettings,
} from './app'
import { combineReducers } from 'redux'
import {
    map,
} from './map'
export default combineReducers( {
    map,
    appSettings,
    appErrors,
} )
