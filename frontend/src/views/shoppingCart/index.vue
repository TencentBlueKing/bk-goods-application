<template>
    <div class="shopcart-wrapper">
        <div class="header" v-if="!isAdmin">
            <bk-divider align="left"><bk-tag type="filled" style="font-size: 13px"><span>购物车</span></bk-tag></bk-divider>
        </div>
        <div class="header" v-if="isAdmin">
            <bk-divider align="left"><bk-tag type="filled" style="font-size: 13px"><span>物资导入及申请</span></bk-tag></bk-divider>
        </div>
        <div class="cart-body-wapper">
            <div class="header-wapper">
                <div class="head-total-info">
                    <span>全部物资</span>
                    <bk-tag radius="10px">{{allGoodsCount}}</bk-tag>
                </div>
                <div class="import-btn" v-if="isAdmin">
                    <bk-upload
                        :theme="'button'"
                        :with-credentials="true"
                        :custom-request="upload"
                        :size="50"
                        :files="excelFiles"
                        :accept="'.xls, .xlsx'"
                        :limit="1"
                    ></bk-upload>
                </div>
                <bk-button v-if="!isAdmin" theme="primary" title="导出" class="mr10" @click="exportCart()">
                    导出
                </bk-button>
            </div>
            <div class="content-wapper">
                <div class="goods-type-list" v-if="(cartList.length === 0 && isAdmin === false) || (applyCartList.length === 0 && isAdmin === true)">
                    <div class="empty-cart">
                        <svg t="1642558051352" class="icon" viewBox="0 0 1024 1024" version="1.1" p-id="5516" width="200" height="200">
                            <path d="M64 409l227.038-152.906A24 24 0 0 1 304.444 252h417.194a24 24 0 0 1 13.492 4.151L960 409v339c0 13.255-10.745 24-24 24H88c-13.255 0-24-10.745-24-24V409z" fill="#9F9F9F" fill-opacity=".5" p-id="5517"></path>
                            <path d="M64 409h283.136c13.255 0 24 10.745 24 24v44.68c0 13.254 10.745 24 24 24h233.136c13.255 0 24-10.746 24-24V433c0-13.255 10.745-24 24-24H960v355a8 8 0 0 1-8 8H72a8 8 0 0 1-8-8V409z" fill="#FFFFFF" fill-opacity=".4" p-id="5518"></path>
                        </svg>
                        <div>暂无物资信息</div>
                    </div>
                </div>
                <div class="user" v-if="!isAdmin">
                    <div class="goods-type-list" v-for="(item,index) in cartList" :key="index">
                        <div class="type-item-wapper">
                            <div class="type-title">
                                <bk-tag theme="info">{{item.goods_type_name}}</bk-tag>
                                <bk-button v-if="isAdmin" theme="primary" title="申请" class="mr10" @click="submitApply(item,index)">
                                    申请
                                </bk-button>
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
                <div class="admin" v-if="isAdmin">
                    <div class="goods-type-list" v-for="(item,index) in applyCartList" :key="index">
                        <div class="type-item-wapper">
                            <div class="type-title">
                                <bk-tag theme="info">{{item.goods_type_name}}</bk-tag>
                                <bk-button v-if="isAdmin" theme="primary" title="申请" class="mr10" @click="submitApply(item,index)">
                                    申请
                                </bk-button>
                            </div>
                            <div>
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
                                    <bk-table-column label="使用人" prop="username"></bk-table-column>
                                    <bk-table-column label="配送地区" prop="position"></bk-table-column>
                                    <bk-table-column show-overflow-tooltip="true" label="备注" prop="remarks"></bk-table-column>
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
                                            <bk-button class="mr10" theme="primary" text @click="showAdminRemoveBox(props.row)">移除</bk-button>
                                        </template>
                                    </bk-table-column>
                                </bk-table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div style="width:100%;height: 62px;">
                <!-- 占位 -->
            </div>
        </div>
        <!-- <div v-if="false" class="fun-bar-wapper">
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
            <div class="submit-btn" :class="{ 'un-submit': selectedCount === 0 }" @click="submitAllCart">
                {{isAdmin ? "保存" : "申请"}}
            </div>
        </div> -->
    </div>
</template>

