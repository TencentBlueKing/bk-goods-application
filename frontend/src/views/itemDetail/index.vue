<template>
    <div class="itemDetail-wrapper">
        <div class="toCarTab" @click="toShoppingCar">
            <svg t="1641539862015" class="icon" viewBox="0 0 1028 1024" version="1.1" p-id="2153" width="40" height="40">
                <path d="M332.8 790.528q19.456 0 36.864 7.168t30.208 19.968 20.48 30.208 7.68 36.864-7.68 36.864-20.48 30.208-30.208 20.48-36.864 7.68q-20.48 0-37.888-7.68t-30.208-20.48-20.48-30.208-7.68-36.864 7.68-36.864 20.48-30.208 30.208-19.968 37.888-7.168zM758.784 792.576q19.456 0 37.376 7.168t30.72 19.968 20.48 30.208 7.68 36.864-7.68 36.864-20.48 30.208-30.72 20.48-37.376 7.68-36.864-7.68-30.208-20.48-20.48-30.208-7.68-36.864 7.68-36.864 20.48-30.208 30.208-19.968 36.864-7.168zM930.816 210.944q28.672 0 44.544 7.68t22.528 18.944 6.144 24.064-3.584 22.016-13.312 37.888-22.016 62.976-23.552 68.096-18.944 53.248q-13.312 40.96-33.28 56.832t-49.664 15.872l-35.84 0-65.536 0-86.016 0-96.256 0-253.952 0 14.336 92.16 517.12 0q49.152 0 49.152 41.984 0 20.48-9.728 35.84t-38.4 14.336l-49.152 0-94.208 0-118.784 0-119.808 0-99.328 0-55.296 0q-20.48 0-34.304-9.216t-23.04-24.064-14.848-32.256-8.704-32.768q-1.024-6.144-5.632-29.696t-11.264-58.88-14.848-78.848-16.384-87.552q-19.456-103.424-44.032-230.4l-76.8 0q-15.36 0-25.6-7.68t-16.896-18.432-9.216-23.04-2.56-22.528q0-20.48 13.824-33.792t37.376-12.288l103.424 0q20.48 0 32.768 6.144t19.456 15.36 10.24 18.944 5.12 16.896q2.048 8.192 4.096 23.04t4.096 30.208q3.072 18.432 6.144 38.912l700.416 0zM892.928 302.08l-641.024-2.048 35.84 185.344 535.552 1.024z" p-id="2154" fill="#bfbfbf">
                </path>
            </svg>
        </div>
        <div class="good-info-wapper">
            <div class="good-pic">
                <div class="main-pic">
                    <bk-zoom-image :src="mainIamge" class="zoom-image"></bk-zoom-image>
                </div>
                <div class="pic-list">
                    <div class="pic-slide-btn" :class="{ 'ban-btn': slideIndex.nowFirst === 1 }" @click="picSlide('forward')">
                        <bk-icon type="arrows-m-left-shape" />
                    </div>
                    <div class="pic-item-wapper">
                        <ul id="item-list">
                            <li v-for="(item,index) in goodPicList" :key="index"
                                @mouseover="picMouseOver('pic-item' + index, item)"
                            >
                                <img :id="'pic-item' + index" :src="item" alt="">
                            </li>
                        </ul>
                    </div>
                    <div class="pic-slide-btn" :class="{ 'ban-btn': slideIndex.nowEnd === goodPicList.length }" @click="picSlide('backward')">
                        <bk-icon type="arrows-m-right-shape" />
                    </div>
                </div>
            </div>
            <div class="good-content">
                <div class="info-content-wapper">
                    <div class="goods-title">
                        {{infoDetailList[1].value}}
                    </div>
                    <div class="info-detail">
                        <div class="detail-item" v-for="(item,index) in infoDetailList" :key="index" v-show="item.value !== '正常'">
                            <div class="detail-title">{{item.title}}</div>
                            <div class="detail-value">{{item.value}}</div>
                        </div>
                    </div>
                    <div class="buy-goods">
                        <bk-input class="count-btn" type="number" :max="1000" :min="1" precision="0" v-model="numberInputValue"></bk-input>
                        <bk-button class="push-btn" theme="primary" title="加入购物车" @click="addToCar">
                            加入购物车
                        </bk-button>
                    </div>
                </div>
            </div>
        </div>
        <div class="good-detail-wapper">
            <bk-tab @tab-change="changeDetailTab" :active.sync="active" type="unborder-card">
                <bk-tab-panel v-for="(panel, index) in detailPanels" v-bind="panel" :key="index">
                    <v-md-preview v-if="index === 0" :text="markDownInfo.goodDetail"></v-md-preview>
                    <v-md-preview v-else :text="markDownInfo.goodParams"></v-md-preview>
                </bk-tab-panel>
            </bk-tab>
        </div>
    </div>
