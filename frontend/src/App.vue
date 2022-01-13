<template>
    <div class="monitor-navigation" :class="systemCls">
        <bk-navigation
            :header-title="nav.id"
            :side-title="nav.title"
            :default-open="true"
            :navigation-type="'top-bottom'"
            :need-menu="false"
            @toggle="handleToggle">
            <template slot="header">
                <div class="monitor-navigation-header">
                    <ol class="header-nav">
                        <div v-for="(item,index) in header.list" :key="item.id" theme="light navigation-message" :arrow="false" offset="0, -5" placement="bottom">
                            <router-link :to="item.path">
                                <li v-show="item.show" class="header-nav-item"
                                    :class="{ 'item-active': index === header.active }"
                                    @click="header.active = (item.id - 1)">
                                    {{item.name}}
                                </li>
                            </router-link>
                        </div>
                    </ol>
                    <bk-popover theme="light navigation-message" :arrow="false" offset="-20, 10" placement="bottom-start" :tippy-options="{ 'hideOnClick': false }">
                        <div class="header-user">
                            admin
                            <i class="bk-icon icon-down-shape"></i>
                        </div>
                        <template slot="content">
                            <ul class="monitor-navigation-admin">
                                <li class="nav-item" v-for="userItem in user.list" :key="userItem">
                                    {{userItem}}
                                </li>
                            </ul>
                        </template>
                    </bk-popover>
                </div>
            </template>
            <div v-if="header.active === 0" class="toCarTab" @click="toShoppingCar">
                <svg t="1641539862015" class="icon" viewBox="0 0 1028 1024" version="1.1" p-id="2153" width="40" height="40">
                    <path d="M332.8 790.528q19.456 0 36.864 7.168t30.208 19.968 20.48 30.208 7.68 36.864-7.68 36.864-20.48 30.208-30.208 20.48-36.864 7.68q-20.48 0-37.888-7.68t-30.208-20.48-20.48-30.208-7.68-36.864 7.68-36.864 20.48-30.208 30.208-19.968 37.888-7.168zM758.784 792.576q19.456 0 37.376 7.168t30.72 19.968 20.48 30.208 7.68 36.864-7.68 36.864-20.48 30.208-30.72 20.48-37.376 7.68-36.864-7.68-30.208-20.48-20.48-30.208-7.68-36.864 7.68-36.864 20.48-30.208 30.208-19.968 36.864-7.168zM930.816 210.944q28.672 0 44.544 7.68t22.528 18.944 6.144 24.064-3.584 22.016-13.312 37.888-22.016 62.976-23.552 68.096-18.944 53.248q-13.312 40.96-33.28 56.832t-49.664 15.872l-35.84 0-65.536 0-86.016 0-96.256 0-253.952 0 14.336 92.16 517.12 0q49.152 0 49.152 41.984 0 20.48-9.728 35.84t-38.4 14.336l-49.152 0-94.208 0-118.784 0-119.808 0-99.328 0-55.296 0q-20.48 0-34.304-9.216t-23.04-24.064-14.848-32.256-8.704-32.768q-1.024-6.144-5.632-29.696t-11.264-58.88-14.848-78.848-16.384-87.552q-19.456-103.424-44.032-230.4l-76.8 0q-15.36 0-25.6-7.68t-16.896-18.432-9.216-23.04-2.56-22.528q0-20.48 13.824-33.792t37.376-12.288l103.424 0q20.48 0 32.768 6.144t19.456 15.36 10.24 18.944 5.12 16.896q2.048 8.192 4.096 23.04t4.096 30.208q3.072 18.432 6.144 38.912l700.416 0zM892.928 302.08l-641.024-2.048 35.84 185.344 535.552 1.024z" p-id="2154" fill="#bfbfbf">
                    </path>
                </svg>
            </div>
            <div class="monitor-navigation-content">
                <main class="main-content" v-bkloading="{ isLoading: mainContentLoading, opacity: 1 }">
                    <router-view :key="routerKey" v-show="!mainContentLoading" />
                </main>
            </div>
            <template slot="footer">
                <div class="monitor-navigation-footer">
                    Copyright © 2012-{{new Date().getFullYear()}} Tencent BlueKing. All Rights Reserved. 腾讯蓝鲸 版权所有
                </div>
            </template>
        </bk-navigation>
        <app-auth ref="bkAuth"></app-auth>
    </div>
</template>

