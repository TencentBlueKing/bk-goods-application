<template>
    <div class="example3-wrapper">
        <div class="inner">
            <div class="item">
                <p>我是 example3 页面，本页和 example1 页面一样，可以三个 router 切换看看请求情况。以下示例注意打开控制台观察</p>
                <p>从其他页面切换到本页面时，本页面会显示 loading，这个 loading 的持续过程包括了所有页面的公共请求(/api/user/)以及本页面自己的抓取数据的请求。</p>
                <p>本页面自己的请求为 /app/index?invoke=enterExample1 和 /app/index?invoke=enterExample2，详情参见 src/views/example1/index.vue 文件 fetchPageData 方法。用来模拟进入页面，需要获取数据才能显示页面的情况。</p>
            </div>
            <div class="item">
                <p>{{enterMsg1}}</p>
                <p>{{enterMsg2}}</p>
            </div>
        </div>
        <div class="inner">
            <div class="item">
                <p>点击下方的 btn1 按钮发送一个 ajax 请求，请求执行时间为 2 秒，多次点击，<b>会</b> cancel 上一次未返回的请求</p>
                <p>点击下方的 btn2 按钮发送一个 ajax 请求，请求执行时间为 2 秒，多次点击，<b>不会</b> cancel 上一次未返回的请求</p>
                <bk-button type="default" @click="btn1">btn1（get）</bk-button>
                <bk-button type="default" @click="btn2">btn2（post）</bk-button>
            </div>
            <div class="item">
                <p>{{btn1Msg}}</p>
                <p>{{btn2Msg}}</p>
            </div>
        </div>
        <div class="inner">
            <div class="item">
                <p>演示 delete 请求，如何发送数据</p>
                <bk-button type="default" @click="del">del</bk-button>
            </div>
            <div class="item">
                <p>{{delMsg}}</p>
            </div>
        </div>
        <div class="inner">
            <div class="item">
                <p>获取 user 信息</p>
                <bk-button type="default" @click="getUser">getUser</bk-button>
            </div>
            <div class="item">
                <p>{{userInfo}}</p>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        components: {
        },
        data () {
            return {
                getMsg: '',
                postMsg: '',
                deleteMsg: '',
                longMsg: '',
                enterMsg1: '',
                enterMsg2: '',
                btn1Msg: '',
                btn2Msg: '',
                delMsg: '',
                userInfo: null
            }
        },
        created () {
        },
        methods: {
            /**
             * 获取页面数据
             * 如果在页面中重写此方法，那么 mixins 中的这个方法不会被执行
             *
             * @return {Promise} promise 对象
             */
            fetchPageData () {
                // 串行写法
                // await this.$store.dispatch(`example/enterExample1`, {time: +new Date()})
                // await this.$store.dispatch(`example/enterExample2`, {time: +new Date()})

                // 并行写法
                const promises = []
                promises.push(this.$store.dispatch('example/enterExample1', { delay: 1000 }))
                promises.push(this.$store.dispatch('example/enterExample2', { delay: 1000 }))
                return Promise.all(promises).then(res => {
                    this.enterMsg1 = res[0].data.msg
                    this.enterMsg2 = res[1].data.msg
                }).catch(err => {
                    console.error('err', err)
                })
            },

            /**
             * btn1
             */
            async btn1 () {
                try {
                    const res = await this.$store.dispatch('example/btn1', { btn: 'btn1', delay: 2000 })
                    this.btn1Msg = res.data.msg
                } catch (e) {
                    console.error(e)
                }
            },

            /**
             * btn2
             */
            async btn2 () {
                try {
                    const res = await this.$store.dispatch('example/btn2', { btn: 'btn2', delay: 2000 }, { cancelPrevious: false })
                    this.btn2Msg = res.data.msg
                } catch (e) {
                    console.error(e)
                }
            },

            /**
             * del
             */
            async del () {
                try {
                    const res = await this.$store.dispatch('example/del', { time: +new Date() })
                    this.delMsg = res.data.msg
                } catch (e) {
                    console.error(e)
                }
            },

            /**
             * getUser
             */
            async getUser () {
                try {
                    const data = await this.$store.dispatch('userInfo')
                    this.userInfo = Object.assign({}, data)
                } catch (e) {
                    console.error(e)
                }
            }
        }
    }
</script>

<style scoped>
    @import './index.css';
</style>
