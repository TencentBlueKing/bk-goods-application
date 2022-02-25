<template>
    <header class="magic-header">
        <a :href="`${host}/`" target="_blank" class="logo">
            <img src="@doc/images/magic.png" alt="">
        </a>
        <ul class="clearfix">
            <li class="dropdown nav-dropdown" id="nav_index">
                <button class="btn btn-default dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-expanded="true">
                    <span>组件库</span>
                    <span class="caret"></span>
                </button>
                <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu1">
                    <li><a role="meneitem" target="_blank" :href="`${host}/`"><span>PC端(普通版)</span></a>
                    </li>
                    <li><a role="meneitem" target="_blank" :href="`${host}/#index?isPro=1`"><span>PC端(标准版)</span></a>
                    </li>
                    <li><a role="meneitem" target="_blank" :href="`${host}/components_vue/2.0/example/index.html#/`"><span>Vue组件</span></a>
                    </li>
                    <li><a role="meneitem" target="_blank" :href="`${host}/#mobile/show`"><span>移动端</span></a>
                    </li>
                    <li><a role="meneitem" target="_blank" :href="`${host}/#components`"><span>组件预览</span></a>
                    </li>
                </ul>
            </li>
            <li class="dropdown nav-dropdown">
                <button class="btn btn-default dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-expanded="true">
                    <span>可视化布局</span>
                    <span class="caret"></span>
                </button>
                <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu1">
                    <li><a role="meneitem" target="_blank" :href="`${host}/#build/show`"><span>PC端</span></a>
                    </li>
                    <li><a role="meneitem" target="_blank" :href="`${host}/#mobile_build/show`"><span>移动端</span></a>
                    </li>
                    <li><a role="meneitem" target="_blank" :href="`${host}/#wx_build/show`"><span>微信小程序</span></a>
                    </li>
                </ul>
            </li>
            <li id="example_index"><a target="_blank" :href="`${host}/#templates`"><span>套餐样例</span></a>
            </li>
            <li id="plugin_index"><a target="_blank" :href="`${host}/#plugin`">插件列表</a>
            </li>
            <li class="dropdown magic-doc-list nav-dropdown" id="nav-dropdown">
                <button class="btn btn-default dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-expanded="true">
                    <span>帮助文档</span>
                    <span class="caret"></span>
                </button>
                <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu1">
                    <li><a role="meneitem" target="_blank" :href="`${host}/#doc/show?id=html_structure`">前端规范</a>
                    </li>
                    <li><a role="meneitem" target="_blank" :href="`${host}/#design`">设计规范</a>
                    </li>
                    <li><a role="meneitem" target="_blank" :href="`${host}/#css`">辅助样式</a>
                    </li>
                    <li><a role="meneitem" target="_blank" :href="`${host}/#about/show`">模版下载</a>
                    </li>
                </ul>
            </li>
            <li id="nav_start" style="margin-left:1px;"><a target="_blank" :href="`${host}/#start`"><span>新手起步</span></a>
            </li>
            <li class="fr header-user" style="display:none;" id="header_user_box">
                <div class="fr logout"> <span class="magic-poweroff">退出</span>

                </div>
                <div class="fr" id="magic_user">
                    <img src="" alt="" class="avatar">
                    <a class="name" target="_blank" :href="`${host}/#mytemplates`"></a>
                </div>
            </li>
        </ul>
    </header>
</template>

<script>
    export default {
        data () {
            return {
                host: '//magicbox.bk.tencent.com'
            }
        }
    }
</script>

<style scoped lang="postcss">
    @import '@doc/css/header.css';
</style>
