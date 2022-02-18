<template>
    <div class="applyHistory-wrapper">
        <div class="header">
            <bk-divider align="left"><bk-tag type="filled" style="font-size: 13px"><span @click="refresh" style="cursor: pointer">历史记录</span></bk-tag></bk-divider>
        </div>
        <div class="condition-form">
            <bk-form :label-width="130" :model="formData" ref="infoForm">
                <bk-container :col="12" :margin="6">
                    <bk-row>
                        <bk-col :span="9">
                            <bk-row class="condition-form-row">
                                <bk-col :span="3">
                                    <div class="goodName">
                                        <bk-form-item label="物品名" :property="'goodName'">
                                            <bk-input v-model="formData.good_name" placeholder="请输入"></bk-input>
                                        </bk-form-item>
                                    </div>
                                </bk-col>
                                <bk-col :span="3">
                                    <div class="goodCode">
                                        <bk-form-item label="物品编号" :property="'goodCode'">
                                            <bk-input v-model="formData.good_code" placeholder="请输入"></bk-input>
                                        </bk-form-item>
                                    </div>
                                </bk-col>
                                <bk-col :span="3">
                                    <div class="applyReason">
                                        <bk-form-item label="申请原因" :property="'applyReason'">
                                            <bk-input v-model="formData.reason" placeholder="请输入"></bk-input>
                                        </bk-form-item>
                                    </div>
                                </bk-col>
                            </bk-row>
                            <bk-row class="condition-form-row">
                                <bk-col :span="3">
                                    <div class="start-date">
                                        <bk-form-item
                                            label="开始时间"
                                            :property="'startDate'"
                                            :icon-offset="35">
                                            <bk-date-picker placeholder="请选择" :timer="false" v-model="formData.start_date" :disabled="false" style="width: 100%">
                                            </bk-date-picker>
                                        </bk-form-item>
                                    </div>
                                </bk-col>
                                <bk-col :span="3">
                                    <div class="end-date">
                                        <bk-form-item
                                            label="结束时间"
                                            :property="'endDate'"
                                            :icon-offset="0">
                                            <bk-date-picker placeholder="请选择" :timer="false" v-model="formData.end_date" :disabled="false" style="width: 100%">
                                            </bk-date-picker>
                                        </bk-form-item>
                                    </div>
                                </bk-col>
                                <bk-col :span="3">
                                    <div class="status">
                                        <bk-form-item
                                            label="状态"
                                            :property="'status'">
                                            <bk-select v-model="formData.status">
                                                <bk-option
                                                    key="999"
                                                    id="999"
                                                    name="全部">
                                                </bk-option>
                                                <bk-option v-for="option in statusList"
                                                    :key="option.id"
                                                    :id="option.id"
                                                    :name="option.name">
                                                </bk-option>
                                            </bk-select>
                                        </bk-form-item>
                                    </div>
                                </bk-col>
                            </bk-row>
                        </bk-col>
                        <bk-col :span="3">
                            <div style="text-align: center;line-height: 90px;">
                                <bk-button size="large" :outline="true" theme="primary" title="查询" @click.stop.prevent="search">查询</bk-button>
                            </div>
                        </bk-col>
                    </bk-row>
                </bk-container>
            </bk-form>
        </div>
        <div class="historyTable">
            <div class="more-options">
                <bk-dropdown-menu @show="dropdownShow" @hide="dropdownHide" ref="dropdown">
                    <div class="dropdown-trigger-btn" style="padding-left: 19px;" slot="dropdown-trigger">
                        <span>批量操作</span>
                        <i :class="['bk-icon icon-angle-down',{ 'icon-flip': isDropdownShow }]"></i>
                    </div>
                    <ul class="bk-dropdown-list" slot="dropdown-content">
                        <li><a href="javascript:;" @click="exportData" class="multi-export">导出数据</a></li>
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
                @page-limit-change="handlePageLimitChange">
                <bk-table-column type="selection" width="60"></bk-table-column>
                <bk-table-column label="物品名称" prop="good_name"></bk-table-column>
                <bk-table-column label="物品编码" prop="good_code"></bk-table-column>
                <bk-table-column label="申请时间" prop="apply_time"></bk-table-column>
                <bk-table-column label="数量" prop="num"></bk-table-column>
                <bk-table-column label="申请原因" prop="reason"></bk-table-column>
                <bk-table-column label="状态" prop="status"></bk-table-column>
                <bk-table-column label="审核人" prop="apply_time"></bk-table-column>
                <bk-table-column label="审核日期" prop="apply_time"></bk-table-column>
                <bk-table-column label="备注" prop="apply_time"></bk-table-column>
                <bk-table-column label="操作" width="150">
                    <template slot-scope="props">
                        <bk-button class="mr10" theme="primary" text @click="editHistory(props.row)" v-if="props.row.status === '管理员审核中' || props.row.status === '组长审核中'">编辑</bk-button>
                        <bk-button class="mr10" theme="primary" text @click="deleteHistory(props.row)" v-if="props.row.status !== '审核完成'">删除</bk-button>
                    </template>
                </bk-table-column>
            </bk-table>
            <div class="edit-history-dialog">
                <bk-dialog v-model="editDialogVisible"
                    :render-directive="'show'"
                    theme="primary"
                    :width="700"
                    :mask-close="false"
                    :header-position="'center'"
                    :confirm-fn="confirmEdit"
                    ok-text="确定修改"
                    title="编辑申请记录">
                    <div class="input-remark">
                        <bk-form :label-width="100" :model="remark" :rules="rules" ref="remark">
                            <bk-form-item label="备注" :required="true" :property="'inputRemark'">
                                <bk-input type="textarea" v-model="remark" placeholder="请输入"></bk-input>
                            </bk-form-item>
                        </bk-form>
                    </div>
                </bk-dialog>
            </div>
            <div class="delete-confirm-dialog">
                <bk-dialog v-model="deleteDialogVisible"
                    :render-directive="'show'"
                    theme="primary"
                    :width="700"
                    :mask-close="false"
                    :header-position="'center'"
                    :confirm-fn="confirmDelete"
                    ok-text="确定删除"
                    title="删除申请记录">
                    <div class="input-remark">
                        <bk-form :label-width="100" :model="remark" :rules="rules" ref="remark">
                            <bk-form-item label="备注" :required="true" :property="'inputRemark'">
                                <bk-input type="textarea" v-model="remark" placeholder="请输入"></bk-input>
                            </bk-form-item>
                        </bk-form>
                    </div>
                </bk-dialog>
            </div>
        </div>
    </div>
