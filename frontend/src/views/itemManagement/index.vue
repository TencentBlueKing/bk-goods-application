<template>
    <div class="itemManagement-wrapper">
        <div class="header">
            <bk-divider align="left">
                <bk-tag
                    type="filled"
                    style="font-size: 13px"
                ><span>物品管理</span></bk-tag>
            </bk-divider>
        </div>
        <div class="header-wrapper">
            <div class="fun-bar">
                <span>物品编号：</span>
                <bk-input
                    :clearable="true"
                    v-model="unSubmitSearch.goodCode"
                ></bk-input>
            </div>
            <div class="fun-bar">
                <span>物品名称：</span>
                <bk-input
                    :clearable="true"
                    v-model="unSubmitSearch.goodName"
                ></bk-input>
            </div>
            <div class="fun-bar">
                <span style="width: 72px">物品类别：</span>
                <bk-select
                    :disabled="false"
                    v-model="unSubmitSearch.goodTypeId"
                    style="width: 200px"
                    searchable
                >
                    <bk-option
                        :key="0"
                        :id="0"
                        :name="'全部'"
                    > </bk-option>
                    <bk-option
                        v-for="goodType in goodTypeList"
                        :key="goodType.id"
                        :id="goodType.id"
                        :name="goodType.type_name"
                    >
                    </bk-option>
                </bk-select>
            </div>

            <bk-button
                :theme="'primary'"
                :title="'搜索按钮'"
                class="mr10 search-btn"
                @click="searchGoodsInfo"
            >
                搜索
            </bk-button>
            <bk-button
                :theme="'primary'"
                :title="'添加按钮'"
                class="mr10 add-btn"
                @click="$router.push({ name: 'itemCreateUpdate', query: { action: 'create' } })"
            >
                添加
            </bk-button>
        </div>
        <div
            class="goods-info-load"
            v-bkloading="{
                isLoading: isGoodsInfoLoad,
                theme: 'primary',
                zIndex: 10
            }"
        ></div>
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
                :header-cell-style="{ background: '#fff' }"
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
                <bk-table-column label="物品类型">
                    <template slot-scope="props">
                        <bk-tag ext-cls="custom-tag">{{props.row.good_type_name}}</bk-tag>
                    </template>
                </bk-table-column>
                <bk-table-column
                    label="参考价"
                    prop="price"
                ></bk-table-column>
                <bk-table-column
                    label="操作"
                    width="150"
                >
                    <template slot-scope="props">
                        <bk-button
                            class="mr10"
                            theme="primary"
                            text
                            :disabled="props.row.status === '创建中'"
                            @click="$router.push({ name: 'itemCreateUpdate', query: { action: 'update', row_id: props.row.id } })"
                        >编辑</bk-button>
                        <bk-button
                            class="mr10"
                            theme="primary"
                            text
                            @click="clickDownGood(props.row)"
                        >下架</bk-button>
                    </template>
                </bk-table-column>
            </bk-table>
        </div>
    </div>
</template>

<script>
    import {
        GET_GOOD_LIST_URL, GET_GOOD_TYPE_LIST_URL,
        GET_GOOD_CODE_LIST_URL, DOWN_GOOD_URL
    } from '@/pattern'
    export default {
        data () {
            return {
                unSubmitSearch: {
                    goodCode: '',
                    goodName: '',
                    goodTypeId: 0
                },
                submitSearchInput: {
                    goodCode: '',
                    goodName: '',
                    goodTypeId: 0
                },
                isGoodsInfoLoad: true,
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
                getGoodsFlag: true,
                isGoodTypesLoad: true,
                goodsCodeList: []
            }
        },
        created () {
            this.getGoods()
            this.getGoodTypes()
            this.getGoodCodeList()
        },
        methods: {
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
                    this.$$bkMessage({
                        message: 'get_good_code_list接口报错',
                        theme: 'error'
                    })
                })
            },
            searchCodeSelect (value, option) {
                this.unSubmitSearch.goodCode = this.goodsCodeList[value].name
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
                        console.error(res.message)
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
            clickDownGood (row) {
                this.$bkInfo({
                    title: '确认下架物品',
                    subTitle: row.good_code + '（' + row.good_name + '）',
                    showFooter: true,
                    extCls: 'down-good-dialog',
                    confirmFn: () => {
                        this.downGood(row.id)
                    }
                })
            },
            handlePageLimitChange () {
                // 点击切换选择数据条数
                this.goodsInfo.pagination.limit = arguments[0]
                this.getGoods()
            },
            toggleTableSize () {
                const size = ['small', 'medium', 'large']
                const index = (size.indexOf(this.size) + 1) % 3
                this.size = size[index]
            },
            handlePageChange (page) {
                // 点击切换页数
                this.goodsInfo.pagination.current = page
                this.getGoods()
            }
        }
    }
</script>

<style scoped lang="postcss">
    @import "./index.css";
    /* .title-wapper{
                                    margin-top: 10px;
                                } */
    .header-wrapper {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        margin-top: 30px;
        .fun-bar {
            display: flex;
            align-items: center;
            margin-right: 20px;
            span {
                width: 100px;
            }
        }
    }
    .add-type-wrapper {
        display: flex;
        align-items: center;
        span {
            width: 100px;
        }
    }
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

    .good-dialog /deep/ .bk-dialog-wrapper .bk-dialog {
        width: 80% !important;
        top: 100px;
        .bk-dialog-content {
            width: 100% !important;
            left: 0 !important;
        }
    }
    .good-dialog /deep/ .bk-dialog-body {
        height: 600px;
        overflow: auto;
        .form-wrapper {
            display: flex;
            flex-wrap: wrap;
            .good-form {
                flex: 1;
                /* width: 40%; */
                margin-right: 20px;
                .bk-form-item
                    .bk-form-content
                    .bk-form-control
                    /deep/
                    .bk-input-text {
                    width: 100%;
                }
                .bk-form-item .bk-form-content .bk-form-control .group-box {
                    border-right: none;
                    .group-text {
                        padding: 0 4px;
                    }
                }
            }
            .remark-wrapper {
                display: flex;
                flex: 1;
                margin: 20px 0 0 0;
                span {
                    width: 40px;
                }
            }
        }
        .text-wrapper {
            display: flex;
            margin-top: 20px;
            span {
                width: 80px;
            }
        }
    }

    .pic-wrapper {
        display: flex;
        margin-top: 20px;
        span {
            margin-right: 24px;
            width: 56px;
            text-align: right;
        }
    }
    /deep/ .bk-dialog-wrapper .bk-dialog-header .bk-dialog-header-inner,
    .bk-dialog-wrapper .bk-dialog-header p {
        font-size: 20px;
    }
    /deep/.bk-table-enable-row-transition .bk-table-body td {
        border: none !important;
    }
    /deep/.bk-table {
        border: none !important;
        &:before {
            height: 0px !important;
        }
    }
    /deep/.bk-table-outer-border:after {
        width: 0px !important;
    }
    /deep/.bk-table-pagination-wrapper {
        border: none !important;
    }
    .custom-tag {
        color: #409EFF;
    }
</style>
