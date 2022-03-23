<template>
    <div class="magic-footer">
        <div class="magic-copyright">
            <p>
                <a href="javascript:void(0);" id="contact-us" class="link magic-contact">
                    <img src="@doc/images/qq.png" style="width:17px;">QQ交谈
                </a>
                Copyright © 2012-<span id="cur_year">{{year}}</span> Tencent BlueKing. All Rights Reserved. 蓝鲸智云 版权所有
            </p>
        </div>
        <div class="magic-button">
            <a href="javascript:void(0);" class="magic-top" v-show="showBackTop" @click="backTop">
                <img src="@doc/images/back-top.png" alt="返回顶部" />
            </a>
            <a href="https://bk.tencent.com/s-mart/community" target="_blank" class="magic-feedback">
                <img src="@doc/images/feedback.png" alt="反馈" />
            </a>
        </div>
    </div>
</template>

<script>
    import { loadScript } from '@/common/util'

    export default {
        data () {
            return {
                year: new Date().getFullYear(),
                showBackTop: false
            }
        },
        mounted () {
            window.addEventListener('scroll', this.toggleBackTop)
            loadScript('http://wp.qiye.qq.com/loader/4.0.0.js', this.loadScriptCallback)
        },
        destroyed () {
            window.removeEventListener('scroll', this.toggleBackTop)
        },
        methods: {
            /**
             * 加载 script 回调函数，主要用于加载 QQ 交谈唤起 QQ 的 script
             *
             * @param {string} e 错误信息
             */
            loadScriptCallback (e) {
                if (e) {
                    console.error(e)
                    return
                }

                try {
                    window.__WPA.create({
                        nameAccount: '800802001',
                        customEle: document.getElementById('contact-us')
                    })
                } catch (err) {
                    console.error(`唤起 QQ 失败: ${err}`)
                }
            },

            /**
             * 获取页面滚动高度，判断是否出现返回顶部
             */
            toggleBackTop () {
                let scrollTop = 0
                let bodyScrollTop = 0
                let documentScrollTop = 0

                if (document.body) {
                    bodyScrollTop = document.body.scrollTop
                }

                if (document.documentElement) {
                    documentScrollTop = document.documentElement.scrollTop
                }

                scrollTop = (bodyScrollTop - documentScrollTop > 0) ? bodyScrollTop : documentScrollTop
                this.showBackTop = scrollTop > 0
            },

            /**
             * 返回到页面顶部
             */
            backTop () {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                })
            }
        }
    }
</script>

<style scoped lang="postcss">
    @import '@doc/css/footer.css';
</style>
