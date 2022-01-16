<template>
    <div class="shopcart-wrapper">
        <div class="cart-body-wapper">
            <div class="header-wapper">
                <div class="head-total-info">
                    <span>全部物资</span>
                    <bk-tag radius="10px">{{allGoodsCount}}</bk-tag>
                </div>
            </div>
            <div class="content-wapper">
                <div class="goods-type-list" v-for="(item,index) in cartList" :key="index">
                    <div class="type-item-wapper">
                        <div class="type-title">
                            <bk-tag theme="info">{{item.goods_type_name}}</bk-tag>
                        </div>
                        <div class="goods-item-list">
                            <bk-table
                                :ref="'typeTable' + item.goods_type_id"
                                @select="rowSelectChange"
                                @select-all="(val) => tableSelectAll(val,index)"
                                ext-cls="type-table"
                                :data="item.goods_list"
                                :size="size"
                                :outer-border="false"
                                :header-border="false"
                                :header-cell-style="{ background: '#fff' }"
                            >
                                <bk-table-column type="selection" width="60"></bk-table-column>
                                <bk-table-column label="物资编码" prop="good_code"></bk-table-column>
                                <bk-table-column label="物资名称" prop="good_name"></bk-table-column>
                                <bk-table-column label="参考价格" prop="price"></bk-table-column>
                                <bk-table-column label="数量">
                                    <template slot-scope="props">
                                        <bk-input @change="(value, event) => goodNumChange(value, event, props.row)"
                                            type="number" :max="1000" :min="1"
                                            v-model="props.row.num"
                                        ></bk-input>
                                    </template>
                                </bk-table-column>
                                <bk-table-column label="操作" width="150">
                                    <template slot-scope="props">
                                        <bk-button class="mr10" theme="primary" text @click="showRemoveBox(props.row, 'table')">移除</bk-button>
                                    </template>
                                </bk-table-column>
                            </bk-table>
                        </div>
                    </div>
                </div>
            </div>
            <div style="width:100%;height: 62px;">
                <!-- 占位 -->
            </div>
        </div>
        <div class="fun-bar-wapper">
            <div class="fun-list-wapper">
                <div class="select-fun">
                    <bk-checkbox
                        :true-value="'yes'"
                        :false-value="'no'"
                        ext-cls="select-all"
                        @change="allCheckChange"
                        v-model="allSelectVal">
                        全选
                    </bk-checkbox>
                    <div class="delete-btn" @click="showRemoveBox('','bottom')">
                        删除
                    </div>
                </div>
                <div class="total-info">
                    <div class="total-select">
                        已选物资
                        <span>{{selectedCount}}</span>
                        件
                    </div>
                    <div class="total-price">{{'合计：' + selectedPrice}}</div>
                </div>
            </div>
            <div class="export-btn" title="导出" @click="exportCart">
                <bk-icon type="download" />
            </div>
            <div class="submit-btn" :class="{ 'un-submit': selectedCount === 0 }" @click="submitCart">
                申请
            </div>
        </div>
    </div>
</template>

