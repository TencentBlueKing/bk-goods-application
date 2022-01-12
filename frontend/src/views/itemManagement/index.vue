<template>
    <div class="example2-wrapper">
        <div class="inner">
            <div class="item">
                <p>我是 example2 页面。以下示例注意打开控制台观察</p>
                <p>本页面没有页面显示需要的数据的请求，只有一个公共请求(userInfo)</p>
            </div>
            <div class="item">
                <p>{{$store.getters.user}}</p>
            </div>
            <div class="item">
                <bk-date-picker class="mr15" v-model="initDateTime" :type="'datetime'" :placeholder="'选择日期'"></bk-date-picker>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        components: {},
        data () {
            return {
                initDateTime: new Date()
            }
        },
        created () {
        },
        methods: {
        }
    }
</script>

<style scoped>
    @import './index.css';
</style>
