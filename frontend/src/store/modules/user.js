import http from '@/api'

const state = {
    userInfo: {}
}

const getters = {
}

const actions = {
    /**
         * 获取用户信息
         *
         * @param {Object} context store 上下文对象 { commit, state, dispatch }
         *
         * @return {Promise} promise 对象
         */
    userInfo (context, config = {}) {
        return http.get(USER_INFO_URL, {}, config).then(response => {
            const userData = response.data || {}
            context.commit('setUserInfo', userData)
            return userData
        })
    }
}

const mutations = {
    /**
         * 更新当前用户 user
         *
         * @param {Object} state store state
         * @param {Object} user user 对象
         */
    setUserInfo (state, userInfo) {
        userInfo.isAdmin = userInfo.isScretary
        state.userInfo = userInfo
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
