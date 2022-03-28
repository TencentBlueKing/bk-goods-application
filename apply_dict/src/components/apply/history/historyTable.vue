<template>
    <div class="table-content">
        <div class="more-options">
            <bk-dropdown-menu
                @show="isDropdownShow = true"
                @hide="isDropdownShow = false"
                ref="dropdown"
            >
                <div
                    class="dropdown-trigger-btn"
                    style="padding-left: 19px;"
                    slot="dropdown-trigger"
                >
                    <span>批量操作</span>
                    <i :class="['bk-icon icon-angle-down',{ 'icon-flip': isDropdownShow }]"></i>
                </div>
                <ul
                    class="bk-dropdown-list"
                    slot="dropdown-content"
                >
                    <li>
                        <a
                            href="javascript:;"
                            @click="exportData"
                            class="multi-export"
                        >导出数据</a>
                    </li>
                </ul>
            </bk-dropdown-menu>
        </div>
        <bk-table
            height="430"
            :data="history"
            :size="medium"
            :pagination="pagination"
            @select="selectRow"
            @select-all="selectAll"
            @row-mouse-enter="handleRowMouseEnter"
            @row-mouse-leave="handleRowMouseLeave"
            @page-change="handlePageChange"
            @page-limit-change="handlePageLimitChange"
        >
            <bk-table-column
                type="selection"
                width="60"
            ></bk-table-column>
            <bk-table-column
                label="物品名称"
                prop="good_name"
                width="150"
            ></bk-table-column>
            <bk-table-column
                label="物品编码"
                prop="good_code"
            ></bk-table-column>
            <bk-table-column
                label="申请时间"
                prop="create_time"
                width="160"
            ></bk-table-column>
            <bk-table-column
                label="数量"
                prop="num"
                width="55"
            ></bk-table-column>
            <bk-table-column
                label="申请原因"
                prop="reason"
            ></bk-table-column>
            <bk-table-column
                label="状态"
                prop="status"
                width="110"
            ></bk-table-column>
            <bk-table-column
                label="审核人"
                prop="reviewer"
                width="120"
            ></bk-table-column>
            <bk-table-column
                label="审核日期"
                prop="review_time"
                width="180"
            >
            </bk-table-column>
            <bk-table-column
                label="备注"
                prop="reason"
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
                        @click="edit(props.row)"
                        :disabled="props.row.status !== '导员审核中'"
                    >编辑</bk-button>
                    <bk-button
                        class="mr10"
                        theme="primary"
                        text
                        @click="destroy(props.row)"
                        :disabled="props.row.status === '管理员审核中'"
                    >删除</bk-button>
                </template>
            </bk-table-column>
        </bk-table>
    </div>
</template>

<script>
    import {
        deriveExcelUrl, getGoodApplyListUrl
    } from '@/pattern'
    export default {
        data () {
            return {
                selected: {
                    selectedRows: [] // 存放被选中行数
                },
                getParams: {
                    good_name: '',
                    good_code: '',
                    reason: '',
                    start_time: '',
                    end_time: '',
                    status: '',
                    size: 10,
                    page: 1
                },
                history: [],
                pagination: { // 分页器数据
                    current: 1,
                    count: 10,
                    limit: 10
                },
                isDropdownShow: false
            }
        },
        created () {
            this.getGoodApplyList()
        },
        methods: {
            getGoodApplyList () {
                this.$http.post(getGoodApplyListUrl, {
                    start_time: this.getParams.start_time,
                    end_time: this.getParams.end_time,
                    good_code: this.getParams.good_code,
                    good_name: this.getParams.good_name,
                    reason: this.getParams.reason,
                    status: this.getParams.status,
                    page: this.getParams.page,
                    size: this.getParams.size
                }).then(res => {
                    this.history = res.data.apply_list
                    this.pagination.count = res.data.total_num
                })
            },
            exportData () {
                if (this.selected.selectedRows.length === 0) {
                    this.handleError({ theme: 'warning' }, '未选择任何数据')
                    return
                }
                this.$http.post(deriveExcelUrl, { model: 3, dataList: this.selected }).then(res => {
                    if (res && res.result === true) {
                        const link = document.createElement('a') // 生成a元素，用以实现下载功能
                        link.href = res.data.file_url
                        document.body.appendChild(link)
                        link.click()
                        document.body.removeChild(link)
                        this.getGoodApplyList()
                        this.selected.selectedRows = []
                    } else if (res && res.result === false) {
                        this.handleError({ theme: 'error' }, res.message)
                    }
                })
            },
            search (formData) {
                this.getParams.start_time = formData.startDate ? this.moment(formData.startDate).format('YYYY-MM-DD') : ''
                this.getParams.end_time = formData.endDate ? this.moment(formData.endDate).format('YYYY-MM-DD') : ''
                this.getParams.status = formData.status
                if (formData.status === 999 || formData.status === '999') {
                    this.getParams.status = ''
                }
                this.getParams.good_name = formData.good_name
                this.getParams.good_code = formData.good_code
                this.getParams.reason = formData.apply_reason

                this.pagination.current = 1
                this.getParams.page = this.pagination.current
                this.getGoodApplyList()
            },
            selectRow (selection, row) { // 选择单行时触发函数
                const idx = this.selected.selectedRows.indexOf(row.id)
                if (idx !== -1) {
                    this.selected.selectedRows.splice(idx, 1)
                } else {
                    this.selected.selectedRows.push(row.id)
                }
            },
            selectAll () { // 全选时触发函数
                let ifFullPage = true
                for (let index = 0; index < this.history.length; index++) {
                    const ifIdx = this.selected.selectedRows.indexOf(this.history[index].id)
                    if (ifIdx === -1) {
                        ifFullPage = false
                    }
                    if (!ifFullPage) {
                        break
                    }
                }
                if (this.selected.selectedRows.length !== 0 && !ifFullPage) {
                    for (let index = 0; index < this.history.length; index++) {
                        if (this.selected.selectedRows.indexOf(this.history[index].id) === -1) {
                            this.selected.selectedRows.push(this.history[index].id)
                        }
                    }
                } else if (this.selected.selectedRows.length !== 0 && ifFullPage) {
                    for (let index = 0; index < this.history.length; index++) {
                        const delIdx = this.selected.selectedRows.indexOf(this.history[index].id)
                        this.selected.selectedRows.splice(delIdx, 1)
                    }
                } else if (this.selected.selectedRows.length === 0) {
                    for (let index = 0; index < this.history.length; index++) {
                        this.selected.selectedRows.push(this.history[index].id)
                    }
                }
            },
            edit (row) {
                this.$emit('edit', row)
            },
            destroy (row) {
                this.$emit('destroy', row)
            },
            handlePageLimitChange () { // 修改每页多少条数据触发函数
                this.pagination.limit = arguments[0]
                this.getParams.size = this.pagination.limit
                this.pagination.current = 1
                this.getParams.page = this.pagination.current
                this.selected.selectedRows = []
                this.getGoodApplyList()
            },
            handlePageChange (page) { // 修改当前页触发函数
                this.pagination.current = page
                this.getParams.page = this.pagination.current
                this.getGoodApplyList()
            },
            handleError (config, message) { // 遇到后台报自定义错误时上方弹窗提醒
                config.message = message
                config.offsetY = 80
                this.$bkMessage(config)
            }
        }
    }
</script>

<style lang="postcss" scoped>
</style>
