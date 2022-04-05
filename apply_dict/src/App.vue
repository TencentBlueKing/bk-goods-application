<template>
    <div
        class="monitor-navigation"
        :class="systemCls"
    >
        <bk-navigation
            :header-title="nav.id"
            :side-title="nav.title"
            :default-open="true"
            :navigation-type="'top-bottom'"
            :need-menu="false"
            @toggle="handleToggle"
            v-if="$route.name !== 'home'"
        >
            <div class="top">
                <div class="top-blank"></div>
                <div class="top-content">
                    <div class="top-content-info">
                        {{viewInfo}}
                        <bk-switcher
                            v-model="isApplyViewSwitcherOnF"
                            v-if="hasApplyViewSwitcher"
                            theme="primary"
                        ></bk-switcher>
                    </div>
                    <div class="top-content-underline"></div>
                </div>
            </div>
            <template slot="header">
                <div class="monitor-navigation-header">
                    <ol class="header-nav">
                        <div
                            v-for="(item,index) in header.list"
                            :key="item.id"
                            theme="light navigation-message"
                            :arrow="false"
                            offset="0, -5"
                            placement="bottom"
                        >
                            <router-link :to="{ name: item.pageName }">
                                <li
                                    v-if="item.show"
                                    class="header-nav-item"
                                    :class="{ 'item-active': index === header.active }"
                                    @click="header.active = (item.id - 1)"
                                >
                                    {{item.name}}
                                </li>
                            </router-link>
                        </div>
                    </ol>
                    <bk-popover
                        theme="light navigation-message"
                        :arrow="false"
                        offset="20, 10"
                        :align="'left'"
                        placement="bottom-start"
                        :tippy-options="{ 'hideOnClick': false }"
                    >
                        <div class="header-user">
                            {{ userInfo.username }}
                            <i class="bk-icon icon-down-shape"></i>
                        </div>
                        <template slot="content">
                            <ul
                                class="monitor-navigation-admin"
                                style="right: 0"
                            >
                                <li
                                    class="nav-item"
                                    v-for="userItem in user.list"
                                    :key="userItem"
                                    @click="PUSH(userItem)"
                                >
                                    {{userItem.name}}
                                </li>
                            </ul>
                            <bk-dialog
                                v-model="userCenterDialogVisible"
                                title="个人信息"
                                :width="400"
                                :esc-close="false"
                                :show-footer="false"
                            >
                                <div style="width: 100%; margin: 0">
                                    <user-center ref="userCenter"></user-center>
                                </div>
                            </bk-dialog>
                        </template>
                    </bk-popover>
                </div>
            </template>
            <div class="monitor-navigation-content">
                <main
                    class="main-content"
                    v-bkloading="{ isLoading: mainContentLoading, opacity: 1 }"
                >
                    <router-view
                        :key="routerKey"
                        v-show="!mainContentLoading"
                    />
                </main>
            </div>
            <template slot="footer">
                <div class="monitor-navigation-footer">
                    Copyright © 2012-{{new Date().getFullYear()}} Tencent BlueKing. All Rights Reserved. 腾讯蓝鲸 版权所有
                </div>
            </template>
        </bk-navigation>
        <app-auth ref="bkAuth"></app-auth>
        <Home
            class="home-wrapper"
            v-if="$route.name === 'home'"
        ></Home>
    </div>
</template>

