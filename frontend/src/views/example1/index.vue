<template>
    <div class="example1-wrapper">
        <div class="inner">
            <div class="item">
                <p>测试ajax get post 请求</p>
                <bk-button type="default" @click="btn1">btn1（get）</bk-button>
                <p>{{btn1Msg}}</p>
                <bk-button type="default" @click="btn2">btn2（post）</bk-button>
                <p>{{btn2Msg}}</p>
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
                btn1Msg: '',
                btn2Msg: '',
                userInfo: null
            }
        },
        created () {
        },
        methods: {
            /**
             * 获取页面数据
             *
             * @return {Promise} promise 对象
             */
            fetchPageData () {
            },

            /**
             * btn1
             */
            async btn1 () {
                this.$http.get('/test_get_or_post/').then(res => {
                    if (res.result) {
                        this.btn1Msg = res
                    }
                })
            },

            /**
             * btn2
             */
            async btn2 () {
                this.$http.post('/test_get_or_post/').then(res => {
                    if (res.result) {
                        this.btn2Msg = res
                    }
                })
            },
            /**
             * getUser
             */
            async getUser () {
                try {
                    const data = await this.$store.dispatch('userInfo', {}, { fromCache: true })
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
