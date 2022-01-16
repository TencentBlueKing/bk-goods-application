<template>
    <div class="index-wrapper">
        <bk-button :text="true" title="primary" @click="toIndex()" class="indexButton" v-if="showReturn">
            <bk-icon type="angle-double-left" style="font-size: 20px;" /> 返回首页
        </bk-button>
        <div class="search">
            <bk-input v-model="searchContent" :clearable="false" :font-size="'medium'" size="large">
                <bk-dropdown-menu class="group-text" @show="dropdownShow" @hide="dropdownHide" ref="dropdown" slot="prepend" :font-size="'medium'">
                    <bk-button type="primary" slot="dropdown-trigger" class="selectType">
                        <span>{{ type.type_name }}</span>
                        <i :class="['bk-icon icon-angle-down',{ 'icon-flip': isDropdownShow }]"></i>
                    </bk-button>
                    <ul class="bk-dropdown-list" slot="dropdown-content">
                        <li><a href="javascript:;" v-for="(item, index) in typeList" :key="index" @click="triggerHandler(item)">{{ item.type_name }}</a></li>
                    </ul>
                </bk-dropdown-menu>
                <template slot="append">
                    <bk-button theme="primary" title="search" :outline="true" class="group-text" :text="true" @click="search()">
                        <bk-icon type="search" />
                    </bk-button>
                </template>
            </bk-input>
        </div>
        <div class="banner" v-if="showBanner">
            <bk-swiper :pics="bannerPics" height="300" width="950" :is-loop="false" class="swiper"></bk-swiper>
        </div>
        <div class="exception-wrap" v-if="showEmpty">
            <bk-exception class="exception-wrap-item exception-part" type="search-empty" scene="page" :class="{ 'exception-gray': isGray }"> </bk-exception>
        </div>
        <div class="goods">
            <div class="goodCard" v-for="(item, index) in goodsList" :key="index" @click="toDetail(item.id)">
                <bk-card :show-head="false" class="bkCard">
                    <img :src="item.pics" alt="">
                    <p class="goodName">{{ item.good_name }}</p>
                    <div class="goodPrice">￥<div style="color: orange">{{ item.price }}</div></div>
                    <p>{{ item.cn_status }}</p>
                    <div class="addButton">
                        <bk-button theme="primary" title="search" :outline="true" class="group-text" :text="true" @click.stop="add2cart(item.id)">
                            加入购物车
                        </bk-button>
                    </div>
                </bk-card>
            </div>
        </div>
        <div class="paginator">
            <bk-pagination
                align="center"
                :current.sync="currentPage"
                :count.sync="pageCount"
                :show-limit="false">
            </bk-pagination>
        </div>
    </div>
</template>

