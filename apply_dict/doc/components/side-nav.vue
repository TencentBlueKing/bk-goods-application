<template>
    <div class="side-nav">
        <div class="side-header">
            <div class="title">
                <img src="@doc/images/logo.png" class="vue-logo">
                蓝鲸前端开发脚手架
            </div>
        </div>
        <div class="nav-item" v-for="(group, groupIndex) in groups" :key="groupIndex">
            <div class="nav-title" :class="!group.groupId ? 'no-groupid' : ''">{{group.groupId}}</div>
            <div class="nav-content" :class="{
                'nav-active': activeId === component.id || activeId === component.id + 'Example'
            }" v-for="(component, componentIndex) in group.components" :key="componentIndex" @click="changeRouter(component)">
                {{component.text}}
            </div>
        </div>
    </div>
</template>

<script>
    import { getActualTop } from '@/common/util'

    export default {
        data () {
            return {
                groups: [
                    {
                        components: [
                            {
                                id: 'introduction',
                                text: '简介'
                            },
                            {
                                id: 'installAndUsage',
                                text: '安装与使用'
                            }
                        ]
                    },
                    {
                        groupId: 'bkui-cli 使用命令介绍',
                        components: [
                            {
                                id: 'commandHelp',
                                text: 'bkui -h'
                            },
                            {
                                id: 'commandVersion',
                                text: 'bkui -v'
                            },
                            {
                                id: 'commandInit',
                                text: 'bkui init'
                            }
                        ]
                    },
                    {
                        groupId: 'bkui-cli 命令行问答式交互',
                        components: [
                            {
                                id: 'questionExplain',
                                text: '命令行问题说明'
                            }
                        ]
                    },
                    {
                        groupId: '生成项目目录结构说明',
                        components: [
                            {
                                id: 'webpack4DirExplain',
                                text: 'webpack4 类型项目目录结构'
                            }
                        ]
                    },
                    {
                        groupId: '配置说明',
                        components: [
                            {
                                id: 'configExplain',
                                text: '配置说明'
                            }
                        ]
                    }
                ],
                activeId: ''
            }
        },
        watch: {
            $route (to, from) {
                this.$nextTick(() => {
                    window.scrollTo(0, 0)
                })
                this.activeId = to.name || ''

                this.hashChangeHanlder()
            }
        },
        created () {
            this.activeId = this.$route.name || ''
        },
        mounted () {
            const curActiveMenu = document.querySelector('.nav-content.nav-active')
            if (curActiveMenu) {
                document.querySelector('.app-side-nav').scrollTop = curActiveMenu.offsetTop - 85
            }
        },
        methods: {
            changeRouter (component, componentIndex) {
                this.activeId = component.id
                this.$router.push({
                    name: component.id
                })
            },
            hashChangeHanlder () {
                const hash = this.$route.hash
                if (hash) {
                    const node = document.querySelector('.app-content').querySelector(`a[href="${hash}"]`)
                    this.jumpHash(node)
                }
            },
            jumpHash (node) {
                setTimeout(() => {
                    if (!node) {
                        window.scrollTo(0, 0)
                        return
                    }
                    const top = getActualTop(node)
                    window.scrollTo(0, top - 70)
                }, 10)
            }
        }
    }
</script>

<style scoped lang="postcss">
    @import '@doc/css/side-nav.css';
</style>