<script>
    import { mapState } from 'vuex'
    import { bkTable, bkTableColumn, bkButton } from 'bk-magic-vue'
    import {
        GET_SHOPPING_CART_URL, DELETE_CART_GOODS_URL, UPDATE_GROUP_APPLY_URL, UPDATE_CART_GOODS_URL, DERIVE_EXCEL_URL,
        GET_GROUP_APPLY_URL, DELETE_GROUP_APPLY_URL, IMPORT_EXCEL_URL, DEL_EXCEL_URL
    } from '@/pattern'
    export default {
        components: {
            bkTable,
            bkTableColumn,
            bkButton
        },
        data () {
            return {
                isAdmin: false,
                curUsername: '',
                allSelectVal: false,
                size: 'medium',
                cartList: [],
                applyCartList: [],
                allGoodsCount: 0,
                selectGoodsList: [],
                selectAppliesList: [],
                selectedCount: 0,
                selectedPrice: 0,
                timer: null,
                changeGoodsList: [],
                excelFiles: [], // 导入组件绑定列表
                fileCache: []
            }
        },
        computed: {
            ...mapState({
                userInfo: state => state.user.userInfo
            })
        },
        watch: {
            selectAppliesList: {
                handler (val) {
                    this.selectedCount = 0
                    this.selectedPrice = 0
                    val.forEach((good) => {
                        if (good.selected) {
                            this.selectedCount++
                            this.applyCartList[good.table_index].goods_list.forEach((item) => {
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
            },
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
            this.curUsername = this.userInfo.username // 从state中获取用户名
            this.isAdmin = this.userInfo.isAdmin
            if (this.isAdmin) {
                this.initCartData() // 若是管理员，则加载数据
            }
        },
        updated () {
            const importDom = document.querySelector('.file-wrapper')
            if (importDom !== undefined && importDom !== null) {
                document.querySelector('.file-wrapper').setAttribute('bk-lablename', '导入物资')
            }
        },
        methods: {
            initCartData () {
                if (this.isAdmin) {
                    this.getGroupApplyList()
                } else {
                    this.getCartList()
                }
            },
            getCartList () {
                if (this.curUsername !== '') {
                    this.$http.get(GET_SHOPPING_CART_URL).then((res) => {
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
            showAdminRemoveBox (row, type) {
                const deleteList = [row]
                this.$bkInfo({
                    title: '确定要删除该物资吗？',
                    confirmFn: async () => {
                        try {
                            // await this.deleteTableGoods(deleteList)
                            await this.deleteApplyList(deleteList)
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
                if (this.isAdmin === false) {
                    deleteList.forEach((item) => {
                        this.cartList[item.table_index].goods_list = this.cartList[item.table_index].goods_list.filter((good) => {
                            return item.id !== good.id
                        })
                    })
                    // 删除空表
                    this.cartList = this.cartList.filter((typeItem) => {
                        return typeItem.goods_list.length !== 0
                    })
                    // 更新selectGoodsList
                    this.selectGoodsList = []
                    this.cartList.forEach((typeItem) => {
                        typeItem.goods_list.forEach((good) => {
                            this.selectGoodsList.push(good)
                        })
                    })
                } else if (this.isAdmin === true) {
                    deleteList.forEach((item) => {
                        this.applyCartList[item.table_index].goods_list = this.applyCartList[item.table_index].goods_list.filter((good) => {
                            return item.id !== good.id
                        })
                    })
                    // 删除空表
                    this.applyCartList = this.applyCartList.filter((typeItem) => {
                        return typeItem.goods_list.length !== 0
                    })
                    // 更新selectAppliesList
                    this.selectAppliesList = []
                    this.applyCartList.forEach((typeItem) => {
                        typeItem.goods_list.forEach((good) => {
                            this.selectAppliesList.push(good)
                        })
                    })
                }
            },
            deleteCartList (deleteList) {
                // 在数据库中删除物资
                const idList = []
                deleteList.forEach((item) => {
                    idList.push(item.id)
                })
                this.$http.post(DELETE_CART_GOODS_URL, { cartIdList: idList }).then((res) => {
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
            deleteApplyList (deleteList) {
                const id = deleteList[0].id
                this.$http.post(DELETE_GROUP_APPLY_URL, { applyId: id }).then((res) => {
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
                if (this.isAdmin === false) {
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
                } else if (this.isAdmin === true) {
                    this.applyCartList.forEach((typeItem, typeIndex) => {
                        typeItem.goods_list.forEach((good, goodIndex) => {
                            good['table_index'] = typeIndex
                            this.selectAppliesList.forEach((selectGood) => {
                                if (selectGood.id === good.id && selectGood.selected) {
                                    this.$refs['typeTable' + typeItem.goods_type_id][0].toggleRowSelection(this.applyCartList[typeIndex].goods_list[goodIndex], true)
                                }
                            })
                        })
                    })
                }
            },
            rowSelectChange (selection, row) {
                if (this.isAdmin === false) {
                    this.selectGoodsList.forEach((good) => {
                        if (row.id === good.id) {
                            good.selected = !good.selected
                        }
                    })
                } else if (this.isAdmin === true) {
                    this.selectAppliesList.forEach((good) => {
                        if (row.id === good.id) {
                            good.selected = !good.selected
                        }
                    })
                }
            },
            tableSelectAll (selection, tableIndex) {
                if (this.isAdmin === false) {
                    this.cartList[tableIndex].goods_list.forEach((good) => {
                        this.selectGoodsList.forEach((item) => {
                            if (item.good_code === good.good_code) {
                                item.selected = (selection.length !== 0)
                            }
                        })
                    })
                } else if (this.isAdmin === true) {
                    this.applyCartList[tableIndex].goods_list.forEach((good) => {
                        this.selectAppliesList.forEach((item) => {
                            if (item.good_code === good.good_code) {
                                item.selected = (selection.length !== 0)
                            }
                        })
                    })
                }
            },
            allCheckChange () {
                if (this.isAdmin === false) {
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
                } else if (this.isAdmin === true) {
                    this.applyCartList.forEach((typeItem) => {
                        this.$refs['typeTable' + typeItem.goods_type_id][0].clearSelection()
                    })
                    if (this.allSelectVal === 'yes') {
                        this.applyCartList.forEach((typeItem) => {
                            this.$refs['typeTable' + typeItem.goods_type_id][0].toggleAllSelection()
                        })
                    }
                    this.selectAppliesList.forEach((good) => {
                        good.selected = (this.allSelectVal === 'yes')
                    })
                }
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
                if (this.isAdmin === false) {
                    uqChangeGoodsList.forEach((changeGood) => {
                        if (this.cartList[changeGood.table_index] !== null && this.cartList[changeGood.table_index].length !== 0) {
                            this.cartList[changeGood.table_index].goods_list.forEach((good) => {
                                if (good.id === changeGood.id) {
                                    updateList.push(good)
                                }
                            })
                        }
                    })
                } else if (this.isAdmin === true) {
                    uqChangeGoodsList.forEach((changeGood) => {
                        if (this.applyCartList[changeGood.table_index] !== null && this.applyCartList[changeGood.table_index].length !== 0) {
                            this.applyCartList[changeGood.table_index].goods_list.forEach((good) => {
                                if (good.id === changeGood.id) {
                                    updateList.push(good)
                                }
                            })
                        }
                    })
                }
                const updateUrl = this.isAdmin ? UPDATE_GROUP_APPLY_URL : UPDATE_CART_GOODS_URL
                const params = this.isAdmin ? { applyList: updateList, updateType: 'num' } : { goodsList: updateList }
                this.$http.post(updateUrl, params).then((res) => {
                    if (!res.result) {
                        this.$bkMessage({
                            message: '物资数量更新失败',
                            offsetY: 80,
                            theme: 'error'
                        })
                    }
                }).catch(() => {
                    this.$bkMessage({
                        message: updateUrl + '接口报错',
                        offsetY: 80,
                        theme: 'error'
                    })
                }).finally(() => {
                    this.timer = null
                    this.changeGoodsList = []
                })
            },
            submitAllCart () {
                if (this.selectedCount > 0) {
                    this.$bkInfo({
                        title: '确定要提交申请吗？',
                        confirmFn: async () => {
                            try {
                                const selectedList = this.getSelectedGoodsList()
                                this.$http.post(
                                    UPDATE_GROUP_APPLY_URL,
                                    {
                                        userName: this.curUsername,
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
                if (this.isAdmin === false) {
                    this.selectGoodsList.forEach((good) => {
                        this.cartList[good.table_index].goods_list.forEach((item) => {
                            if (good.id === item.id && good.selected) {
                                selectedList.push(item)
                            }
                        })
                    })
                } else if (this.isAdmin === true) {
                    this.selectAppliesList.forEach((good) => {
                        this.applyCartList[good.table_index].goods_list.forEach((item) => {
                            if (good.id === item.id && good.selected) {
                                selectedList.push(item)
                            }
                        })
                    })
                }
                return selectedList
            },
            exportCart () {
                const submitGoods = { selectedRows: [] }
                this.getSelectedGoodsList().forEach((good) => {
                    submitGoods.selectedRows.push(good.id)
                })
                if (submitGoods.selectedRows.length === 0) {
                    this.$bkMessage({
                        message: '请先选择物资',
                        offsetY: 80,
                        theme: 'warning'
                    })
                    return
                }
                this.$http.post(DERIVE_EXCEL_URL, { model: 2, dataList: submitGoods })
                    .then((res) => {
                        if (res.result) {
                            const link = document.createElement('a') // 生成a元素，用以实现下载功能
                            link.href = res.data.file_url
                            document.body.appendChild(link)
                            link.click()
                            document.body.removeChild(link)
                            const fileName = res.data.file_url.split('/').slice(-1)[0] // 获取文件名
                            const dirName = res.data.file_url.split('/').slice(-2, -1)[0] // 获取文件夹名
                            this.fileCache.push([fileName, dirName])
                            this.sleep(30 * 60).then(() => { // 半小时后删除excel文件
                                this.$http.post(DEL_EXCEL_URL, { dirName: this.fileCache[0][1], fileName: this.fileCache[0][0], username: this.curUsername }).then(() => {
                                    this.fileCache.shift()
                                })
                            })
                            this.$bkMessage({
                                message: '购物车导出成功',
                                offsetY: 80,
                                theme: 'success'
                            })
                        } else {
                            this.$bkMessage({
                                message: '购物车导出失败',
                                offsetY: 80,
                                theme: 'console.error();'
                            })
                        }
                    }).catch(() => {
                        // this.$bkMessage({
                        //     message: 'derive_excel接口报错',
                        //     offsetY: 80,
                        //     theme: 'error'
                        // })
                    })
            },
            getGroupApplyList () {
                this.$http.get(GET_GROUP_APPLY_URL).then((res) => {
                    if (res.result && res.data !== null) {
                        this.allGoodsCount = 0
                        this.applyCartList = JSON.parse(JSON.stringify(res.data))
                        this.applyCartList.forEach((typeItem, typeIndex) => {
                            this.allGoodsCount += typeItem.goods_list.length
                            typeItem.goods_list.forEach((good) => {
                                good['table_index'] = typeIndex
                            })
                        })
                        // 初始化购物车选择状态数组
                        this.selectAppliesList = []
                        JSON.parse(JSON.stringify(this.applyCartList)).forEach((typeItem) => {
                            typeItem.goods_list.forEach((good) => {
                                good.selected = false
                                this.selectAppliesList.push(good)
                            })
                        })
                    } else {
                        this.$bkMessage({
                            message: res.message,
                            offsetY: 80,
                            theme: 'error'
                        })
                    }
                }).catch(() => {
                    this.$bkMessage({
                        message: 'get_group_apply接口报错',
                        offsetY: 80,
                        theme: 'error'
                    })
                })
            },
            submitApply (tableItem, tableIndex) {
                const submitApplyList = this.selectAppliesList.filter((apply) => {
                    return apply.selected && apply.table_index === tableIndex
                })
                if (submitApplyList.length === 0) {
                    this.$bkMessage({
                        message: '请先选择物资',
                        offsetY: 80,
                        theme: 'warning'
                    })
                    return
                }
                this.$bkInfo({
                    title: '确定要提交' + tableItem.goods_type_name + '物资申请吗？',
                    confirmFn: async () => {
                        try {
                            this.$http.post(
                                UPDATE_GROUP_APPLY_URL,
                                {
                                    applyList: submitApplyList,
                                    updateType: 'status'
                                }
                            ).then((res) => {
                                if (!res.result) {
                                    this.$bkMessage({
                                        message: res.message,
                                        offsetY: 80,
                                        theme: 'error'
                                    })
                                } else {
                                    this.deleteTableGoods(submitApplyList)
                                    this.$bkMessage({
                                        message: '申请成功',
                                        theme: 'success'
                                    })
                                }
                            }).catch(() => {
                                this.$bkMessage({
                                    message: 'add_group_apply接口报错',
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
            },
            sleep (time) { // 计时器
                return new Promise((resolve, reject) => {
                    setTimeout(resolve, time * 1000)
                })
            },
            upload (file) { // 上传文件函数
                this.getBase64(file.fileObj.origin).then(res => {
                    const excelFile = res.split(',')[1] // 获取文件信息
                    const fileName = this.curUsername + '_' + file.fileObj.name // 获取文件名
                    this.$http.post(IMPORT_EXCEL_URL, { file: excelFile, fileName: fileName }).then(res => {
                        if (res && res.result === true && res.code === 200) { // 全部导入成功
                            this.handleError({ theme: 'success' }, res.message)
                        } else if (res && res.result === true && res.code === 5003) { // 存在导入失败物品
                            this.handleError({ theme: 'warning' }, '物资' + res.data.created_fail_list + '导入失败')
                            const link = document.createElement('a') // 生成a元素，用以实现下载功能
                            link.href = res.data.file_url
                            document.body.appendChild(link)
                            link.click()
                            document.body.removeChild(link)
                        } else if (res && res.result === false) { // 有错误
                            this.handleError({ theme: 'error' }, res.message)
                        }
                        this.excelFiles.push({ // 给上传组件绑定列表添加文件信息
                            name: fileName
                        })
                        this.excelFiles = []
                        this.handleError({ theme: 'warning' }, '3秒后刷新页面')
                        this.sleep(3).then(() => {
                            // const delDirPath = 'import_cart_excel' // 后台存放导入文件路径
                            // this.$http.post(DEL_EXCEL_URL, { dirName: delDirPath, fileName: fileName, username: this.curUsername }).then(() => { // 导入后删除文件
                            //     this.excelFiles.pop() // 如果你不想用下面的刷新页面就用这个pop 把下面的refresh删掉就行
                            //     this.refresh()
                            // })
                            this.refresh()
                        })
                    })
                })
            },
            refresh () { // 刷新页面
                this.$router.go(0)
            },
            getBase64 (file) { // 用FileReader解析文件
                return new Promise(function (resolve, reject) {
                    const reader = new FileReader()
                    let fileResult = ''
                    reader.readAsDataURL(file)
                    // 文件加载成功时触发
                    reader.onload = function () {
                        fileResult = reader.result
                    }
                    // 文件加载失败时触发
                    reader.onerror = function (error) {
                        reject(error)
                    }
                    // 加载成功后使用
                    reader.onloadend = function () {
                        resolve(fileResult)
                    }
                })
            },
            handleError (config, message) { // 页面弹出提示信息
                config.message = message
                config.offsetY = 80
                this.$bkMessage(config)
            }
        }
    }
</script>

<style scoped lang="postcss">
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
            display: flex;
            justify-content: space-between;
            align-items: center;
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
            .import-btn{
                font-size: 24px;
                cursor: pointer;
                /deep/ .file-wrapper{
                    margin: 0;
                    cursor: pointer;
                }
            }
            .import-btn:hover{
                color: #1768EF;
            }
        }
        .goods-type-list{
            width: 100%;
            margin-bottom: 40px;
            .empty-cart{
                width: 400px;
                margin: 140px auto 0;
                display: flex;
                flex-direction: column;
                svg{
                    margin: 0 auto;
                }
                div{
                    text-align: center;
                    font-size: 20px;
                }
            }
            .type-item-wapper{
                width: 100%;
                .type-title{
                    padding-left: 10px;
                    height: 36px;
                    line-height: 34px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    /deep/.bk-tag{
                        font-size: 16px;
                    }
                    .bk-button{
                        height: 26px;
                        line-height: 26px;height: ;
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
            cursor: not-allowed;
            background: #979BA5;
        }
    }
</style>