<script>

    const goodsUrl = '/purchase/get_good_list' // 获取物品信息接口
    const typesUrl = '/purchase/get_good_type_list' // 获取商品种类
    const detailUrl = 'xxx' // 物品详情跳转链接
    const add2cartUrl = '/purchase/add_cart_goods' // 添加到购物车接口

    export default {
        data () {
            return {
                username: '', // 用户名
                typeList: {}, // 种类列表
                type: '', // 种类
                lastType: '', // 存放上一类型
                bannerNum: 6, // 轮播图数量
                searchContent: '', // 搜索内容
                lastSearchContent: '', // 保留上次的搜索内容
                bannerPics: [], // 轮播图
                goodsList: '', // 商品列表
                isDropdownShow: false, // 种类组件参数
                currentPage: 1, // 当前页数（不用于请求）
                paramPage: 1, // 用于请求的页数
                pageCount: 0, // 总页数
                config: { // 组件参数
                    strokeWidth: 10,
                    bgColor: '#f0f1f5',
                    activeColor: '#3a84ff'
                },
                showReturn: 0, // 是否展示返回首页按钮
                showBanner: 1, // 是否展示轮播图
                showEmpty: 0,
                goodInfo: {
                    num: 1,
                    id: '',
                    username: this.username
                }
            }
        },
        watch: {
            currentPage (val) { // 监测页数的变化
                this.paramPage = val
                this.type = this.lastType
                this.searchContent = this.lastSearchContent
                this.getGoods()
            }
        },
        created () {
            this.username = this.$store.state.user.username
            this.loadData() // 创建实例时加载数据
        },
        methods: {
            loadData () { // 创建时调用获取基本数据
                this.getTypes()
                this.getGoods()
            },
            getTypes () { // 获取所有商品类型
                this.$http.get(typesUrl).then(res => {
                    if (res && res.result === true) { // 判空
                        // eslint-disable-next-line no-new-object
                        const allTypes = new Object()
                        allTypes.id = 0
                        allTypes.type_name = '所有类型'
                        res.data.unshift(allTypes) // 加入所有类型选项
                        this.typeList = res.data // 给类型列表赋值
                    } else if (res && res.result === false) {
                        this.handleError({ theme: 'error' }, res.message)
                    }
                }).catch(() => {
                    // 处理错误
                })
            },
            getGoods () { // 获取指定商品信息
                if (this.lastType !== this.type) {
                    this.paramPage = 1
                }
                this.$http.get(goodsUrl, {
                    params: {
                        good_name: this.searchContent, // 指定商品名称所含内容
                        good_type_id: this.type.id, // 指定商品类型
                        page: this.paramPage, // 指定页
                        size: 8
                    }
                }).then(res => {
                    if (res && res.result === true) {
                        this.lastType = this.type
                        this.lastSearchContent = this.searchContent
                        this.currentPage = this.paramPage
                        this.goodsList = res.data.good_list
                        this.bannerPics = []
                        for (let i = 0; i < res.data.good_list.length; i++) {
                            if (i < this.bannerNum && this.currentPage === 1) { // 给轮播图列表赋值，逻辑是将前六个商品图片赋值给轮播图列表
                                const bannerObject = Object()
                                bannerObject.url = this.goodsList[i].pics[0]
                                bannerObject.link = detailUrl + '/' + this.goodsList[i].id
                                this.bannerPics.push(bannerObject)
                            }
                            this.goodsList[i].pics = this.goodsList[i].pics[0] // 将商品的第一个图片作为展示图片
                        }
                        this.pageCount = res.data.total_num / 8 * 10 // 给页面总数赋值
                        if (res.data.total_list.length === 0) {
                            this.showEmpty = 1 // 显示搜索为空
                        } else {
                            this.showEmpty = 0
                        }
                    } else if (res && res.result === false) {
                        this.handleError({ theme: 'error' }, res.message)
                    }
                }).catch(() => {
                    // 处理错误
                })
            },
            handleError (config, message) {
                config.message = message
                config.offsetY = 80
                this.$bkMessage(config)
            },
            toDetail (id) { // 点击商品卡片跳转到商品详情页
                this.$router.push({ path: detailUrl + '/' + id })
            },
            add2cart (id) { // 点击加入购物车按钮将商品加入购物车
                this.goodInfo.id = id
                if (this.goodInfo.id) {
                    this.$http.post(add2cartUrl, { goodInfo: this.goodInfo }).then(res => {
                        // eslint-disable-next-line no-empty
                        if (res && res.result === true) {
                            
                        } else if (res && res.result === false) {
                            this.handleError({ theme: 'error' }, res.message)
                        }
                    })
                }
            },
            dropdownShow () {
                this.isDropdownShow = true
            },
            dropdownHide () {
                this.isDropdownShow = false
            },
            triggerHandler (type) {
                this.$refs.dropdown.hide()
                this.type = type
            },
            search () { // 点击搜索触发事件
                this.showReturn = 1
                this.showBanner = 0
                // TODO: 对type和searchContent进行post获取新数据
                this.getGoods()
            },
            toIndex () { // 点击返回首页触发事件
                this.$router.go(0)
            }
        }
    }
</script>

<style lang="postcss" scoped>
.index-wrapper{
    .indexButton{
        margin: 20px 30px;
        color: #000;
    }
    .banner{
        width: 100%;
        .swiper {
            left: 15%;
            width: 100%;
            height: 300px;
        }
        
    }
    .search{
        margin: 30px;
        width: 80%;
        text-align: center;
        margin-left: 130px;
        .selectType{
            background-color: #f2f2f2;;
        }
        .group-text{
            height: 36px;
        }
    }
    .goods{
        margin-top: 50px;
        height: auto;
        .goodCard{
            width: 250px;
            display: inline-block;
            float: left;
            margin: 20px 40px;
            .goodName{
                font-size: 25px;
            }
            .goodPrice{
                display: flex;
                font-size: 15px;
            }
            .goodStatus{
                color: #b0b0b0;
                font-size: 10px;
            }
            .addButton{
                text-align: right;
            }
            img{
                width: 200px;
            }
            p {
                margin-top: 10px;
                margin-bottom: 10px;
                &:last-child {
                    margin-bottom: 0;
                    color: #b2b1b1;
                    font-size: 10px;
                }
            }
        }
    }
    .paginator{
        width: 100%;
        display: inline-block;
        margin-top: 70px;
    }
}
</style>
