<template>
    <div class="applyManagement-wrapper">
        <div class="header">
            <bk-divider align="left"><bk-tag type="filled" style="font-size: 13px"><span>申请管理</span></bk-tag></bk-divider>
        </div>
        <div class="condition-form">
            <bk-form :label-width="130" :model="formData" ref="infoForm">
                <bk-container :col="12" :margin="6">
                    <bk-row>
                        <bk-col :span="9">
                            <bk-row class="condition-form-row">
                                <bk-col :span="3">
                                    <div class="applicant">
                                        <bk-form-item
                                            label="申请人"
                                            :property="'applicant'"
                                            class="applicant-item">
                                            <bk-select v-model="formData.applicant">
                                                <bk-option
                                                    key="0"
                                                    id="0"
                                                    name="全部">
                                                </bk-option>
                                                <bk-option v-for="option in applicantList"
                                                    :key="option.id"
                                                    :id="option.username"
                                                    :name="option.username">
                                                </bk-option>
                                            </bk-select>
                                        </bk-form-item>
                                    </div>
                                </bk-col>
                                <bk-col :span="3">
                                    <div class="start-date">
                                        <bk-form-item
                                            label="开始时间"
                                            :property="'startDate'"
                                            :icon-offset="35">
                                            <bk-date-picker :options="startDateOptions" placeholder="请选择" :timer="false" v-model="formData.startDate" :disabled="false" style="width: 100%">
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
                                            <bk-date-picker :options="endDateOptions" placeholder="请选择" :timer="false" v-model="formData.endDate" :disabled="false" style="width: 100%">
                                            </bk-date-picker>
                                        </bk-form-item>
                                    </div>
                                </bk-col>
                            </bk-row>
                            <bk-row class="condition-form-row">
                                <bk-col :span="3" :offset="3">
                                    <div class="campus">
                                        <bk-form-item
                                            label="校区"
                                            :property="'campus'">
                                            <bk-select v-model="formData.campus">
                                                <bk-option
                                                    key="0"
                                                    id="0"
                                                    name="全部">
                                                </bk-option>
                                                <bk-option v-for="option in campusList"
                                                    :key="option.id"
                                                    :id="option.id"
                                                    :name="option.name">
                                                </bk-option>
                                            </bk-select>
                                        </bk-form-item>
                                    </div>
                                </bk-col>
                                <bk-col :span="3">
                                    <div class="college">
                                        <bk-form-item
                                            label="学院"
                                            :property="'college'">
                                            <bk-select v-model="formData.college">
                                                <bk-option
                                                    key="0"
                                                    id="0"
                                                    name="全部">
                                                </bk-option>
                                                <bk-option v-for="option in collegeList"
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
        <div class="applyTable">
            <div class="more-options">
                <bk-dropdown-menu @show="dropdownShow" @hide="dropdownHide" ref="dropdown">
                    <div class="dropdown-trigger-btn" style="padding-left: 19px;" slot="dropdown-trigger">
                        <span>批量操作</span>
                        <i :class="['bk-icon icon-angle-down',{ 'icon-flip': isDropdownShow }]"></i>
                    </div>
                    <ul class="bk-dropdown-list" slot="dropdown-content">
                        <li><a href="javascript:;" @click="agree" class="multi-agree">批量同意</a></li>
                        <li><a href="javascript:;" @click="disagree" class="multi-disagree">批量拒绝</a></li>
                    </ul>
                </bk-dropdown-menu>
            </div>
            <bk-table
                height="430"
                :data="apply"
                :size="medium"
                :pagination="pagination"
                @select="selectRow"
                @select-all="selectAll"
                @row-mouse-enter="handleRowMouseEnter"
                @row-mouse-leave="handleRowMouseLeave"
                @page-change="handlePageChange"
                @page-limit-change="handlePageLimitChange">
                <bk-table-column type="selection" width="60"></bk-table-column>
                <bk-table-column label="使用人" prop="apply_user"></bk-table-column>
                <bk-table-column label="物品编码" prop="good_code"></bk-table-column>
                <bk-table-column label="物品名称" prop="good_name"></bk-table-column>
                <!-- <bk-table-column label="物品类型" prop="goodType"></bk-table-column> -->
                <bk-table-column label="数量" prop="num"></bk-table-column>
                <bk-table-column label="申请时间" prop="apply_time"></bk-table-column>
                <bk-table-column label="地址" prop="position"></bk-table-column>
                <bk-table-column label="申请原因" prop="reason"></bk-table-column>
                <bk-table-column label="操作" width="150">
                    <template slot-scope="props">
                        <bk-button class="mr10" theme="primary" text @click="singleAgree(props.row)">同意</bk-button>
                        <bk-button class="mr10" theme="primary" text @click="singleDisagree(props.row)">拒绝</bk-button>
                    </template>
                </bk-table-column>
            </bk-table>
            <div class="confirm-agree-dialog">
                <bk-dialog v-model="dialogVisible"
                    :render-directive="'show'"
                    theme="primary"
                    :width="700"
                    :mask-close="false"
                    :header-position="'center'"
                    :confirm-fn="confirm()"
                    :ok-text="getOkText()"
                    :title="getDialogTitle()">
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
    const getRootPositionListUrl = 'position/get_root_position_list/' // 获取根地点接口
    const getSubPositionListUrl = 'position/get_sub_position_list/' // 获取子地点接口
    const examineApplyUrl = 'apply/examine_apply/' // 审核申请
    const getApplyUrl = 'apply/' // 获取查询集接口
    const getApplyUserUrl = '/get_apply_users' // 获取组员接口

    export default {
        data () {
            return {
                isDropdownShow: false,
                dialogVisible: false,
                remark: '无', // 审核备注
                formData: { // 查询条件表单数据
                    applicant: 0,
                    startDate: '',
                    endDate: '',
                    campus: 0,
                    college: 0
                },
                get_params: { // 获取申请时提交的参数
                    size: 10,
                    page: 1,
                    start_time: '',
                    end_time: '',
                    apply_user: '',
                    position: ''
                },
                rules: {
                    inputRemark: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ]
                },
                campusList: [], // 校区列表
                collegeList: [], // 学院列表
                apply: [],
                pagination: { // 分页器数据
                    current: 1,
                    count: 10,
                    limit: 10
                },
                selected: {
                    selectedRows: [] // 存放被选中行数
                },
                okText: '',
                dialogTitle: '',
                startDateOptions: {},
                endDateOptions: {}
            }
        },
        watch: {
            'formData.startDate': function (val) {
                this.endDateOptions = {
                    disabledDate: function (date) {
                        if (date < val.setDate(val.getDate())) {
                            return true
                        }
                        return false
                    }
                }
            },
            'formData.endDate': function (val) {
                this.startDateOptions = {
                    disabledDate: function (date) {
                        if (date > val.setDate(val.getDate())) {
                            return true
                        }
                        return false
                    }
                }
            },
            'formData.campus': function (val) { // 监听查询表格的校区变量
                if (val === 0) {
                    return
                }
                this.formData.college = 0
                const parentCode = this.getParentCode(val)
                this.$http.get(getSubPositionListUrl, { params: { parent_code: parentCode } }).then(res => {
                    this.collegeList = res.data
                })
            }
        },
        created () {
            this.username = this.$store.state.user.username
            this.loadData()
        },
        mounted () {},
        methods: {
            loadData () {
                this.getRootPositionList()
                this.getApplyUser()
                this.getApply()
            },
            getApplyUser () { // 获取小组成员
                this.$http.get(getApplyUserUrl).then(res => {
                    if (res) {
                        this.applicantList = res.data
                    }
                })
            },
            getApply () { // 获取申请列表
                this.$http.get(getApplyUrl, { params: {
                    apply_user: this.get_params.apply_user,
                    position: this.get_params.position,
                    start_time: this.get_params.start_time,
                    end_time: this.get_params.end_time,
                    page: this.get_params.page,
                    size: this.get_params.size
                } }).then(res => {
                    if (res) {
                        this.apply = res.data.apply_list
                        this.pagination.count = res.data.total_num
                    }
                })
            },
            getOkText () {
                return this.okText
            },
            getDialogTitle () {
                return this.dialogTitle
            },
            singleAgree (row) { // 单个审核时触发
                if (this.selected.selectedRows.indexOf(row.id) === -1) {
                    this.selected.selectedRows.push(row.id)
                }
                this.agree()
            },
            singleDisagree (row) { // 单个审核时触发
                if (this.selected.selectedRows.indexOf(row.id) === -1) {
                    this.selected.selectedRows.push(row.id)
                }
                this.disagree()
            },
            agree () { // 批量审核时触发
                if (this.selected.selectedRows.length === 0) {
                    this.handleError({ theme: 'warning' }, '未选择任何数据')
                    return
                }
                this.okText = '确定同意'
                this.dialogTitle = '同意申请'
                this.triggerHandler()
                this.dialogVisible = true
            },
            confirmAgree () {
                this.$refs.remark.validate().then(validator => {
                    const examineApplyParamsIdList = this.selected.selectedRows
                    const remark = this.remark
                    this.$http.post(examineApplyUrl, { apply_id_list: examineApplyParamsIdList, model: 'agree', remark: remark }).then(res => {
                        if (res.result === true) {
                            this.handleError({ theme: 'success' }, res.message)
                        } else if (res.result === false) {
                            this.handleError({ theme: 'error' }, res.message)
                        }
                    })
                    this.selected.selectedRows = []
                    this.dialogVisible = false
                    this.getApply()
                }, validator => {
                    // 显示第一个出错位置
                    // alert(`${validator.field}：${validator.content}`)
                })
            },
            disagree () { // 批量审核时触发
                if (this.selected.selectedRows.length === 0) {
                    this.handleError({ theme: 'warning' }, '未选择任何数据')
                    return
                }
                this.okText = '确定拒绝'
                this.dialogTitle = '拒绝申请'
                this.triggerHandler()
                this.dialogVisible = true
            },
            confirmDisagree () {
                this.$refs.remark.validate().then(validator => {
                    const examineApplyParamsIdList = this.selected.selectedRows
                    const remark = this.remark
                    this.$http.post(examineApplyUrl, { apply_id_list: examineApplyParamsIdList, model: 'reject', remark: remark }).then(res => {
                        if (res.result === true) {
                            this.handleError({ theme: 'success' }, res.message)
                        } else if (res.result === false) {
                            this.handleError({ theme: 'error' }, res.message)
                        }
                    })
                    this.selected.selectedRows = []
                    this.dialogVisible = false
                    this.getApply()
                }, validator => {
                    // 显示第一个出错位置
                    // alert(`${validator.field}：${validator.content}`)
                })
            },
            confirm () {
                if (this.okText === '确定同意') {
                    return this.confirmAgree
                } else if (this.okText === '确定拒绝') {
                    return this.confirmDisagree
                }
            },
            search () { // 按下查询按钮时触发
                if (this.formData.startDate) {
                    this.get_params.start_time = this.dateFormat('YYYY-mm-dd', this.formData.startDate)
                } else {
                    this.get_params.start_time = ''
                }
                if (this.formData.endDate) {
                    const tempDate = new Date(Date.parse(this.formData.endDate))
                    tempDate.setDate(tempDate.getDate() + 1)
                    this.get_params.end_time = this.dateFormat('YYYY-mm-dd', tempDate)
                } else {
                    this.get_params.end_time = ''
                }
                if (this.formData.applicant === 0 || this.formData.applicant === '0') {
                    this.get_params.apply_user = ''
                } else {
                    this.get_params.apply_user = this.formData.applicant
                }
                let campus = ''
                let college = ''
                if (this.formData.campus === 0 || this.formData.campus === '0') {
                    campus = ''
                } else {
                    const campusObj = this.campusList.find(this.formDataCampusLocationIdToName)
                    if (campusObj) {
                        campus = campusObj.name
                    } else {
                        campus = ''
                    }
                }
                if (this.formData.college === 0 || this.formData.college === '0') {
                    college = ''
                } else {
                    const collegeObj = this.collegeList.find(this.formDataCollegeLocationIdToName)
                    if (collegeObj) {
                        college = collegeObj.name
                    } else {
                        college = ''
                    }
                }
                this.get_params.position = (!campus && !college) ? '' : campus + ',' + college
                this.pagination.current = 1
                this.get_params.page = this.pagination.current
                this.getApply()
            },
            getParentCode (val) { // 获取校区的编码
                let parentCode = ''
                for (let index = 0; index < this.campusList.length; index++) {
                    if (this.campusList[index].id === val) {
                        parentCode = this.campusList[index].code
                        break
                    }
                }
                return parentCode
            },
            getRootPositionList () { // 获取校区列表
                this.$http.get(getRootPositionListUrl).then(res => {
                    this.campusList = res.data
                })
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
                for (let index = 0; index < this.apply.length; index++) {
                    const ifIdx = this.selected.selectedRows.indexOf(this.apply[index].id)
                    if (ifIdx === -1) {
                        ifFullPage = false
                    }
                    if (!ifFullPage) {
                        break
                    }
                }
                if (this.selected.selectedRows.length !== 0 && !ifFullPage) {
                    for (let index = 0; index < this.apply.length; index++) {
                        if (this.selected.selectedRows.indexOf(this.apply[index].id) === -1) {
                            this.selected.selectedRows.push(this.apply[index].id)
                        }
                    }
                } else if (this.selected.selectedRows.length !== 0 && ifFullPage) {
                    for (let index = 0; index < this.apply.length; index++) {
                        const delIdx = this.selected.selectedRows.indexOf(this.apply[index].id)
                        this.selected.selectedRows.splice(delIdx, 1)
                    }
                } else if (this.selected.selectedRows.length === 0) {
                    for (let index = 0; index < this.apply.length; index++) {
                        this.selected.selectedRows.push(this.apply[index].id)
                    }
                }
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
                this.getApply()
            },
            handlePageChange (page) { // 修改当前页触发函数
                this.pagination.current = page
                this.get_params.page = this.pagination.current
                this.getApply()
            },
            formDataCampusLocationIdToName (obj) {
                return obj.id === this.formData.campus
            },
            formDataCollegeLocationIdToName (obj) {
                return obj.id === this.formData.college
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
            refresh () { // 刷新页面
                this.$router.go(0)
            }
        }
    }
</script>

<style lang="postcss" scoped>
.applyManagement-wrapper {
    width: 95%;
    margin: 0 auto;
    overflow: hidden;
    .condition-form {
        padding: 30px 0 0 0;
        .condition-form-row {
            margin-bottom: 30px;
            .applicant {
            }
            .commit {
                text-align: center;
                line-height: 110px;
            }
        }
    }
    .applyTable {
        text-align: right;
        .more-options {
            margin: 0 20px 10px 0;
        }
        .multi-agree:hover {
            color: rgb(29, 206, 29);
        }
        .multi-disagree:hover {
            color: red;
        }
        .confirm-agree-dialog {
            .input-remark {
            }
        }
    }
}
</style>
