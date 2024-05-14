export const User=(state=false,action)=>{
    switch(action.type){
        case 'setUser':
            return action.data
        default:
            return state
    }
}
export const setUser=(data)=>{
    return{
        type:'setUser',
        data
    }
}

export const AuthTokens=(state=false,action)=>{
    switch(action.type){
        case 'setAuthTokens':
            return action.data
        default:
            return state
    }
}
export const setAuthTokens=(data)=>{
    return{
        type:'setAuthTokens',
        data
    }
}