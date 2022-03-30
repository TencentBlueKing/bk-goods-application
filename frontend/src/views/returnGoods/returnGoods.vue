<template>
    <div class="returnGoods-wrapper">
        <div class="breadCrumb">
            <bk-breadcrumb>
                <bk-breadcrumb-item v-for="(item,index) in navList" :key="index" :to="item.link">{{item.title}}</bk-breadcrumb-item>
            </bk-breadcrumb>
        </div>
        <div class="message-table">
            <bk-form :label-width="200" form-type="vertical">
                <bk-container :col="12" :gutter="8">
                    <bk-row style="width: 90%">
                        <bk-col :span="8">
                            <div class="applicant">
                                <bk-form-item label="申请人">
                                    <bk-tag style="font-size: 15px">{{ username }}</bk-tag>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="4" style="line-height: 90px">
                            <div class="return">
                                <bk-button theme="danger" title="提交" :outline="true" size="large" @click="dialogVisible">
                                    提交
                                </bk-button>
                                <bk-dialog v-model="returnDialogVisible"
                                    theme="primary"
                                    width="600"
                                    :render-directive="'if'"
                                    :mask-close="false"
                                    :header-position="left"
                                    @confirm="returnGoods"
                                    :esc-close="false"
                                    title="">
                                    确认提交?
                                </bk-dialog>
                            </div>
                        </bk-col>
                    </bk-row>
                    <bk-row style="margin-bottom: 30px;">
                        <bk-col :span="3">
                            <div class="returnLocation">
                                <bk-form-item label="退库省份">
                                    <bk-select :disabled="false" v-model="formData.province" style="width: 80%"
                                        ext-cls="select-custom"
                                        ext-popover-cls="select-popover-custom"
                                        searchable>
                                        <bk-option
                                            key="0"
                                            id="0"
                                            name="所有地区">
                                        </bk-option>
                                        <bk-option v-for="option in provinceList"
                                            :key="option.id"
                                            :id="option.name"
                                            :name="option.name">
                                        </bk-option>
                                    </bk-select>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="3">
                            <div class="returnLocation">
                                <bk-form-item label="退库城市">
                                    <bk-select :disabled="false" v-model="formData.city" style="width: 80%"
                                        ext-cls="select-custom"
                                        ext-popover-cls="select-popover-custom"
                                        searchable>
                                        <bk-option
                                            key="0"
                                            id="0"
                                            name="所有地区">
                                        </bk-option>
                                        <bk-option v-for="option in cityList"
                                            :key="option.id"
                                            :id="option.name"
                                            :name="option.name">
                                        </bk-option>
                                    </bk-select>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="3">
                            <div class="returnReason">
                                <bk-form-item label="退库原因">
                                    <bk-select :disabled="false" v-model="formData.reason" style="width: 80%"
                                        ext-cls="select-custom"
                                        ext-popover-cls="select-popover-custom"
                                        searchable>
                                        <bk-option v-for="option in reasonList"
                                            :key="option.id"
                                            :id="option.id"
                                            :name="option.reason_name">
                                        </bk-option>
                                    </bk-select>
                                </bk-form-item>
                            </div>
                        </bk-col>
                    </bk-row>
                    <bk-row style="margin-bottom: 20px;">
                        <div class="remark">
                            <bk-form-item label="备注">
                                <bk-input type="textarea" v-model="formData.remark" placeholder="请输入备注" style="width:90%"></bk-input>
                            </bk-form-item>
                        </div>
                    </bk-row>
                </bk-container>
            </bk-form>
        </div>
        <div class="returnData">
            <bk-table style="margin-top: 15px;"
                :data="data"
                :size="medium"
                :pagination="pagination"
                @select="selectRow"
                @select-all="selectAll"
                @row-mouse-enter="handleRowMouseEnter"
                @row-mouse-leave="handleRowMouseLeave"
                @page-change="handlePageChange"
                @page-limit-change="handlePageLimitChange">
                <bk-table-column type="selection" width="60"></bk-table-column>
                <bk-table-column label="物资编码" prop="good_code"></bk-table-column>
                <bk-table-column label="物品名称" prop="good_name"></bk-table-column>
                <bk-table-column label="所在地区" prop="position"></bk-table-column>
                <bk-table-column label="使用人" prop="username"></bk-table-column>
                <bk-table-column label="状态" prop="status"></bk-table-column>
            </bk-table>
        </div>
    </div>
</template>