<script>
    import { mapGetters } from 'vuex'

    import { bus } from '@/common/bus'

    export default {
        name: 'monitor-navigation',

        data () {
            return {
                routerKey: +new Date(),
                systemCls: 'mac',
                nav: {
                    list: [
                        {
                            id: 'home',
                            name: '首页',
                            icon: 'icon-tree-application-shape',
                            children: []
                        }
                    ],
                    id: 'home1',
                    toggle: true,
                    submenuActive: false,
                    title: '蓝鲸物资采购平台'
                },
                header: {
                    list: [
                        {
                            name: '首页',
                            id: 1,
                            path: 'purchaseHome',
                            show: true
                        },
                        {
                            name: '物品管理',
                            id: 2,
                            path: 'itemManagement',
                            show: true
                        }
                    ],
                    active: 0,
                    bizId: 1
                },
                user: {
                    list: [
                        '个人中心',
                        '退出'
                    ]
                },
                lang: {
                    list: [
                        {
                            name: '中文',
                            id: 'chinese'
                        },
                        {
                            name: 'English',
                            id: 'english'
                        },
                        {
                            name: '日本語',
                            id: 'japanese'
                        }
                    ]
                }
            }
        },
        computed: {
            ...mapGetters(['mainContentLoading']),
            curHeaderNav () {
                return this.header.list[this.header.active] || {}
            }
        },
        created () {
            const platform = window.navigator.platform.toLowerCase()
            if (platform.indexOf('win') === 0) {
                this.systemCls = 'win'
            }
        },
        mounted () {
            const self = this
            bus.$on('show-login-modal', data => {
                self.$refs.bkAuth.showLoginModal(data)
            })
            bus.$on('close-login-modal', () => {
                self.$refs.bkAuth.hideLoginModal()
                setTimeout(() => {
                    window.location.reload()
                }, 0)
            })
        },
        methods: {
            handleToggle (v) {
                this.nav.toggle = v
            },
            toShoppingCar () {
                this.header.active = -1
                this.$router.push({ path: '/shoppingcart' })
            }
        }
    }
</script>

