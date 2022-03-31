<template>
    <div class="applyManagement-wrapper">
        <div class="condition-form">
            <manage-form @search="handleSearch"></manage-form>
        </div>
        <div class="applyTable">
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
                                @click="agree"
                                class="multi-agree"
                            >批量同意</a>
                        </li>
                        <li>
                            <a
                                href="javascript:;"
                                @click="disagree"
                                class="multi-disagree"
                            >批量拒绝</a>
                        </li>
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
                @page-limit-change="handlePageLimitChange"
            >
                <bk-table-column
                    type="selection"
                    width="60"
                ></bk-table-column>
                <bk-table-column
                    label="使用人"
                    prop="apply_user"
                ></bk-table-column>
                <bk-table-column
                    label="物品编码"
                    prop="good_code"
                ></bk-table-column>
                <bk-table-column
                    label="物品名称"
                    prop="good_name"
                ></bk-table-column>
                <!-- <bk-table-column label="物品类型" prop="goodType"></bk-table-column> -->
                <bk-table-column
                    label="数量"
                    prop="num"
                ></bk-table-column>
                <bk-table-column
                    label="申请时间"
                    prop="apply_time"
                ></bk-table-column>
                <bk-table-column
                    label="地址"
                    prop="position"
                ></bk-table-column>
                <bk-table-column
                    label="申请原因"
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
                            @click="singleAgree(props.row)"
                        >同意</bk-button>
                        <bk-button
                            class="mr10"
                            theme="primary"
                            text
                            @click="singleDisagree(props.row)"
                        >拒绝</bk-button>
                    </template>
                </bk-table-column>
            </bk-table>
            <div class="confirm-agree-dialog">
                <bk-dialog
                    v-model="dialogVisible"
                    :render-directive="'show'"
                    theme="primary"
                    :width="700"
                    :mask-close="false"
                    :header-position="'center'"
                    :confirm-fn="confirm()"
                    :ok-text="getOkText()"
                    :title="getDialogTitle()"
                >
                    <div class="input-remark">
                        <bk-form
                            :label-width="100"
                            :model="remark"
                            :rules="rules"
                            ref="remark"
                        >
                            <bk-form-item
                                label="备注"
                                :required="true"
                                :property="'inputRemark'"
                            >
                                <bk-input
                                    type="textarea"
                                    v-model="remark"
                                    placeholder="请输入"
                                ></bk-input>
                            </bk-form-item>
                        </bk-form>
                    </div>
                </bk-dialog>
            </div>
        </div>
    </div>
</template>

<script>
    import { mapState } from 'vuex'
    import {
        examineApplyUrl, getApplyUrl
    } from '@/pattern'
    import ManageForm from '@/components/apply/manage/manageForm.vue'

    export default {
        components: {
            ManageForm
        },
        data () {
            return {
                isDropdownShow: false,
                dialogVisible: false,
                remark: '无', // 审核备注
                getParams: { // 获取申请时提交的参数
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
                dialogTitle: ''
            }
        },
        computed: {
            ...mapState({
                userInfo: state => state.user.userInfo
            })
        },
        created () {
            this.getApply()
        },
        methods: {
            getApply () { // 获取申请列表
                this.$http.get(getApplyUrl, {
                    params: this.getParams
                }).then(res => {
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
            handleSearch (formData) { // 按下查询按钮时触发
                this.getParams.start_time = formData.startDate ? this.moment(formData.startDate).format('YYYY-MM-DD') : ''
                this.getParams.end_time = formData.endDate ? this.moment(formData.endDate).format('YYYY-MM-DD') : ''
                this.getParams.apply_user = formData.applicant || ''
                let campus = ''
                let college = ''
                if (formData.campus === 0 || formData.campus === '0') {
                    campus = ''
                } else {
                    campus = this.campusList.find(obj => obj.id === formData.campus).name || ''
                }
                if (formData.college === 0 || formData.college === '0') {
                    college = ''
                } else {
                    college = this.collegeList.find(obj => obj.id === formData.college).name || ''
                }
                this.getParams.position = (!campus && !college) ? '' : campus + ',' + college
                this.pagination.current = 1
                this.getParams.page = this.pagination.current
                this.getApply()
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
                this.getParams.size = this.pagination.limit
                this.pagination.current = 1
                this.getParams.page = this.pagination.current
                this.selected.selectedRows = []
                this.getApply()
            },
            handlePageChange (page) { // 修改当前页触发函数
                this.pagination.current = page
                this.getParams.page = this.pagination.current
                this.getApply()
            },
            triggerHandler () {
                this.$refs.dropdown.hide()
            }
        }
    }
</script>

<style lang="postcss" scoped>
    .applyManagement-wrapper {
        margin-top: 10px;
        padding-bottom: 20px;
        overflow-x: hidden;
        .condition-form {
            padding: 30px 0 0 0;
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
