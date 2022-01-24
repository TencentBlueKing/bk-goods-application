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
const PurchaseHome = () => import(/* webpackChunkName: 'purchaseHome' */'@/views/purchaseHome')
const ItemManagement = () => import(/* webpackChunkName: 'itemManagement' */'@/views/itemManagement')
const ItemDetail = () => import(/* webpackChunkName: 'itemDetail' */'@/views/itemDetail')
const NotFound = () => import(/* webpackChunkName: 'none' */'@/views/404')
const ShoppingCart = () => import(/* webpackChunkName: 'shoppingCart' */'@/views/shoppingCart')
const personalGoods = () => import(/* webpackChunkName: 'personalGoods' */'@/views/personalGoods/personalGoods.vue')
const returnGoods = () => import(/* webpackChunkName: 'returnGoods' */'@/views/returnGoods/returnGoods.vue')

const routes = [
    {
        path: window.PROJECT_CONFIG.SITE_URL,
        name: 'appMain',
        component: MainEntry,
        alias: '',
        children: [
            {
                path: 'purchaseHome',
                alias: '',
                name: 'purchaseHome',
                component: PurchaseHome
            },
            {
                path: 'itemManagement',
                name: 'itemManagement',
                component: ItemManagement
            },
            {
                path: 'itemDetail',
                name: 'itemDetail',
                component: ItemDetail
            },
            {
                path: 'shoppingCart',
                name: 'shoppingCart',
                component: ShoppingCart
            },
            {
                path: 'personalGoods',
                name: 'personalGoods',
                component: personalGoods
            },
            {
                path: 'returnGoods',
                name: 'returnGoods',
                component: returnGoods
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
