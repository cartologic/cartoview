import { configureStore } from './configureStore'
export const store = configureStore()
export function storeWithInitial( initialState ) {
    return configureStore( initialState )
}
export default store