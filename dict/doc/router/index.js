/**
 * @file router 配置
 * @author wheel-w
 */

import Vue from 'vue'
import VueRouter from 'vue-router'

import introRoutes from '@doc/router/intro'

Vue.use(VueRouter)

const NotFound = () => import(/* webpackChunkName: 'none' */'@/views/404')

const routes = introRoutes.concat({
    path: '*',
    name: '404',
    component: NotFound
})

const router = new VueRouter({
    routes: routes
})

router.beforeEach(async (to, from, next) => {
    next()
})

router.afterEach(async (to, from) => {
})

export default router
