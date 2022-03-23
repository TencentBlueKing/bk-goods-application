<template>
    <div class="applyHistory-wrapper">
        <div class="header">
            <bk-divider align="left"><bk-tag type="filled" style="font-size: 13px"><span>历史记录</span></bk-tag></bk-divider>
        </div>
        <div class="condition-form">
            <bk-form :label-width="130" :model="formData" ref="infoForm">
                <bk-container :col="12" :margin="6">
                    <bk-row>
                        <bk-col :span="9">
                            <bk-row class="condition-form-row">
                                <bk-col :span="3">
                                    <div class="goodName">
                                        <bk-form-item label="物品名称" :property="'goodName'">
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
                                            <bk-input v-model="formData.apply_reason" placeholder="请输入"></bk-input>
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
                                            <bk-date-picker :options="startDateOptions" placeholder="请选择" :timer="false" v-model="formData.start_date" :disabled="false" style="width: 100%">
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
                                            <bk-date-picker :options="endDateOptions" placeholder="请选择" :timer="false" v-model="formData.end_date" :disabled="false" style="width: 100%">
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
                <bk-table-column label="物品名称" prop="good_name" width="150"></bk-table-column>
                <bk-table-column label="物品编码" prop="good_code"></bk-table-column>
                <bk-table-column label="申请时间" prop="create_time" width="160"></bk-table-column>
                <bk-table-column label="数量" prop="num" width="55"></bk-table-column>
                <bk-table-column label="申请原因" prop="reason"></bk-table-column>
                <bk-table-column label="状态" prop="status" width="110"></bk-table-column>
                <bk-table-column label="审核人" prop="reviewer" width="120"></bk-table-column>
                <bk-table-column label="审核日期" prop="review_time" width="180"></bk-table-column>
                <bk-table-column label="备注" prop="reason"></bk-table-column>
                <bk-table-column label="操作" width="150">
                    <template slot-scope="props">
                        <bk-button class="mr10" theme="primary" text @click="editHistory(props.row)" :disabled="props.row.status !== '导员审核中'">编辑</bk-button>
                        <bk-button class="mr10" theme="primary" text @click="deleteHistory(props.row)" :disabled="props.row.status === '管理员审核中'">删除</bk-button>
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
                    <div>
                        <bk-form :label-width="100" :model="remark" :rules="rules" ref="remark">
                            <bk-container :col="12" :margin="6">
                                <bk-row style="margin: 0 0 30px 0;">
                                    <bk-col :span="6">
                                        <div>
                                            <bk-form-item label="物品名称" :property="'goodName'">
                                                <bk-input v-model="editFormData.good_name" placeholder="请输入"></bk-input>
                                            </bk-form-item>
                                        </div>
                                    </bk-col>
                                    <bk-col :span="6">
                                        <div>
                                            <bk-form-item label="物品编号" :property="'goodCode'">
                                                <bk-input v-model="editFormData.good_code" placeholder="请输入"></bk-input>
                                            </bk-form-item>
                                        </div>
                                    </bk-col>
                                </bk-row>
                                <bk-row style="margin: 0 0 30px 0;">
                                    <bk-col :span="6">
                                        <div>
                                            <bk-form-item label="申请原因" :property="'applyReason'">
                                                <bk-input v-model="editFormData.reason" placeholder="请输入"></bk-input>
                                            </bk-form-item>
                                        </div>
                                    </bk-col>
                                    <bk-col :span="6">
                                        <div class="apply-num">
                                            <bk-form-item
                                                label="申请数量">
                                                <bk-input type="number" :min="1" :precision="precision" v-model="editFormData.num"></bk-input>
                                            </bk-form-item>
                                        </div>
                                    </bk-col>
                                </bk-row>
                            </bk-container>
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
                    title="确定删除记录？">
                </bk-dialog>
            </div>
        </div>
    </div>
</template>