</template>

<script>
    import { bkZoomImage, bkInput, bkButton, bkTab, bkTabPanel } from 'bk-magic-vue'
    // import mainIamge from
    export default {
        components: {
            bkZoomImage, bkInput, bkButton, bkTab, bkTabPanel
        },
        data () {
            return {
                mainIamge: '/static/images/nopic.png',
                defaultPicNum: 4,
                picSize: 108,
                slideIndex: {
                    nowFirst: 1,
                    nowEnd: 1,
                    nowTranX: 0
                },
                lastOverPicId: '',
                infoDetailList: [
                    {
                        title: '参考价',
                        value: '暂无'
                    },
                    {
                        title: '物品名称',
                        value: '暂无'
                    },
                    {
                        title: '物品编码',
                        value: '暂无'
                    },
                    {
                        title: '备注',
                        value: '暂无'
                    }
                ],
                goodPicList: [],
                numberInputValue: 1,
                detailPanels: [
                    { name: 'detail', label: '商品详情', count: 10 },
                    { name: 'params', label: '参数规格', count: 20 }
                ],
                active: 'detail',
                markDownInfo: {
                    goodDetail: '',
                    goodParams: ''
                },
                goodInfo: {},
                curUsername: '',
                goodId: 6
            }
        },
        created () {
            this.curUsername = this.$store.getters.user.username
            if (this.$route.query.goodId === undefined || this.$route.query.goodId === null) {
                this.$bkMessage({
                    message: '物品ID获取失败',
                    offsetY: 80,
                    theme: 'error'
                })
            } else {
                this.goodId = this.$route.query.goodId
                this.getDetailInfo()
            }
        },
        methods: {
            getDetailInfo () {
                this.$http.get('/purchase/get_good_detail?good_id=' + this.goodId).then((res) => {
                    if (res.result && res.data !== null) {
                        this.goodInfo = res.data
                        this.infoDetailList[0].value = '￥' + res.data.price
                        this.infoDetailList[1].value = res.data.good_name
                        this.infoDetailList[2].value = res.data.good_code
                        this.infoDetailList[3].value = res.data.remark
                        if (res.data.pics.length !== 0) {
                            if (res.data.pics[0] === '') {
                                this.mainIamge = '/static/images/nopic.png'
                            } else {
                                this.goodPicList = res.data.pics
                                this.mainIamge = this.goodPicList[0]
                            }
                        } else {
                            this.mainIamge = '/static/images/nopic.png'
                        }
                        this.markDownInfo.goodDetail = res.data.introduce.replace(/\\n/g, '\n')
                        this.markDownInfo.goodParams = res.data.specifications.replace(/\\n/g, '\n')
                        this.slideIndex.nowEnd = this.goodPicList.length > this.defaultPicNum ? this.defaultPicNum : this.goodPicList.length
                    } else {
                        this.$bkMessage({
                            message: res.message,
                            offsetY: 80,
                            theme: 'error'
                        })
                    }
                }).catch(() => {
                    this.$bkMessage({
                        message: 'get_good_detail接口报错',
                        offsetY: 80,
                        theme: 'error'
                    })
                })
            },
            // 图片滑动事件
            picSlide (sildeType) {
                if (sildeType === 'forward') {
                    if (this.slideIndex.nowFirst > 1) {
                        const IndexGap = this.slideIndex.nowFirst - 1
                        if (IndexGap >= this.defaultPicNum) {
                            this.slideIndex.nowTranX += this.picSize * this.defaultPicNum
                            this.slideIndex.nowEnd -= this.defaultPicNum
                            this.slideIndex.nowFirst = this.slideIndex.nowEnd - 3
                        } else {
                            this.slideIndex.nowTranX += this.picSize * IndexGap
                            this.slideIndex.nowEnd -= IndexGap
                            this.slideIndex.nowFirst = this.slideIndex.nowEnd - 3
                        }
                        document.querySelector('#item-list').style.transform = 'translateX(' + this.slideIndex.nowTranX + 'px)'
                    }
                } else {
                    if (this.slideIndex.nowEnd < this.goodPicList.length) {
                        const IndexGap = this.goodPicList.length - this.slideIndex.nowEnd
                        if (IndexGap >= this.defaultPicNum) {
                            this.slideIndex.nowTranX += -this.picSize * this.defaultPicNum
                            this.slideIndex.nowFirst += this.defaultPicNum
                            this.slideIndex.nowEnd = this.slideIndex.nowFirst + this.defaultPicNum - 1
                        } else {
                            this.slideIndex.nowTranX += -this.picSize * IndexGap
                            this.slideIndex.nowFirst += IndexGap
                            this.slideIndex.nowEnd = this.slideIndex.nowFirst + this.defaultPicNum - 1
                        }
                        document.querySelector('#item-list').style.transform = 'translateX(' + this.slideIndex.nowTranX + 'px)'
                    }
                }
            },
            picMouseOver (picDomId, picUrl) {
                if (this.lastOverPicId !== '') {
                    document.querySelector('#' + this.lastOverPicId).style.border = '0'
                }
                document.querySelector('#' + picDomId).style.border = '2px solid #e53e41'
                this.lastOverPicId = picDomId
                this.mainIamge = picUrl
            },
            changeDetailTab (name) {
                if (name === this.detailPanels[0].name) {
                    console.log('当前是:' + this.detailPanels[0].label)
                } else {
                    console.log('当前是:' + this.detailPanels[1].label)
                }
            },
            addToCar () {
                const updateInfo = {
                    num: parseInt(this.numberInputValue),
                    id: this.goodInfo.id
                }
                this.$http.post(
                    '/purchase/add_cart_goods',
                    {
                        goodInfo: updateInfo
                    }
                ).then((res) => {
                    if (res.result) {
                        this.$bkMessage({
                            message: '物资已加入购物车',
                            theme: 'success'
                        })
                    } else {
                        this.$bkMessage({
                            message: '物资加入购物车失败',
                            offsetY: 80,
                            theme: 'error'
                        })
                    }
                }).catch(() => {
                    this.$bkMessage({
                        message: 'update_cart_goods接口报错',
                        offsetY: 80,
                        theme: 'error'
                    })
                }).finally(() => {
                   
                })
            },
            toShoppingCar () {
                this.$router.push({ path: 'shoppingcart' })
            }
        }
    }
