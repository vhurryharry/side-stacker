import { configureStore } from '@reduxjs/toolkit'
import gameReducer from './reducers/gameSlice'

const store = configureStore({
  reducer: {
    game: gameReducer,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

export default store