<script>
    import { bkTable, bkTableColumn, bkButton } from 'bk-magic-vue'
    export default {
        components: {
            bkTable,
            bkTableColumn,
            bkButton
        },
        data () {
            return {
                cartUsername: '',
                allSelectVal: false,
                size: 'small',
                cartList: [],
                allGoodsCount: 0,
                selectGoodsList: [],
                selectedCount: 0,
                selectedPrice: 0,
                timer: null,
                changeGoodsList: []
            }
        },
        computed: {
        },
        watch: {
            selectGoodsList: {
                handler (val) {
                    this.selectedCount = 0
                    this.selectedPrice = 0
                    val.forEach((good) => {
                        if (good.selected) {
                            this.selectedCount++
                            this.cartList[good.table_index].goods_list.forEach((item) => {
                                if (good.id === item.id) {
                                    this.selectedPrice += item.num * item.price
                                }
                            })
                        }
                    })
                    this.selectedPrice = this.selectedPrice.toFixed(2)
                    this.allGoodsCount = val.length
                    this.allSelectVal = (this.selectedCount === this.allGoodsCount && this.allGoodsCount !== 0) ? 'yes' : 'no'
                },
                deep: true
            }
        },
        created () {
            
        },
        mounted () {
            this.getUserInfo()
            this.getCartList()
        },
        methods: {
            getUserInfo () {
                this.cartUsername = localStorage.getItem('username')
            },
            getCartList () {
                if (this.cartUsername !== '') {
                    this.$http.get('/purchase/get_shopping_car?userName=' + this.cartUsername).then((res) => {
                        if (res.result && res.data !== null) {
                            this.allGoodsCount = 0
                            if (res.data.length !== 0) {
                                this.allGoodsCount = 0
                                this.cartList = JSON.parse(JSON.stringify(res.data))
                                this.cartList.forEach((typeItem, typeIndex) => {
                                    this.allGoodsCount += typeItem.goods_list.length
                                    typeItem.goods_list.forEach((good) => {
                                        good['table_index'] = typeIndex
                                    })
                                })
                                // 初始化购物车选择状态数组
                                this.selectGoodsList = []
                                JSON.parse(JSON.stringify(this.cartList)).forEach((typeItem) => {
                                    typeItem.goods_list.forEach((good) => {
                                        good.selected = false
                                        this.selectGoodsList.push(good)
                                    })
                                })
                            }
                        } else {
                            this.$bkMessage({
                                message: res.message,
                                offsetY: 80,
                                theme: 'error'
                            })
                        }
                    }).catch(() => {
                        this.$bkMessage({
                            message: 'get_shopping_car接口报错',
                            offsetY: 80,
                            theme: 'error'
                        })
                    })
                } else {
                    this.$bkMessage({
                        message: '用户信息获取失败',
                        offsetY: 80,
                        theme: 'error'
                    })
                }
            },
            showRemoveBox (row, type) {
                let deleteList = []
                if (type === 'table') {
                    deleteList.push(row)
                } else {
                    // 底部删除按钮
                    deleteList = this.getSelectedGoodsList()
                }
                if (deleteList.length === 0) {
                    return
                }
                this.$bkInfo({
                    title: '确定要删除该物资吗？',
                    confirmFn: async () => {
                        try {
                            // await this.deleteTableGoods(deleteList)
                            await this.deleteCartList(deleteList)
                            this.recoverSelected()
                            this.$bkMessage({
                                message: '删除成功',
                                theme: 'success'
                            })
                            return true
                        } catch (e) {
                            console.warn(e)
                            return false
                        }
                    }
                })
            },
            deleteTableGoods (deleteList) {
                // 在页面删除物资
                deleteList.forEach((item) => {
                    this.cartList[item.table_index].goods_list = this.cartList[item.table_index].goods_list.filter((good) => {
                        return item.id !== good.id
                    })
                })
                // 删除空表
                this.cartList = this.cartList.filter((typeItem) => {
                    return typeItem.goods_list.length !== 0
                })
                // 更新selectlist
                this.selectGoodsList = []
                this.cartList.forEach((typeItem) => {
                    typeItem.goods_list.forEach((good) => {
                        this.selectGoodsList.push(good)
                    })
                })
            },
            deleteCartList (deleteList) {
                // 在数据库中删除物资
                const idList = []
                deleteList.forEach((item) => {
                    idList.push(item.id)
                })
                this.$http.post('/purchase/delete_cart_goods', { goodsIdList: idList }).then((res) => {
                    if (res.result) {
                        this.deleteTableGoods(deleteList)
                    } else {
                        this.$bkMessage({
                            message: res.message,
                            offsetY: 80,
                            theme: 'error'
                        })
                    }
                }).catch(() => {
                    this.$bkMessage({
                        message: 'delete_cart_goods接口报错',
                        offsetY: 80,
                        theme: 'error'
                    })
                })
            },
            recoverSelected () {
                this.cartList.forEach((typeItem, typeIndex) => {
                    typeItem.goods_list.forEach((good, goodIndex) => {
                        good['table_index'] = typeIndex
                        this.selectGoodsList.forEach((selectGood) => {
                            if (selectGood.id === good.id && selectGood.selected) {
                                this.$refs['typeTable' + typeItem.goods_type_id][0].toggleRowSelection(this.cartList[typeIndex].goods_list[goodIndex], true)
                            }
                        })
                    })
                })
            },
            rowSelectChange (selection, row) {
                this.selectGoodsList.forEach((good) => {
                    if (row.good_code === good.good_code) {
                        good.selected = !good.selected
                    }
                })
            },
            tableSelectAll (selection, tableIndex) {
                this.cartList[tableIndex].goods_list.forEach((good) => {
                    this.selectGoodsList.forEach((item) => {
                        if (item.good_code === good.good_code) {
                            item.selected = (selection.length !== 0)
                        }
                    })
                })
            },
            allCheckChange () {
                this.cartList.forEach((typeItem) => {
                    this.$refs['typeTable' + typeItem.goods_type_id][0].clearSelection()
                })
                if (this.allSelectVal === 'yes') {
                    this.cartList.forEach((typeItem) => {
                        this.$refs['typeTable' + typeItem.goods_type_id][0].toggleAllSelection()
                    })
                }
                this.selectGoodsList.forEach((good) => {
                    good.selected = (this.allSelectVal === 'yes')
                })
            },
            goodNumChange (value, event, row) {
                this.changeGoodsList.push(row)
                // 修改物资数量(节流)
                if (this.timer) return
                this.timer = setTimeout(() => {
                    this.updateGoodsNum()
                }, 3000)
            },
            updateGoodsNum () {
                const uqChangeGoodsList = new Set(this.changeGoodsList)
                const updateList = []
                uqChangeGoodsList.forEach((changeGood) => {
                    if (this.cartList[changeGood.table_index] !== null && this.cartList[changeGood.table_index].length !== 0) {
                        this.cartList[changeGood.table_index].goods_list.forEach((good) => {
                            if (good.id === changeGood.id) {
                                updateList.push(good)
                            }
                        })
                    }
                })
                this.$http.post(
                    '/purchase/update_cart_goods',
                    {
                        goodsList: updateList
                    }
                ).then((res) => {
                    if (!res.result) {
                        this.$bkMessage({
                            message: '物资数量更新失败',
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
                    this.timer = null
                    this.changeGoodsList = []
                })
            },
            submitCart () {
                if (this.selectedCount > 0) {
                    this.$bkInfo({
                        title: '确定要提交申请吗？',
                        confirmFn: async () => {
                            try {
                                const selectedList = this.getSelectedGoodsList()
                                this.$http.post(
                                    '/purchase/update_group_apply',
                                    {
                                        userName: this.cartUsername,
                                        cartList: selectedList
                                    }
                                ).then((res) => {
                                    if (!res.result) {
                                        this.$bkMessage({
                                            message: res.message,
                                            offsetY: 80,
                                            theme: 'error'
                                        })
                                    } else {
                                        this.deleteCartList(selectedList)
                                        this.$bkMessage({
                                            message: '申请成功',
                                            theme: 'success'
                                        })
                                    }
                                }).catch(() => {
                                    this.$bkMessage({
                                        message: 'apply_cart_goods接口报错',
                                        offsetY: 80,
                                        theme: 'error'
                                    })
                                }).finally(() => {
                                    this.timer = null
                                    this.changeGoodsList = []
                                })
                                return true
                            } catch (e) {
                                console.warn(e)
                                return false
                            }
                        }
                    })
                }
            },
            getSelectedGoodsList () {
                const selectedList = []
                this.selectGoodsList.forEach((good) => {
                    this.cartList[good.table_index].goods_list.forEach((item) => {
                        if (good.id === item.id && good.selected) {
                            selectedList.push(item)
                        }
                    })
                })
                return selectedList
            },
            exportCart () {
                const submitGoods = { selectedRows: this.getSelectedGoodsList() }
                this.$http.post('/purchase/derive_excel',
                                { model: 2, dataList: submitGoods })
                    .then((res) => {
                        if (res.result) {
                            this.$bkMessage({
                                message: '购物车导出成功',
                                offsetY: 80,
                                theme: 'error'
                            })
                        }
                    }).catch(() => {
                        this.$bkMessage({
                            message: 'derive_excel接口报错',
                            offsetY: 80,
                            theme: 'error'
                        })
                    })
            }
        }
    }
</script>

<style scoped lang="postcss">
    @import './index.css';
    .shopcart-wrapper{
        height: 100%;
        width: 76%;
        margin: 0 auto;
    }
    .cart-body-wapper{
        width: 100%;
        padding: 10px;
        .header-wapper{
            width: 100%;
            height: 50px;
            display: flex;
            border-bottom: 1px solid #C4C6CC;
            margin-bottom: 20px;
            .head-total-info{
                line-height: 50px;
                padding: 0 18px;
                font-size: 16px;
                min-width: 100px;
                span{
                    font-weight: bold;
                }
                .bk-tag{
                    font-size: 14px;
                    margin: 0 !important;
                }
            }
        }
        .goods-type-list{
            width: 100%;
            margin-bottom: 40px;
            .type-item-wapper{
                width: 100%;
                .type-title{
                    padding-left: 10px;
                    height: 36px;
                    line-height: 34px;
                    /deep/.bk-tag{
                        font-size: 16px;
                    }
                }
                .goods-item-list{
                    width: 100%;
                    .type-table{
                        font-size: 14px;
                        /deep/ .bk-table-row .cell .bk-input-number{
                            max-width: 100px;
                            font-size: 14px;
                        }
                    }
                }
            }
        }
    }
    .fun-bar-wapper{
        position: fixed;
        z-index: 1111;
        bottom: 85px;
        width: calc(76% - 80px) ;
        height: 60px;
        background: #EAEBF0;
        display: flex;
        justify-content: space-between;
        .fun-list-wapper{
            width: calc(100% - 120px);
            height: 100%;
            display: flex;
            flex-wrap: nowrap;
            justify-content: space-between;
            .select-fun{
                display: flex;
                align-items: center;
                padding-left: 10px;
                .select-all {
                    height: 100%;
                    width: 100%;
                    line-height: 60px;
                    /deep/ .bk-checkbox-text{
                        font-size: 20px;
                        font-family: monospace;
                    }
                }
                .delete-btn{
                    font-size: 20px;
                    width: 80px;
                }
                .delete-btn:hover{
                    color: #1768EF;
                    text-decoration: underline;
                    cursor: pointer;
                }
            }
            .total-info{
                display: flex;
                .total-select{
                    font-size: 18px;
                    line-height: 60px;
                    color: #000;
                    margin-right: 20px;
                    span{
                        color: #1768EF;
                    }
                }
                .total-price{
                    font-size: 18px;
                    line-height: 60px;
                    color: #000;
                    margin-right: 16px;
                }
            }
        }
        .submit-btn{
            width: 120px;
            height: 100%;
            line-height: 60px;
            background: #1768EF;
            font-size: 24px;
            text-align: center;
            color: #fff;
            font-weight: bold;
            cursor: pointer;
        }
        .un-submit{
            cursor:not-allowed;
            background: #979BA5;
        }
        .export-btn{
            width: 50px;
            height: 100%;
            line-height: 60px;
            font-size: 24px;
            i{
                cursor: pointer;
            }
        }
    }
</style>