<script>
    const deriveExcelUrl = '/derive_excel' // 导出数据接口
    const getGoodApplyListUrl = '/get_self_good_apply_list' // 获取申请列表接口
    const getGoodApplyByIdUrl = '/get_good_apply' // 根据id查找单个apply
    const editApplyUrl = '/update_good_apply' // 更新apply信息
    const deleteApplyUrl = '/delete_good_apply' // 删除apply
    const getApplyStatusUrl = '/get_apply_status' // 获取所有申请状态

    export default {
        data () {
            return {
                endDateOptions: {}, // 禁用日期
                startDateOptions: {}, // 禁用日期
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
                editFormData: {
                    good_name: '',
                    good_code: '',
                    reason: '',
                    num: 1
                },
                deleteApplyId: 0,
                precision: 0,
                editDialogVisible: false,
                deleteDialogVisible: false,
                isDropdownShow: false,
                statusList: [],
                history: [],
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
        watch: {
            'formData.start_date': function (val) {
                this.endDateOptions = {
                    disabledDate: function (date) {
                        if (date < val.setDate(val.getDate())) {
                            return true
                        }
                        return false
                    }
                }
            },
            'formData.end_date': function (val) {
                this.startDateOptions = {
                    disabledDate: function (date) {
                        if (date > val.setDate(val.getDate())) {
                            return true
                        }
                        return false
                    }
                }
            }
        },
        created () {
            this.loadData()
        },
        methods: {
            loadData () {
                this.getGoodApplyList()
                this.getApplyStatus()
            },
            getApplyStatus () {
                this.$http.get(getApplyStatusUrl).then(res => {
                    if (res) {
                        this.statusList = res.data
                    }
                })
            },
            getGoodApplyList () {
                this.$http.get(getGoodApplyListUrl, { params: {
                    start_time: this.get_params.start_time,
                    end_time: this.get_params.end_time,
                    good_code: this.get_params.good_code,
                    good_name: this.get_params.good_name,
                    reason: this.get_params.reason,
                    status: this.get_params.status,
                    page: this.get_params.page,
                    size: this.get_params.size
                } }).then(res => {
                    this.history = res.data.apply_list
                    this.pagination.count = res.data.total_num
                })
            },
            search () {
                if (this.formData.start_date) {
                    this.get_params.start_time = this.dateFormat('YYYY-mm-dd', this.formData.start_date)
                } else {
                    this.get_params.start_time = ''
                }
                if (this.formData.end_date) {
                    this.formData.end_date.setDate(this.formData.end_date.getDate() + 1)
                    this.get_params.end_time = this.dateFormat('YYYY-mm-dd', this.formData.end_date)
                } else {
                    this.get_params.end_time = ''
                }
                this.get_params.status = this.formData.status
                if (this.formData.status === 999 || this.formData.status === '999') {
                    this.get_params.status = ''
                }
                this.get_params.good_name = this.formData.good_name
                this.get_params.good_code = this.formData.good_code
                this.get_params.reason = this.formData.apply_reason

                this.pagination.current = 1
                this.get_params.page = this.pagination.current
                console.log('this.get_params', this.get_params)
                this.getGoodApplyList()
            },
            editHistory (row) {
                this.editDialogVisible = true
                this.$http.get(getGoodApplyByIdUrl, { params: {
                    id: row.id
                } }).then(res => {
                    if (res) {
                        console.log('id_apply', res)
                        // this.editFormData.good_name = res.data.good_name
                        // this.editFormData.good_code = res.data.good_code
                        // this.editFormData.reason = res.data.reason
                        // this.editFormData.num = res.data.num
                        this.editFormData = res.data
                    }
                })
            },
            deleteHistory (row) {
                this.deleteDialogVisible = true
                this.deleteApplyId = row.id
            },
            confirmEdit () {
                this.editDialogVisible = false
                let school = ''
                let academy = ''
                let detailPosition = ''
                if (this.editFormData.position) {
                    const positionList = this.editFormData.position.split(',')
                    console.log('positionList', positionList)
                    school = positionList[0]
                    academy = positionList[1]
                    if (positionList.length > 2) {
                        detailPosition = positionList[2]
                    }
                    console.log('school', school)
                    console.log('academy', academy)
                    console.log('detail_position', detailPosition)
                }
                this.$http.post(editApplyUrl, {
                    apply_time: this.editFormData.apply_time,
                    apply_user: this.editFormData.apply_user,
                    good_code: this.editFormData.good_code,
                    good_name: this.editFormData.good_name,
                    id: this.editFormData.id,
                    num: this.editFormData.num,
                    school: school,
                    academy: academy,
                    detail_position: detailPosition,
                    reason: this.editFormData.reason,
                    require_date: this.editFormData.require_date,
                    status: this.editFormData.status
                }).then(res => {
                    if (res.result === true) {
                        this.handleError({ theme: 'success' }, res.message)
                        this.getGoodApplyList()
                    }
                })
            },
            confirmDelete () {
                this.deleteDialogVisible = false
                this.$http.get(deleteApplyUrl, { params: {
                    id: this.deleteApplyId
                } }).then(res => {
                    if (res.result === true) {
                        this.handleError({ theme: 'success' }, res.message)
                        this.getGoodApplyList()
                    }
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
                        // const fileName = res.data.file_url.split('/').slice(-1)[0] // 获取文件名
                        // const dirName = res.data.file_url.split('/').slice(-2, -1)[0] // 获取文件夹名
                        // this.fileCache.push([fileName, dirName])
                        this.getGoodApplyList()
                        this.selected.selectedRows = []
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
                this.getGoodApplyList()
            },
            handlePageChange (page) { // 修改当前页触发函数
                this.pagination.current = page
                this.get_params.page = this.pagination.current
                this.getGoodApplyList()
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
    height:calc(100vh - 200px);
    /* height: 1000px; */
    .condition-form {
        padding: 30px 0 0 0;
        .condition-form-row {
            margin-bottom: 15px;
        }
    }
    .historyTable {
        text-align: right;
        .more-options {
            margin: 0 10px 10px 0;
            .multi-export:hover {

            }
        }
        .edit-history-dialog {
            .edit-table-row {
                
            }
        }
    }
}
</style>
