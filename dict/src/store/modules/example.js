/**
 * @file app store
 * @author wheel-w
 */

import http from '@/api'
import queryString from 'query-string'

export default {
    namespaced: true,
    state: {
    },
    mutations: {
    },
    actions: {
        /**
         * enterExample1 请求，get 请求
         *
         * @param {Object} context store 上下文对象 { commit, state, dispatch }
         * @param {Object} params 请求参数
         *
         * @return {Promise} promise 对象
         */
        enterExample1 (context, params, config = {}) {
            // mock 的地址，示例先使用 mock 地址
            const mockUrl = `?${AJAX_MOCK_PARAM}=index&invoke=enterExample1&${queryString.stringify(params)}`
            return http.get(mockUrl, params, config)
        },

        /**
         * enterExample2 请求, post 请求
         *
         * @param {Object} context store 上下文对象 { commit, state, dispatch }
         * @param {Object} params 请求参数
         *
         * @return {Promise} promise 对象
         */
        enterExample2 (context, params, config = {}) {
            // mock 的地址，示例先使用 mock 地址
            const mockUrl = `?${AJAX_MOCK_PARAM}=index&invoke=enterExample2&${queryString.stringify(params)}`
            return http.post(mockUrl, params, config)
        },

        /**
         * btn1 请求，get 请求
         *
         * @param {Object} context store 上下文对象 { commit, state, dispatch }
         * @param {Object} params 请求参数
         *
         * @return {Promise} promise 对象
         */
        btn1 (context, params, config = {}) {
            // mock 的地址，示例先使用 mock 地址
            const mockUrl = `?${AJAX_MOCK_PARAM}=index&invoke=btn1&${queryString.stringify(params)}`
            return http.get(mockUrl, {}, config)
        },

        /**
         * btn2 请求，post 请求
         *
         * @param {Object} context store 上下文对象 { commit, state, dispatch }
         * @param {Object} params 请求参数
         *
         * @return {Promise} promise 对象
         */
        btn2 (context, params, config = {}) {
            // mock 的地址，示例先使用 mock 地址
            const mockUrl = `?${AJAX_MOCK_PARAM}=index&invoke=btn2&${queryString.stringify(params)}`
            return http.post(mockUrl, params, config)
        },

        /**
         * del 请求，delete 请求
         *
         * @param {Object} context store 上下文对象 { commit, state, dispatch }
         * @param {Object} params 参数
         *
         * @return {Promise} promise 对象
         */
        del (context, params, config) {
            // mock 的地址，示例先使用 mock 地址
            const mockUrl = `?${AJAX_MOCK_PARAM}=index&invoke=del&${queryString.stringify(params)}`
            return http.delete(mockUrl, { data: params }, config)
        }
    }
}
