<template>
    <div class="index-wrapper">
        <div class="header">
        </div>
        <div
            class="toCarTab"
            @click="toShoppingCar"
            v-if="!isAdmin"
        >
            <svg
                t="1641539862015"
                class="icon"
                viewBox="0 0 1028 1024"
                version="1.1"
                p-id="2153"
                width="40"
                height="40"
            >
                <path
                    d="M332.8 790.528q19.456 0 36.864 7.168t30.208 19.968 20.48 30.208 7.68 36.864-7.68 36.864-20.48 30.208-30.208 20.48-36.864 7.68q-20.48 0-37.888-7.68t-30.208-20.48-20.48-30.208-7.68-36.864 7.68-36.864 20.48-30.208 30.208-19.968 37.888-7.168zM758.784 792.576q19.456 0 37.376 7.168t30.72 19.968 20.48 30.208 7.68 36.864-7.68 36.864-20.48 30.208-30.72 20.48-37.376 7.68-36.864-7.68-30.208-20.48-20.48-30.208-7.68-36.864 7.68-36.864 20.48-30.208 30.208-19.968 36.864-7.168zM930.816 210.944q28.672 0 44.544 7.68t22.528 18.944 6.144 24.064-3.584 22.016-13.312 37.888-22.016 62.976-23.552 68.096-18.944 53.248q-13.312 40.96-33.28 56.832t-49.664 15.872l-35.84 0-65.536 0-86.016 0-96.256 0-253.952 0 14.336 92.16 517.12 0q49.152 0 49.152 41.984 0 20.48-9.728 35.84t-38.4 14.336l-49.152 0-94.208 0-118.784 0-119.808 0-99.328 0-55.296 0q-20.48 0-34.304-9.216t-23.04-24.064-14.848-32.256-8.704-32.768q-1.024-6.144-5.632-29.696t-11.264-58.88-14.848-78.848-16.384-87.552q-19.456-103.424-44.032-230.4l-76.8 0q-15.36 0-25.6-7.68t-16.896-18.432-9.216-23.04-2.56-22.528q0-20.48 13.824-33.792t37.376-12.288l103.424 0q20.48 0 32.768 6.144t19.456 15.36 10.24 18.944 5.12 16.896q2.048 8.192 4.096 23.04t4.096 30.208q3.072 18.432 6.144 38.912l700.416 0zM892.928 302.08l-641.024-2.048 35.84 185.344 535.552 1.024z"
                    p-id="2154"
                    fill="#bfbfbf"
                ></path>
            </svg>
        </div>
        <div class="search">
            <el-autocomplete
                v-model="searchContent"
                :fetch-suggestions="querySearch"
                placeholder="请输入内容"
                style="width:90%"
                value-key="type_name"
            >
                <el-button slot="append" icon="el-icon-search" @click="search"></el-button>
            </el-autocomplete>
        </div>
        <div
            class="exception-wrap"
            v-if="showEmpty"
        >
            <bk-exception
                class="exception-wrap-item exception-part"
                type="search-empty"
                scene="page"
                :class="{ 'exception-gray': isGray }"
            >
            </bk-exception>
        </div>
        <div class="goods">
            <div
                class="goodCard"
                v-for="(item, index) in goodsList"
                :key="index"
                @click="toDetail(item.id)"
            >
                <bk-card
                    :show-head="false"
                    class="bkCard"
                >
                    <img
                        :src="item.pics"
                        alt=""
                        style="
                            width: 200px;
                            height: 180px;
                            margin: 10px 10px 0 10px;
                        "
                        v-if="item.pics"
                    />
                    <div
                        class="replacePic"
                        v-if="!item.pics"
                        style="
                            width: 200px;
                            height: 180px;
                            margin: 10px 10px 0 10px;
                        "
                    ></div>
                    <p class="goodName">{{ item.good_name }}</p>
                    <div class="goodPrice">
                        ￥
                        <div style="color: orange">{{ item.price }}</div>
                    </div>
                    <p>{{ item.cn_status }}</p>
                    <div
                        class="replace-addButton"
                        v-if="isAdmin"
                    ></div>
                    <div
                        class="addButton"
                        v-if="!isAdmin"
                    >
                        <bk-button
                            theme="primary"
                            title="search"
                            :outline="true"
                            class="group-text"
                            :text="true"
                            @click.stop="addToCart(item.id)"
                        >
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
                :show-limit="false"
            >
            </bk-pagination>
        </div>
    </div>
</template>