<script>
    import { mapState } from 'vuex'
    import { bus } from '@/common/bus'
    import userCenter from './views/main/userCenter.vue'
    import Home from './views/Home.vue'
    export default {
        name: 'monitor-navigation',
        components: { userCenter, Home },
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
                    title: '物资申请平台'
                },
                header: {
                    list: [
                        {
                            name: '首页',
                            id: 1,
                            pageName: 'applyHome',
                            show: true
                        },
                        {
                            name: '申请管理',
                            id: 2,
                            pageName: 'applyManagement',
                            show: false
                        }
                    ],
                    active: 0,
                    bizId: 1
                },
                user: {
                    list: [
                        {
                            name: '个人中心',
                            id: '',
                            pageName: ''
                        },
                        {
                            name: '历史记录',
                            id: '',
                            pageName: 'applyHistory'
                        }
                    ]
                },
                userCenterDialogVisible: false
            }
        },
        computed: {
            ...mapState({
                userInfo: state => state.user.userInfo,
                viewInfo: state => state.viewInfo,
                hasApplyViewSwitcher: state => state.hasApplyViewSwitcher
            }),
            isApplyViewSwitcherOnF: {
                get () {
                    return this.$store.state.isApplyViewSwitcherOn
                },
                set (newVal) {
                    const context = {
                        'viewInfo': '批量申请',
                        'hasApplyViewSwitcher': true,
                        'isApplyViewSwitcherOn': newVal
                    }
                    this.$store.commit('updateViewInfo', context)
                }
            },
            curHeaderNav () {
                return this.header.list[this.header.active] || {}
            },
            viewInfoF () {
                return this.viewInfo
            },
            hasApplyViewSwitcherF () {
                return this.hasApplyViewSwitcher
            }

        },
        watch: {
            viewInfoF (newVal, _) {
                this.viewInfo = newVal
            },
            hasApplyViewSwitcherF (newVal, _) { // 监听vuex状态的变化
                this.hasApplyViewSwitcher = newVal
            }
        },
        created () {
            const platform = window.navigator.platform.toLowerCase()
            if (platform.indexOf('win') === 0) {
                this.systemCls = 'win'
            }
        },
        mounted () {
            this.header.list[1].show = this.userInfo.isScretary // 是管理员则显示该栏目；否则不显示
            const self = this
            document.querySelector('.main-content').setAttribute('style', '')
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
            findApplyManagement (obj) {
                return obj.id === 2
            },
            PUSH (item) {
                if (item.name === '个人中心') {
                    this.userCenterDialogVisible = true
                    this.$refs.userCenter.loadData()
                    this.header.active = -1
                } else {
                    this.$router.push({ name: item.pageName })
                    this.header.active = -1
                }
            }
        }
    }
</script>

<style lang="postcss">
    @import "./css/reset.css";
    @import "./css/app.css";
    .monitor-navigation /deep/ .container-content {
        position: relative;
    }
    .bk-dialog-wrapper .bk-dialog-body {
        padding: 0 0 20px 40px;
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
            color: #96a2b9;
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
            color: #63656e;
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
                background: -webkit-gradient(
                    linear,
                    right top,
                    left top,
                    from(rgba(37, 48, 71, 1)),
                    to(rgba(38, 50, 71, 1))
                );
                background: linear-gradient(
                    270deg,
                    rgba(37, 48, 71, 1) 0%,
                    rgba(38, 50, 71, 1) 100%
                );
                border-radius: 100%;
                cursor: pointer;
                color: #d3d9e4;
            }
            .lang-icon {
                font-size: 20px;
            }
        }
        .header-mind-mark {
            position: absolute;
            right: 8px;
            top: 8px;
            height: 7px;
            width: 7px;
            border: 1px solid #27334c;
            background-color: #ea3636;
            border-radius: 100%;
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
                background: -webkit-gradient(
                    linear,
                    right top,
                    left top,
                    from(rgba(37, 48, 71, 1)),
                    to(rgba(38, 50, 71, 1))
                );
                background: linear-gradient(
                    270deg,
                    rgba(37, 48, 71, 1) 0%,
                    rgba(38, 50, 71, 1) 100%
                );
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
            color: #96a2b9;
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
        background: #ffffff;
        -webkit-box-shadow: 0px 2px 4px 0px rgba(25, 25, 41, 0.05);
        box-shadow: 0px 2px 4px 0px rgba(25, 25, 41, 0.05);
        border-radius: 2px;
        border: 1px solid rgba(220, 222, 229, 1);
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
        -webkit-box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
        box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
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
                background: #f0f1f5;
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
                color: #63656e;
            }
            .item-date {
                padding: 13px 0;
                margin-left: 16px;
                color: #979ba5;
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
        background: #ffffff;
        border: 1px solid #e2e2e2;
        -webkit-box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
        box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
        padding: 6px 0;
        margin: 0;
        color: #63656e;
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
                color: #3a84ff;
                cursor: pointer;
                background-color: #f0f1f5;
            }
            .lang-icon {
                font-size: 20px;
                margin-right: 6px;
            }
        }
    }
    .monitor-navigation-admin {
        width: 170px #63656e;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-orient: vertical;
        -webkit-box-direction: normal;
        -ms-flex-direction: column;
        flex-direction: column;
        background: #ffffff;
        border: 1px solid #e2e2e2;
        -webkit-box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
        box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
        padding: 6px 0;
        margin: 0;
        color: #63656e;
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
                color: #3a84ff;
                cursor: pointer;
                background-color: #f0f1f5;
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
    .top {
        .top-blank {
            height: 100px;
        }
        .top-content {
            position: relative;
            width: 160px;
            height: 25px;
            left: 130px;
            top: -68px;
            text-align: center;
            .top-content-info {
                font-family: 'Roboto';
                font-style: normal;
                font-size: 20px;
                line-height: 24px;
                color: #000000;
            }
            .top-content-underline {
                width: 160px;
                height: 10px;
                background: #0051DA;
                box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.25);
                border-radius: 12px;
            }
        }
    }
</style>
