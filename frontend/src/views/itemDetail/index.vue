<template>
    <div class="itemDetail-wrapper">
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
    import mainIamge from '../../../static/images/nopic.png'
    export default {
        components: {
            bkZoomImage, bkInput, bkButton, bkTab, bkTabPanel
        },
        data () {
            return {
                mainIamge,
                goodPicList1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
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
                        value: ''
                    },
                    {
                        title: '物品名称',
                        value: ''
                    },
                    {
                        title: '物品编码',
                        value: ''
                    },
                    {
                        title: '备注',
                        value: ''
                    }
                ],
                goodPicList: [],
                numberInputValue: '1',
                detailPanels: [
                    { name: 'detail', label: '商品详情', count: 10 },
                    { name: 'params', label: '参数规格', count: 20 }
                ],
                active: 'detail',
                markDownInfo: {
                    goodDetail: '',
                    goodParams: ''
                }
            }
        },
        created () {
            this.getDetailInfo()
        },
        methods: {
            getDetailInfo () {
                const goodId = 2
                this.$http.get('/purchase/get_good_detail?good_id=' + goodId).then((res) => {
                    if (res.result && res.data !== null) {
                        this.infoDetailList[0].value = '￥' + res.data.price
                        this.infoDetailList[1].value = res.data.good_name
                        this.infoDetailList[2].value = res.data.good_code
                        this.infoDetailList[3].value = res.data.remark
                        if (res.data.pics.length !== 0) {
                            if (res.data.pics[0] === '') {
                                this.mainIamge = '../../../static/images/nopic.png'
                            } else {
                                this.goodPicList = res.data.pics
                                this.mainIamge = this.goodPicList[0]
                            }
                        } else {
                            this.mainIamge = '../../../static/images/nopic.png'
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
