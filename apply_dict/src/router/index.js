/**
 * @file router 配置
 * @author wheel-w
 */

import Vue from 'vue'
import VueRouter from 'vue-router'

import store from '@/store'
import http from '@/api'
import preload from '@/common/preload'

Vue.use(VueRouter)

const MainEntry = () => import(/* webpackChunkName: 'entry' */'@/views')
const applyHome = () => import(/* webpackChunkName: 'applyHome' */'@/views/main/applyHome.vue')
const applyManagement = () => import(/* webpackChunkName: 'applyManagement' */'@/views/main/applyManagement.vue')
const NotFound = () => import(/* webpackChunkName: 'none' */'@/views/404')
const applyHistory = () => import(/* webpackChunkName: 'applyHistory' */'@/views/main/applyHistory.vue')

const routes = [
    {
        path: window.PROJECT_CONFIG.SITE_URL,
        name: 'appMain',
        component: MainEntry,
        redirect: 'applyHome',
        children: [
            {
                path: 'applyHome',
                name: 'applyHome',
                component: applyHome,
                meta: {
                    alias: '首页'
                }
            },
            {
                path: 'applyManagement',
                name: 'applyManagement',
                component: applyManagement,
                meta: {
                    alias: '申请管理'
                }
            },
            {
                path: 'applyHistory',
                name: 'applyHistory',
                component: applyHistory,
                meta: {
                    alias: '历史记录'
                }
            }
        ]
    },
    // 404
    {
        path: '*',
        name: '404',
        component: NotFound
    }
]

const router = new VueRouter({
    mode: 'history',
    routes: routes
})

const cancelRequest = async () => {
    const allRequest = http.queue.get()
    const requestQueue = allRequest.filter(request => request.cancelWhenRouteChange)
    await http.cancel(requestQueue.map(request => request.requestId))
}

let preloading = true
let canceling = true
let pageMethodExecuting = true

router.beforeEach(async (to, from, next) => {
    if (!store.state.user.userInfo.isSecretary && !store.state.user.userInfo.isLeader && to.name === 'applyManagement') {
        router.push({ name: 'applyHome' })
    }
    canceling = true
    await cancelRequest()
    canceling = false
    next()
})

router.afterEach(async (to, from) => {
    store.commit('setMainContentLoading', true)

    preloading = true
    await preload()
    preloading = false

    const pageDataMethods = []
    const routerList = to.matched
    routerList.forEach(r => {
        Object.values(r.instances).forEach(vm => {
            if (typeof vm.fetchPageData === 'function') {
                pageDataMethods.push(vm.fetchPageData())
            }
            if (typeof vm.$options.preload === 'function') {
                pageDataMethods.push(vm.$options.preload.call(vm))
            }
        })
    })

    pageMethodExecuting = true
    await Promise.all(pageDataMethods)
    pageMethodExecuting = false

    if (!preloading && !canceling && !pageMethodExecuting) {
        store.commit('setMainContentLoading', false)
    }
})

export default router
