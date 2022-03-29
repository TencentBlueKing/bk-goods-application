<template>
    <div class="goods-info-table">
        <bk-table
            v-show="!isGoodsInfoLoad"
            v-if="getGoodsFlag"
            style="margin-top: 20px"
            max-height="400"
            :data="goodsInfo.goodList"
            :pagination="goodsInfo.pagination"
            :is-loading="isGoodsInfoLoad"
            @row-mouse-enter="handleRowMouseEnter"
            @row-mouse-leave="handleRowMouseLeave"
            @page-change="handlePageChange"
            @page-limit-change="handlePageLimitChange"
        >
            <bk-table-column
                type="index"
                label="序列"
                width="60"
            ></bk-table-column>
            <bk-table-column
                label="物品编号"
                prop="good_code"
            ></bk-table-column>
            <bk-table-column
                label="物品名称"
                prop="good_name"
            ></bk-table-column>
            <bk-table-column
                label="物品类型"
                prop="good_tye_name"
            ></bk-table-column>
            <bk-table-column label="参考价" prop="price"></bk-table-column>
            <bk-table-column label="操作" width="150">
                <template slot-scope="props">
                    <bk-button
                        class="mr10"
                        theme="primary"
                        text
                        :disabled="props.row.status === '创建中'"
                        @click="editGood(props.row)"
                    >编辑</bk-button
                    >
                    <bk-button
                        class="mr10"
                        theme="primary"
                        text
                        @click="downGood(props.row)"
                    >下架</bk-button
                    >
                </template>
            </bk-table-column>
        </bk-table>
    </div>
</template>

<script>

    import { GET_GOOD_DETAIL_URL, GET_GOOD_LIST_URL, GET_GOOD_TYPE_LIST_URL, GET_GOOD_CODE_LIST_URL, DOWN_GOOD_URL } from '@/pattern'

    export default {
        data () {
            return {
                unSubmitSearch: {
                    goodCode: '',
                    goodName: '',
                    goodTypeId: 0
                },
                isGoodsInfoLoad: true,
                submitSearchInput: {
                    goodCode: '',
                    goodName: '',
                    goodTypeId: 0
                },
                goodsInfo: {
                    totalNum: 0,
                    goodList: [],
                    pagination: {
                        current: 1,
                        count: 500,
                        limit: 20
                    }
                },
                // 物品类型信息
                getGoodsFlag: true
            }
        },
        created () {
            this.getGoods()
            this.getGoodTypes()
            this.getGoodCodeList()
        },
        methods: {
            editGood () {
                this.$emit('editGood', this.submitSearchInput)
            },
            // 后端请求函数
            getGoods () {
                this.isGoodsInfoLoad = true
                this.$http.get(GET_GOOD_LIST_URL, {
                    params: {
                        good_code: this.submitSearchInput.goodCode,
                        good_name: this.submitSearchInput.goodName,
                        good_type_id: this.submitSearchInput.goodTypeId,
                        page: this.goodsInfo.pagination.current,
                        size: this.goodsInfo.pagination.limit
                    }
                }).then(res => {
                    if (res.result) {
                        this.getGoodsFlag = false
                        this.goodsInfo.totalNum = res.data.total_num
                        this.goodsInfo.goodList = res.data.good_list
                        this.goodsInfo.pagination.count = res.data.total_num
                    } else {
                        this.$bkMessage({
                            'offsetY': 80,
                            'delay': 2000,
                            'theme': 'error',
                            'message': res.message
                        })
                    }
                }).finally(() => {
                    this.getGoodsFlag = true
                    this.isGoodsInfoLoad = false
                })
            },
            getGoodTypes () {
                this.isGoodTypesLoad = true
                this.$http.get(GET_GOOD_TYPE_LIST_URL).then(res => {
                    if (res.result) {
                        this.goodTypeList = res.data
                    }
                }).finally(() => {
                    this.isGoodTypesLoad = false
                })
            },
            getGoodCodeList () {
                this.$http.get(GET_GOOD_CODE_LIST_URL).then(res => {
                    if (res.result) {
                        res.data.forEach((item, index) => {
                            this.goodsCodeList.push({
                                id: index,
                                name: item
                            })
                        })
                    }
                }).catch(() => {
                    this.$bkMessage({
                        message: 'get_good_code_list接口报错',
                        theme: 'error'
                    })
                })
            },
            searchCodeSelect (value, option) {
                this.unSubmitSearch.goodCode = this.goodsCodeList[value].name
                console.log('this.unSubmitSearch.goodCode == ', this.unSubmitSearch.goodCode)
            },
            getGoodInfo (goodId) {
                this.$http.get(GET_GOOD_DETAIL_URL, {
                    params: {
                        good_id: goodId
                    }
                }).then(res => {
                    if (res.result) {
                        this.goodFormData.good_code = res.data.good_code
                        this.goodFormData.good_name = res.data.good_name
                        this.goodFormData.good_type_id = res.data.good_type_id
                        this.goodFormData.price = res.data.price
                        // 处理图片
                        const picfiles = []
                        res.data.pics.forEach(url => {
                            // 避免出现空字符串
                            if (url.length !== 0) {
                                const pic = {
                                    'name': url.split('/')[1],
                                    'url': url
                                }
                                picfiles.push(pic)
                            }
                        })
                        this.goodFormData.pics = picfiles
                        this.goodFormData.remark = res.data.remark
                        this.goodFormData.specifications = res.data.specifications
                        this.goodFormData.introduce = res.data.introduce
                    }
                })
            },
            // 下架物品
            downGood (goodId) {
                this.$http.post(DOWN_GOOD_URL, { id: goodId }).then(res => {
                    const config = {
                        'offsetY': 80,
                        'delay': 2000
                    }
                    if (res.result) {
                        config.theme = 'success'
                        config.message = '下架物品成功'
                        this.$bkMessage(config)
                        // 下架成功，重新初始化页面
                        this.getGoods()
                    } else {
                        // 可以省略，没有错误信息
                        console.log(res.message)
                        // config.theme = 'error'
                        // config.message = res.message
                        // this.$bkMessage(config)
                    }
                })
            },
            // 操作事件
            searchGoodsInfo () {
                this.submitSearchInput.goodCode = this.unSubmitSearch.goodCode
                this.submitSearchInput.goodName = this.unSubmitSearch.goodName
                this.submitSearchInput.goodTypeId = this.unSubmitSearch.goodTypeId
                this.getGoods()
            },
            handlePageLimitChange () {
                // 点击切换选择数据条数
                this.goodsInfo.pagination.limit = arguments[0]
                // console.log('handlePageLimitChange', arguments)
                this.getGoods()
            },
            handlePageChange (page) {
                // 点击切换页数
                this.goodsInfo.pagination.current = page
                this.getGoods()
            }
        }
    }
</script>
<style lang="postcss" scoped>
    .goods-info-table /deep/ .bk-table .bk-table-header-wrapper .bk-table-header {
        width: 100% !important;
    }
    .goods-info-table /deep/ .bk-table .bk-table-body-wrapper .bk-table-body {
        width: 100% !important;
    }
    .goods-info-table
        /deep/
        .bk-table
        .bk-table-body-wrapper
        .bk-table-empty-block {
        width: 100% !important;
    }
</style>