<script>
    import { mapState } from 'vuex'

    import {
        GET_GOOD_LIST_URL, GET_GOOD_TYPE_LIST_URL, ITEMDETAIL_URL, ADD_CART_GOODS_URL
    } from '@/pattern'

    export default {
        data () {
            return {
                username: '', // 用户名
                isAdmin: false, // 是否是管理员
                typeList: [], // 种类列表
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
                pageSize: 4,
                pageCount: 0, // 总页数
                config: { // 组件参数
                    strokeWidth: 10,
                    bgColor: '#f0f1f5',
                    activeColor: '#3a84ff'
                },
                showReturn: 0, // 是否展示返回首页按钮
                showEmpty: 0,
                goodInfo: {
                    num: 1,
                    id: '',
                    username: ''
                }
            }
        },
        computed: {
            ...mapState({
                userInfo: state => state.user.userInfo
            })
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
            this.username = this.userInfo.username
            this.isAdmin = this.userInfo.isAdmin
            this.loadData() // 创建实例时加载数据
        },
        mounted () {
            this.$store.commit('updateViewInfo', '采购首页')
        },
        methods: {
            loadData () { // 创建时调用获取基本数据
                this.getTypes()
                this.getGoods()
            },
            getTypes () { // 获取所有商品类型
                this.$http.get(GET_GOOD_TYPE_LIST_URL).then(res => {
                    if (res && res.result === true) { // 判空
                        this.typeList = res.data // 给类型列表赋值
                    } else if (res && res.result === false) {
                        this.handleError({ theme: 'error' }, res.message)
                    }
                }).catch(() => {
                    // 处理错误
                })
            },
            getGoods () { // 获取指定商品信息
                if (this.showReturn === 0) {
                    this.pageSize = 8
                } else {
                    this.pageSize = 8
                }
                this.$http.get(GET_GOOD_LIST_URL, {
                    params: {
                        good_name: this.searchContent, // 指定商品名称所含内容
                        good_type_id: this.type.id, // 指定商品类型
                        page: this.paramPage, // 指定页
                        size: this.pageSize
                    }
                }).then(res => {
                    if (res && res.result === true) {
                        this.lastType = this.type
                        this.lastSearchContent = this.searchContent
                        this.currentPage = this.paramPage
                        this.goodsList = res.data.good_list
                        if (this.bannerPics.length === 0) {
                            for (let i = 0; i < res.data.good_list.length; i++) {
                                if (i < this.bannerNum) { // 给轮播图列表赋值，逻辑是将前六个商品图片赋值给轮播图列表
                                    const bannerObject = Object()
                                    bannerObject.url = this.goodsList[i].pics[0]
                                    bannerObject.link = ITEMDETAIL_URL + '?goodId=' + this.goodsList[i].id
                                    this.bannerPics.push(bannerObject)
                                }
                            }
                        }
                        for (let i = 0; i < res.data.good_list.length; i++) {
                            this.goodsList[i].pics = this.goodsList[i].pics[0] // 将商品的第一个图片作为展示图片
                        }
                        this.pageCount = res.data.total_num / this.pageSize * 10 // 给页面总数赋值
                        if (res.data.total_num === 0) {
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
                this.$router.push({ path: ITEMDETAIL_URL, query: { goodId: id } })
            },
            addToCart (id) { // 点击加入购物车按钮将商品加入购物车
                this.goodInfo.id = id
                const updateInfo = {
                    id: this.goodInfo.id,
                    num: 1
                }
                if (this.goodInfo.id) {
                    this.$http.post(ADD_CART_GOODS_URL, { goodInfo: updateInfo }).then(res => {
                        // eslint-disable-next-line no-empty
                        if (res && res.result === true) {
                            this.handleError({ theme: 'success' }, res.message)
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
                this.currentPage = 1
                this.paramPage = this.currentPage
                // TODO: 对type和searchContent进行post获取新数据
                this.getGoods()
            },
            toIndex () { // 点击返回首页触发事件
                this.$router.go(0)
            },
            toShoppingCar () {
                this.$router.push({ path: 'shoppingCart' })
            },
            querySearch (queryString, cb) {
                const results = queryString ? this.typeList.filter(this.createFilter(queryString)) : this.typeList
                cb(results)
            },
            createFilter (queryString) {
                return (typeList) => {
                    return (typeList.type_name.toLowerCase().indexOf(queryString.toLowerCase()) === 0)
                }
            }
        }
    }
</script>

<style lang="postcss" scoped>
    .index-wrapper {
        width: 90%;
        margin: 0 auto;
        overflow: auto;
        .toCarTab {
            position: absolute;
            bottom: 180px;
            right: 100px;
            z-index: 1000;
            cursor: pointer;
            border-radius: 50%;
            width: 74px;
            height: 74px;
            border: 1px solid #979ba5;
            background: #fff;
            svg {
                margin-top: 18px;
                margin-left: 15px;
            }
        }
        .toCarTab:hover {
            box-shadow: 0px 0px 4px #888888;
            path {
                fill: #3a84ff;
            }
        }
        .banner {
            width: 100%;
            .swiper {
                margin: 0 auto;
                background-size: auto;
                width: 100%;
                height: 300px;
            }
            /deep/ .bk-swiper-main .bk-swiper-img {
                display: inline-block;
                height: 100%;
                width: 100%;
                margin: 0;
                background-size: auto;
                background-repeat: no-repeat;
                background-position: 50%;
            }
        }
        .search {
            margin: 10px auto;
            width: 80%;
            text-align: center;
            margin-left: 130px;
            display: flex;
            .returnIndex {
                width: 120px;
                line-height: 35px;
                margin-right: 20px;
            }
            .selectType {
                background-color: #f2f2f2;
            }
            .group-text {
                height: 36px;
            }
        }
        .goods {
            height: auto;
            width: 1040px;
            margin: 0 auto;
            overflow: hidden;
            .goodCard {
                width: 220px;
                height: 265px;
                display: inline-block;
                float: left;
                margin: 0 20px;
                /deep/ .bk-card-body {
                    width: 100%;
                    padding: 0;
                }
                .goodName {
                    font-size: 15px;
                    margin-left: 20px;
                }
                .goodPrice {
                    margin-top: 5px;
                    margin-left: 15px;
                    display: flex;
                    font-size: 10px;
                }
                .replace-addButton {
                    margin: 0 10px 5px 0;
                }
                .addButton {
                    text-align: right;
                    font-size: 5px;
                    margin: 0 10px 5px 0;
                }
                img {
                    width: 200px;
                }
                p {
                    &:last-child {
                        margin-bottom: 0;
                        color: #b2b1b1;
                        font-size: 10px;
                    }
                }
            }
        }
        .paginator {
            margin-top: 5px;
            width: 100%;
            display: inline-block;
        }
    }
</style>