<style lang="postcss">
    @import './css/reset.css';
    @import './css/app.css';
    .toCarTab{
        position: absolute;
        bottom: 140px;
        right: 60px;
        z-index: 1000;
        cursor: pointer;
        border-radius: 50%;
        width: 74px;
        height: 74px;
        border: 1px solid #979BA5;
        background: #fff;
        svg{
            margin-top: 18px;
            margin-left: 15px;
        }
    }
    .toCarTab:hover{
        box-shadow: 0px 0px 4px #888888;
        path{
            fill: #3A84FF;
        }
    }
    .monitor-navigation-header {
        -webkit-box-flex: 1;
        -ms-flex: 1;
        flex: 1;
        overflow: hidden;
        height: 100%;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        font-size: 14px;
        justify-content: space-between;
        .header-nav {
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            padding: 0;
            margin: 0;
            width: 100%;
            display: flex;
            justify-content: space-between;
        }
        .header-nav-item {
            list-style: none;
            height: 50px;
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            margin-right: 40px;
            color: #96A2B9;
            min-width: 56px;
            &.item-active {
                color: #fff !important;
            }
            &:hover {
                cursor: pointer;
                color: #d3d9e4;
            }
        }
        .header-title {
            color: #63656E;
            font-size: 16px;
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            margin-left: -6px;
        }
        .header-title-icon {
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            width: 28px;
            height: 28px;
            font-size: 28px;
            color: #3a84ff;
            cursor: pointer;
        }
        .header-select {
            width: 240px;
            margin-left: auto;
            margin-right: 34px;
            border: none;
            background: #252f43;
            color: #d3d9e4;
            -webkit-box-shadow: none;
            box-shadow: none;
        }
        .header-mind {
            color: #768197;
            font-size: 16px;
            position: relative;
            height: 32px;
            width: 32px;
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            -webkit-box-pack: center;
            -ms-flex-pack: center;
            justify-content: center;
            margin-right: 8px;
            &:hover {
                background: -webkit-gradient(linear,right top, left top,from(rgba(37,48,71,1)),to(rgba(38,50,71,1)));
                background: linear-gradient(270deg,rgba(37,48,71,1) 0%,rgba(38,50,71,1) 100%);
                border-radius: 100%;
                cursor: pointer;
                color: #d3d9e4;
            }
            .lang-icon {
                font-size:20px;
            }
        }
        .header-mind-mark {
            position: absolute;
            right: 8px;
            top: 8px;
            height: 7px;
            width: 7px;
            border: 1px solid #27334C;
            background-color: #EA3636;
            border-radius: 100%
        }
        .header-help {
            color: #768197;
            font-size: 16px;
            position: relative;
            height: 32px;
            width: 32px;
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            -webkit-box-pack: center;
            -ms-flex-pack: center;
            justify-content: center;
            margin-right: 8px;
            &:hover {
                background: -webkit-gradient(linear,right top, left top,from(rgba(37,48,71,1)),to(rgba(38,50,71,1)));
                background: linear-gradient(270deg,rgba(37,48,71,1) 0%,rgba(38,50,71,1) 100%);
                border-radius: 100%;
                cursor: pointer;
                color: #d3d9e4;
            }
        }
        .header-user {
            height: 100%;
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            -webkit-box-pack: center;
            -ms-flex-pack: center;
            justify-content: center;
            color: #96A2B9;
            margin-left: 8px;
            &:hover {
                cursor: pointer;
                color: #d3d9e4;
            }
            .bk-icon {
                margin-left: 5px;
                font-size: 12px;
            }
        }
    }
    .monitor-navigation-content {
        overflow: auto;
        padding: 5px 15px 15px 15px;
        font-size: 14px;
        color: #737987;
        height: calc(100% - 84px);
        background: #FFFFFF;
        -webkit-box-shadow: 0px 2px 4px 0px rgba(25,25,41,0.05);
        box-shadow: 0px 2px 4px 0px rgba(25,25,41,0.05);
        border-radius: 2px;
        border: 1px solid rgba(220,222,229,1);
        .main-content {
            min-height: 600px;
            height: 100%;
        }
    }
    .monitor-navigation-footer {
        height: 52px;
        width: 100%;
        margin: 32px 0 0;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        -webkit-box-pack: center;
        -ms-flex-pack: center;
        justify-content: center;
        border-top: 1px solid #dcdee5;
        color: #63656e;
        font-size: 12px;
    }
    .monitor-navigation-message {
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-orient: vertical;
        -webkit-box-direction: normal;
        -ms-flex-direction: column;
        flex-direction: column;
        width: 360px;
        background-color: #ffffff;
        border: 1px solid #e2e2e2;
        border-radius: 2px;
        -webkit-box-shadow: 0px 3px 4px 0px rgba(64,112,203,0.06);
        box-shadow: 0px 3px 4px 0px rgba(64,112,203,0.06);
        color: #979ba5;
        font-size: 12px;
        .message-title {
            -webkit-box-flex: 0;
            -ms-flex: 0 0 48px;
            flex: 0 0 48px;
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            color: #313238;
            font-size: 14px;
            padding: 0 20px;
            margin: 0;
            border-bottom: 1px solid #f0f1f5;
        }
        .message-list {
            -webkit-box-flex: 1;
            -ms-flex: 1;
            flex: 1;
            max-height: 450px;
            overflow: auto;
            margin: 0;
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-orient: vertical;
            -webkit-box-direction: normal;
            -ms-flex-direction: column;
            flex-direction: column;
            padding: 0;
        }
        .message-list-item {
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            width: 100%;
            padding: 0 20px;
            &:hover {
                cursor: pointer;
                background: #F0F1F5;
            }
            .item-message {
                padding: 13px 0;
                line-height: 16px;
                min-height: 42px;
                -webkit-box-flex: 1;
                -ms-flex: 1;
                flex: 1;
                -ms-flex-wrap: wrap;
                flex-wrap: wrap;
                color: #63656E;
            }
            .item-date {
                padding: 13px 0;
                margin-left: 16px;
                color: #979BA5;
            }
        }
        .message-footer {
            -webkit-box-flex: 0;
            -ms-flex: 0 0 42px;
            flex: 0 0 42px;
            border-top: 1px solid #f0f1f5;
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            -webkit-box-pack: center;
            -ms-flex-pack: center;
            justify-content: center;
            color: #3a84ff;
        }
    }
    .monitor-navigation-nav {
        width: 150px;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-orient: vertical;
        -webkit-box-direction: normal;
        -ms-flex-direction: column;
        flex-direction: column;
        background: #FFFFFF;
        border: 1px solid #E2E2E2;
        -webkit-box-shadow: 0px 3px 4px 0px rgba(64,112,203,0.06);
        box-shadow: 0px 3px 4px 0px rgba(64,112,203,0.06);
        padding: 6px 0;
        margin: 0;
        color: #63656E;
        .nav-item {
            -webkit-box-flex: 0;
            -ms-flex: 0 0 32px;
            flex: 0 0 32px;
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            padding: 0 16px;
            list-style: none;
            &:hover {
                color: #3A84FF;
                cursor: pointer;
                background-color: #F0F1F5;
            }
            .lang-icon {
                font-size: 20px;
                margin-right: 6px;
            }
        }
    }
    .monitor-navigation-admin {
        width: 170px #63656E;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-orient: vertical;
        -webkit-box-direction: normal;
        -ms-flex-direction: column;
        flex-direction: column;
        background: #FFFFFF;
        border: 1px solid #E2E2E2;
        -webkit-box-shadow: 0px 3px 4px 0px rgba(64,112,203,0.06);
        box-shadow: 0px 3px 4px 0px rgba(64,112,203,0.06);
        padding: 6px 0;
        margin: 0;
        color: #63656E;
        .nav-item {
            -webkit-box-flex: 0;
            -ms-flex: 0 0 32px;
            flex: 0 0 32px;
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            padding: 0 16px;
            list-style: none;
            &:hover {
                color: #3A84FF;
                cursor: pointer;
                background-color: #F0F1F5;
            }
            .lang-icon {
                font-size: 20px;
                margin-right: 6px;
            }
        }
    }
    .tippy-popper .tippy-tooltip.navigation-message-theme {
        padding: 0;
        border-radius: 0;
        -webkit-box-shadow: none;
        box-shadow: none;
    }
</style>