<script>
    import {
        GET_ROOT_POSITION_LIST_URL, GET_SUB_POSITION_LIST_URL, GET_PERSONAL_GOODS_URL, WITHDRAW_REASON_URL, ADD_WITHDRAW_APPLY_URL
    } from '@/pattern'
    import { mapState } from 'vuex'
    export default {
        data () {
            return {
                navList: [ // 面包屑列表
                    {
                        title: '个人物资查询', link: { name: 'personalGoods' }
                    },
                    {
                        title: '物资退库', link: { name: 'returnGoods' }
                    }
                ],
                formData: {
                    province: 0,
                    city: 0,
                    remark: '',
                    reason: ''
                },
                provinceList: [],
                cityList: [],
                reasonList: [],
                idList: [],
                username: '',
                get_params: { // 用于提交请求的数据
                    form: {
                        name: '',
                        code: '',
                        province: '',
                        city: '',
                        status: 2,
                        type: ''
                    },
                    page: 1,
                    pageLimit: 10
                },
                pagination: { // 分页器数据
                    current: 1,
                    count: 50,
                    limit: 10
                },
                selected: {
                    selectedRows: [] // 存放被选中行数
                },
                data: '',
                returnDialogVisible: false,
                FIRST: true
            }
        },
        computed: {
            ...mapState({
                userInfo: state => state.user.userInfo
            })
        },
        watch: {
            'formData.province': function (val) { // 监听单个导入时的页面表格的校区变量
                this.cityList = []
                this.formData.city = 0
                if (val === 0 || val === '0') {
                    return
                }
                const parentCode = this.getParentCode(val)
                this.$http.get(GET_SUB_POSITION_LIST_URL, { params: { parent_code: parentCode } }).then(res => {
                    console.log(res)
                    this.cityList = res.data
                })
            }
        },
        created () {
            if (!this.$route.params.isFromPersonalGoods) { // 如果不是从个人物资查询页面的跳转则直接返回个人物资查询页面
                this.$router.replace({ name: 'personalGoods' })
            }
            this.loadData()
        },
        methods: {
            loadData () {
                this.username = this.$store.state.user.userInfo.username // 从state中获取用户名
                this.idList = JSON.stringify(this.$route.params.idList.selectedRows)
                this.getPersonalGoods()
                this.getPosition()
                this.getWithdrawReasons()
            },
            getParentCode (val) { // 获取父级地区的编码
                let parentCode = ''
                for (let index = 0; index < this.provinceList.length; index++) {
                    if (this.provinceList[index].name === val) {
                        parentCode = this.provinceList[index].code
                        break
                    }
                }
                return parentCode
            },
            checkIdList () {
                if (this.data.length !== JSON.parse(this.idList).length && this.FIRST === true) { // 传进来的id存在状态为非使用的情况
                    this.handleError({ theme: 'warning' }, '状态非在使用的物资不可退库')
                    this.FIRST = false
                }
            },
            getPosition () { // 获得一级地点
                this.$http.get(GET_ROOT_POSITION_LIST_URL).then(res => {
                    if (res) {
                        if (res && res.result === true) {
                            this.provinceList = res.data
                        } else if (res && res.result === false) {
                            this.handleError({ theme: 'error' }, res.message)
                        }
                    }
                })
            },
            getWithdrawReasons () { // 获得所有退库原因
                this.$http.get(WITHDRAW_REASON_URL).then(res => {
                    if (res) {
                        if (res && res.result === true) {
                            this.reasonList = res.data
                        } else if (res && res.result === false) {
                            this.handleError({ theme: 'error' }, res.message)
                        }
                    }
                })
            },
            getPersonalGoods () { // 获得个人物资
                this.$http.get(GET_PERSONAL_GOODS_URL, {
                    params: {
                        username: this.username,
                        form: this.get_params.form,
                        page: this.get_params.page,
                        pageLimit: this.get_params.pageLimit,
                        idList: this.idList
                    }
                }).then(res => {
                    if (res && res.result === true) {
                        this.pagination.count = res.data[res.data.length - 1].total // 获取数据总量
                        res.data.pop()
                        this.data = res.data
                        this.checkIdList()
                        if (this.data.length === 0) {
                            this.$router.replace({ name: 'personalGoods', params: { isFromReturnGoods: true } })
                        }
                    } else if (res && res.result === false) {
                        this.handleError({ theme: 'error' }, res.message)
                    }
                }).catch(err => {
                    console.log('错误为：', err)
                })
            },
            dialogVisible () { // 提交确认对话框
                if (this.selected.selectedRows.length === 0) {
                    this.handleError({ theme: 'warning' }, '未选择任何数据')
                    return
                }
                this.returnDialogVisible = true
            },
            returnGoods () { // 退库函数
                this.$http.post(ADD_WITHDRAW_APPLY_URL, { good_ids: this.selected.selectedRows, reason_id: this.formData.reason, province: this.formData.province, city: this.formData.city, remark: this.formData.remark }).then(res => {
                    if (res && res.result === true) {
                        this.handleError({ theme: 'success' }, '退库成功')
                        this.idList = JSON.parse(this.idList) // 转为列表类型
                        for (let index = 0; index < this.selected.selectedRows.length; index++) {
                            const idx = this.idList.indexOf(this.selected.selectedRows[index])
                            if (idx !== -1) {
                                this.idList.splice(idx, 1)
                            }
                        }
                        this.idList = JSON.stringify(this.idList) // 转回字符串
                        this.selected.selectedRows = []
                        this.pagination.current = 1
                        this.get_params.page = this.pagination.current
                        this.getPersonalGoods()
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
            },
            selectAll () { // 全选时触发函数
                if (this.selected.selectedRows.length !== 0 && this.selected.selectedRows.length !== this.pagination.limit) {
                    this.selected.selectedRows = []
                    for (let index = 0; index < this.data.length; index++) {
                        this.selected.selectedRows.push(this.data[index].id)
                    }
                } else if (this.selected.selectedRows.length !== 0 && this.selected.selectedRows.length === this.pagination.limit) {
                    this.selected.selectedRows = []
                } else if (this.selected.selectedRows.length === 0) {
                    for (let index = 0; index < this.data.length; index++) {
                        this.selected.selectedRows.push(this.data[index].id)
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
                this.get_params.pageLimit = this.pagination.limit
                this.pagination.current = 1
                this.get_params.page = this.pagination.current
                this.selectedRows = []
                this.getPersonalGoods()
            },
            handlePageChange (page) { // 修改当前页触发函数
                this.pagination.current = page
                this.get_params.page = this.pagination.current
                this.getPersonalGoods()
            }
        }
    }
</script>

<style lang="postcss" scoped>
.returnGoods-wrapper{
    .breadCrumb{
        margin: 15px 20px;
    }
    .message-table{
        .return{
            text-align: right;
        }
    }
    .returnData{
        margin: 20px 10px;
    }
}
</style>
