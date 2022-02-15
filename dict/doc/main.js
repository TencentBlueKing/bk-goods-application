/**
 * @file doc entry
 * @author wheel-w
 */

import Vue from 'vue'

import Exception from '@/components/exception'
import '@/common/bkmagic'

import anchorMixin from '@doc/mixins/mixin-anchor'
import Intro from '@doc/Intro'
import router from '@doc/router'
import Header from '@doc/components/header'
import Footer from '@doc/components/footer'
import SideNav from '@doc/components/side-nav.vue'

Vue.component('app-exception', Exception)
Vue.component('app-header', Header)
Vue.component('app-footer', Footer)
Vue.component('side-nav', SideNav)

global.mainComponent = new Vue({
    el: '#app',
    router,
    components: { Intro },
    mixins: [anchorMixin],
    template: '<Intro />'
})
