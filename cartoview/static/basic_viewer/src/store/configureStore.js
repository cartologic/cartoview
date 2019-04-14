import { applyMiddleware, createStore } from 'redux'

import ReduxThunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension';
import rootReducer from '../reducers'
export function configureStore( initialState ) {
    return createStore( rootReducer, initialState, composeWithDevTools(
        applyMiddleware( ReduxThunk ) ) )
}