</template>

<script>
    const deriveExcelUrl = '/purchase/derive_excel'

    export default {
        data () {
            return {
                formData: { // 查询条件表单数据
                    good_name: '',
                    good_code: '',
                    apply_reason: '',
                    start_date: '',
                    end_date: '',
                    status: 999
                },
                get_params: {
                    good_name: '',
                    good_code: '',
                    reason: '',
                    start_time: '',
                    end_time: '',
                    status: '',
                    size: 10,
                    page: 1
                },
                editDialogVisible: false,
                deleteDialogVisible: false,
                isDropdownShow: false,
                statusList: [],
                history: [
                    {
                        id: 1,
                        good_name: 1,
                        status: '组长审核中'
                    },
                    {
                        id: 2,
                        good_name: 2,
                        status: '管理员审核中'
                    },
                    {
                        id: 3,
                        good_name: 3,
                        status: '组长审核中'
                    },
                    {
                        id: 4,
                        good_name: 4,
                        status: '审核完成'
                    },
                    {
                        id: 5,
                        good_name: 5,
                        status: '组长审核中'
                    },
                    {
                        id: 6,
                        good_name: 6,
                        status: '管理员审核中'
                    }
                    
                ],
                pagination: { // 分页器数据
                    current: 1,
                    count: 10,
                    limit: 10
                },
                selected: {
                    selectedRows: [] // 存放被选中行数
                }
            }
        },
        methods: {
            search () {
                if (this.formData.start_date) {
                    this.get_params.start_time = this.dateFormat('YYYY-mm-dd', this.formData.start_date)
                } else {
                    this.get_params.start_time = ''
                }
                if (this.formData.end_date) {
                    this.get_params.end_time = this.dateFormat('YYYY-mm-dd', this.formData.end_date)
                } else {
                    this.get_params.end_time = ''
                }
                if (this.formData.status === 999 || this.formData.status === '999') {
                    this.get_params.status = ''
                }
                this.get_params.good_name = this.formData.good_name
                this.get_params.good_code = this.formData.good_code
                this.get_params.reason = this.formData.apply_reason

                this.pagination.current = 1
                this.get_params.page = this.pagination.current
                console.log('this.get_params', this.get_params)
            },
            editHistory () {
                this.editDialogVisible = true
            },
            deleteHistory () {
                this.deleteDialogVisible = true
            },
            confirmEdit () {
                console.log('confirmEdit')
                this.editDialogVisible = false
            },
            confirmDelete () {
                console.log('confirmDelete')
                this.deleteDialogVisible = false
            },
            exportData () {
                this.$http.post(deriveExcelUrl, { model: 3, dataList: this.selected }).then(res => {
                    if (res && res.result === true) {
                        const link = document.createElement('a') // 生成a元素，用以实现下载功能
                        link.href = res.data.file_url
                        document.body.appendChild(link)
                        link.click()
                        document.body.removeChild(link)
                        const fileName = res.data.file_url.split('/').slice(-1)[0] // 获取文件名
                        const dirName = res.data.file_url.split('/').slice(-2, -1)[0] // 获取文件夹名
                        this.fileCache.push([fileName, dirName])
                    } else if (res && res.result === false) {
                        this.handleError({ theme: 'error' }, res.message)
                    }
                })
            },
            selectRow (selection, row) { // 选择单行时触发函数
                const idx = this.selected.selectedRows.indexOf(row.id)
                if (idx !== -1) {
                    this.selected.selectedRows.splice(idx, 1)
                } else {
                    this.selected.selectedRows.push(row.id)
                }
                console.log('this.selected.selectedRows', this.selected.selectedRows)
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
                console.log('this.selected.selectedRows', this.selected.selectedRows)
            },
            handleError (config, message) { // 遇到后台报自定义错误时上方弹窗提醒
                config.message = message
                config.offsetY = 80
                this.$bkMessage(config)
            },
            handlePageLimitChange () { // 修改每页多少条数据触发函数
                this.pagination.limit = arguments[0]
                this.get_params.size = this.pagination.limit
                this.pagination.current = 1
                this.get_params.page = this.pagination.current
                this.selected.selectedRows = []
                // this.getApply()
            },
            handlePageChange (page) { // 修改当前页触发函数
                this.pagination.current = page
                this.get_params.page = this.pagination.current
                // this.getApply()
            },
            dateFormat (fmt, date) {
                let ret
                const opt = {
                    'Y+': date.getFullYear().toString(), // 年
                    'm+': (date.getMonth() + 1).toString(), // 月
                    'd+': date.getDate().toString(), // 日
                    'H+': date.getHours().toString(), // 时
                    'M+': date.getMinutes().toString(), // 分
                    'S+': date.getSeconds().toString() // 秒.
                    // 有其他格式化字符需求可以继续添加，必须转化成字符串
                }
                for (const k in opt) {
                    ret = new RegExp('(' + k + ')').exec(fmt)
                    if (ret) {
                        fmt = fmt.replace(ret[1], (ret[1].length === 1) ? (opt[k]) : (opt[k].padStart(ret[1].length, '0')))
                    }
                }
                return fmt
            },
            dropdownShow () {
                this.isDropdownShow = true
            },
            dropdownHide () {
                this.isDropdownShow = false
            },
            triggerHandler () {
                this.$refs.dropdown.hide()
            },
            refresh () { // 刷新页面
                this.$router.go(0)
            }
        }
    }
</script>

<style lang="postcss" scoped>
.applyHistory-wrapper {
    width: 95%;
    margin: 0 auto;
    overflow: hidden;
    .condition-form {
        padding: 30px 0 0 0;
        .condition-form-row {
            margin-bottom: 30px;
        }
    }
    .historyTable {
        text-align: right;
        .more-options {
            margin: 0 20px 10px 0;
            .multi-export:hover {

            }
        }
    }
}
</style>