</script>

<style scoped lang="postcss">
    @import './index.css';
    .itemDetail-wrapper{
        height: 100%;
        width:  76%;
        margin: 0 auto;
        .toCarTab{
            position: absolute;
            bottom: 180px;
            right: 100px;
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
        .good-info-wapper{
            width: 100%;
            border-bottom: 1px solid #EAEBF0;
            display: flex;
            .good-pic{
                height: 100%;
                width: 480px;
                padding: 10px;
                .main-pic{
                    width: 460px;
                    height: 460px;
                    border: 1px solid #999;
                    .zoom-image{
                        height: 100%;
                             width: 100%;
                         /deep/ .bk-full-screen{
                              z-index: 1002 !important;
                         }
                         img{
                             height: 100%;
                             width: 100%;
                         }
                    }
                }
                .pic-list{
                    display: flex;
                    flex-wrap: nowrap;
                    height: 108px;
                    margin-top: 10px;
                    .my-enter,.my-leave-to{
                        opacity: 0;
                        transform: translateX(80px);
                    }
                    .my-enter-active,.my-leave-active{
                        transition: all 0.5S ease
                    }
                    .pic-item-wapper{
                        width: 676px;
                        height: 108px;
                        display: flex;
                        flex-wrap: nowrap;
                        overflow: hidden;
                        ul{
                            transition: transform 0.5s ease-in-out;
                            width: 100%;
                            height: 100%;
                            display: flex;
                            flex-wrap: nowrap;
                            img{
                                margin: 4px;
                                width: 100px;
                                height: 100px;
                            }
                        }
                    }
                    .pic-slide-btn{
                        width: 20px;
                        height: 100%;
                        background: #EAEBF0;
                        cursor: pointer;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    }
                    .ban-btn{
                        color: #C4C6CC !important;
                        cursor: default !important;
                    }
                }
            }
            .good-content{
                height: 100%;
                width: calc(100% - 480px);
                padding: 10px 10px 10px 30px;
                border-left: 1px solid #EAEBF0;
                .info-content-wapper{
                    .goods-title{
                        font-size: 22px;
                        font-weight: bold;
                        color: #313238;
                        margin-bottom: 20px;
                    }
                    .info-detail{
                        width: 100%;
                        margin-bottom: 20px;
                        .detail-item{
                            display: flex;
                            font-size: 16px;
                            margin-bottom: 14px;
                            .detail-title{
                                width: 80px;
                            }
                            .detail-value{
                                width: calc(100% - 80px);
                                padding-left: 10px;
                                max-height: 200px;
                                overflow: auto;
                            }
                            .abnormal{
                                font-weight: bold;
                            }
                        }
                    }
                    .buy-goods{
                        display: flex;
                        height: 80px;
                        .count-btn{
                            width: 86px;
                            /deep/ .bk-input-number{
                                input{
                                    height: 50px !important;
                                }
                            }
                        }
                        .push-btn{
                            width: 130px;
                            height: 50px;
                            font-size: 16px;
                        }
                    }
                }
            }
        }
    }
</style>
