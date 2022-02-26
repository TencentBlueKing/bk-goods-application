<template>
    <div class="applyHome-wrapper">
        <div class="header">
            <bk-divider align="left"><bk-tag type="filled" style="font-size: 13px"><span @click="refresh" style="cursor: pointer">首页</span></bk-tag></bk-divider>
        </div>
        <div class="switcher">
            <bk-tag style="margin-right: 10px">批量申请</bk-tag>
            <bk-switcher v-model="showMultiImport" theme="primary"></bk-switcher>
        </div>
        <div class="info-table" v-if="showInfoForm">
            <bk-form :label-width="130" :model="formData" :rules="rules" ref="infoForm">
                <bk-container :col="12" :margin="6">
                    <bk-row class="info-table-row">
                        <bk-col :span="3">
                            <div class="applicant">
                                <bk-form-item
                                    label="申请人"
                                    :property="'applicant'">
                                    <bk-tag>{{ formData.applicant }}</bk-tag>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="3">
                            <div class="group-leaders">
                                <bk-form-item
                                    :label="getInfoTableLabel()"
                                    :property="'leaders'">
                                    <bk-tag>{{ formData.leaders }}</bk-tag>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="3">
                            <div class="apply-good-name">
                                <bk-form-item
                                    label="申请物品名"
                                    :required="true"
                                    :property="'goodName'">
                                    <bk-input v-model="formData.goodName" placeholder=""></bk-input>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="3">
                            <div class="apply-good-code">
                                <bk-form-item
                                    label="申请物品编号"
                                    :required="true"
                                    :property="'goodCode'">
                                    <bk-input v-model="formData.goodCode" placeholder=""></bk-input>
                                </bk-form-item>
                            </div>
                        </bk-col>
                    </bk-row>
                    <bk-row class="info-table-row">
                        <bk-col :span="3">
                            <div class="campus">
                                <bk-form-item
                                    label="校区"
                                    :required="true"
                                    :property="'campus'">
                                    <bk-select v-model="formData.campus">
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
                                    :required="true"
                                    :property="'college'">
                                    <bk-select v-model="formData.college">
                                        <bk-option v-for="option in collegeList"
                                            :key="option.id"
                                            :id="option.id"
                                            :name="option.name">
                                        </bk-option>
                                    </bk-select>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="3">
                            <div class="specificLocation">
                                <bk-form-item
                                    label="具体地点"
                                    :required="true"
                                    :property="'specificLocation'">
                                    <bk-input v-model="formData.specificLocation" placeholder=""></bk-input>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="3">
                            <div class="apply-num">
                                <bk-form-item
                                    label="申请数量"
                                    :property="'applyNum'">
                                    <bk-input type="number" :min="1" :precision="precision" v-model="formData.num"></bk-input>
                                </bk-form-item>
                            </div>
                        </bk-col>
                    </bk-row>
                    <bk-row class="info-table-row">
                        <bk-col :span="3">
                            <div class="get-date">
                                <bk-form-item
                                    label="期望领用日期"
                                    :property="'getDate'"
                                    :required="true">
                                    <bk-date-picker placeholder="请选择" :timer="false" v-model="formData.getDate" :disabled="false" style="width: 100%">
                                    </bk-date-picker>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="9">
                            <div class="apply-reason">
                                <bk-form-item
                                    :required="true"
                                    label="申请原因"
                                    :property="'applyReason'">
                                    <bk-input type="textarea" v-model="formData.applyReason"></bk-input>
                                </bk-form-item>
                            </div>
                        </bk-col>
                    </bk-row>
                    <bk-row class="info-table-row">
                        <bk-col :span="12">
                            <div class="commit">
                                <bk-button size="medium" :outline="true" theme="primary" title="提交申请" @click.stop.prevent="commitApply">提交申请</bk-button>
                            </div>
                        </bk-col>
                    </bk-row>
                </bk-container>
            </bk-form>
        </div>
        <div class="multi-import-page" v-show="showMultiImport">
            <div class="success-apply">
                <bk-table
                    :data="successApply"
                    :size="medium"
                    :pagination="pagination"
                    @select="selectRow"
                    @select-all="selectAll"
                    @row-mouse-enter="handleRowMouseEnter"
                    @row-mouse-leave="handleRowMouseLeave"
                    @page-change="handlePageChange"
                    @page-limit-change="handlePageLimitChange">
                    <bk-table-column type="selection" width="60"></bk-table-column>
                    <bk-table-column label="使用人" prop="applicant"></bk-table-column>
                    <!-- <bk-table-column label="导员" prop="leaders"></bk-table-column> -->
                    <bk-table-column label="物品编码" prop="goodCode"></bk-table-column>
                    <bk-table-column label="物品名称" prop="goodName"></bk-table-column>
                    <bk-table-column label="数量" prop="num"></bk-table-column>
                    <bk-table-column label="期望领用日期" prop="getDate"></bk-table-column>
                    <!-- <bk-table-column label="校区" prop="campus"></bk-table-column>
                    <bk-table-column label="学院" prop="college"></bk-table-column>
                    <bk-table-column label="具体地点" prop="specificLocation"></bk-table-column>
                    <bk-table-column label="申请原因" prop="applyReason"></bk-table-column> -->
                </bk-table>
            </div>
            <div class="multi-commit">
                <bk-container :col="12" :gutter="4">
                    <bk-row>
                        <bk-col :span="11">
                            <bk-button style="margin: 4px 10% 0 0" size="medium" :outline="true" theme="primary" title="提交申请" @click.stop.prevent="commitMultiApply">提交申请</bk-button>
                        </bk-col>
                        <bk-col :span="1">
                            <div class="select-file">
                                <bk-upload
                                    class="upload-button"
                                    :theme="'button'"
                                    :with-credentials="true"
                                    :custom-request="upload"
                                    :size="50"
                                    :files="excelFiles"
                                    :accept="'.xls, .xlsx'"
                                    :limit="1"
                                ></bk-upload>
                            </div>
                        </bk-col>
                    </bk-row>
                </bk-container>
            </div>
            <div class="input-more">
                <bk-dialog v-model="inputVisible"
                    theme="primary"
                    :width="700"
                    :mask-close="false"
                    :header-position="'center'"
                    :confirm-fn="confirmMultiCommit"
                    ok-text="确定提交"
                    title="请完善信息">
                    <bk-form :label-width="130" ref="inputForm">
                        <bk-container :col="12" :margin="6">
                            <bk-row style="margin: 25px;">
                                <bk-col :span="12">
                                    <div class="leaders">
                                        <bk-form-item
                                            label="导员">
                                            <bk-tag>{{ multiInput.leaders }}</bk-tag>
                                        </bk-form-item>
                                    </div>
                                </bk-col>
                            </bk-row>
                            <bk-row style="margin: 25px;">
                                <bk-col :span="12">
                                    <div class="campus">
                                        <bk-form-item
                                            label="校区"
                                            :required="true"
                                            :property="'multiCampus'">
                                            <bk-select v-model="multiInput.campus">
                                                <bk-option v-for="option in campusList"
                                                    :key="option.id"
                                                    :id="option.id"
                                                    :name="option.name">
                                                </bk-option>
                                            </bk-select>
                                        </bk-form-item>
                                    </div>
                                </bk-col>
                            </bk-row>
                            <bk-row style="margin: 25px;">
                                <bk-col :span="12">
                                    <div class="college">
                                        <bk-form-item
                                            label="学院"
                                            :required="true"
                                            :property="'multiCollege'">
                                            <bk-select v-model="multiInput.college">
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
                            <bk-row style="margin: 25px;">
                                <bk-col :span="12">
                                    <div class="specificLocation">
                                        <bk-form-item
                                            label="具体地点"
                                            :required="true"
                                            :property="'multiSpecificLocation'">
                                            <bk-input v-model="multiInput.specificLocation" placeholder=""></bk-input>
                                        </bk-form-item>
                                    </div>
                                </bk-col>
                            </bk-row>
                            <bk-row style="margin: 25px;">
                                <bk-col :span="12">
                                    <div class="apply-reason">
                                        <bk-form-item
                                            :required="true"
                                            label="申请原因"
                                            :property="'multiApplyReason'">
                                            <bk-input type="textarea" v-model="multiInput.applyReason"></bk-input>
                                        </bk-form-item>
                                    </div>
                                </bk-col>
                            </bk-row>
                        </bk-container>
                    </bk-form>
                </bk-dialog>
            </div>
        </div>
    </div>
</template>

<script>
    const delFilesUrl = '/purchase/del_excel' // 删除已生成的excel文件接口
    const analysisExcelUrl = '/analysis_apply_excel' // 解析excel文件数据接口
    const getRootPositionListUrl = '/get_root_position_list' // 获取根地点接口
    const getSubPositionListUrl = '/get_sub_position_list' // 获取子地点接口
    const getLeadersUrl = '/get_leader' // 获取导员接口
    const commitApplyUrl = '/submit_apply_list' // 提交申请接口

    export default {
        data () {
            return {
                isDropdownShow: false,
                isLeader: false,
                isAdmin: false,
                username: '',
                showInfoForm: true,
                showMultiImport: false,
                excelFiles: [],
                inputVisible: false,
                multiInput: { // 批量导入时所需填写的表格数据
                    leaders: '无',
                    campus: '',
                    college: '',
                    specificLocation: '',
                    applyReason: ''
                },
                formData: { // 单个导入时所需填写的表格数据
                    applicant: '',
                    leaders: '无',
                    goodName: '',
                    goodCode: '',
                    campus: '',
                    college: '',
                    specificLocation: '',
                    num: 1,
                    getDate: '',
                    applyReason: ''
                },
                precision: 0,
                successApply: [], // 页面展示数据
                allSuccessApply: [], // 所有数据
                selected: {
                    selectedRows: []
                }, // 存放被选中行数
                pagination: { // 分页器数据
                    current: 1,
                    count: 50,
                    limit: 10
                },
                campusList: [], // 校区列表
                collegeList: [], // 学院列表
                rules: {
                    goodName: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    getDate: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    goodCode: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    campus: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    college: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    applyReason: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ],
                    specificLocation: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }
                    ]
                }
            }
        },
        watch: {
            showMultiImport: function (val) { // 监听批量导入页面是否展示
                this.changUploadName()
                this.showInfoForm = !val
            },
            'formData.campus': function (val) { // 监听单个导入时的页面表格的校区变量
                const parentCode = this.getParentCode(val)
                this.$http.get(getSubPositionListUrl, { params: { parent_code: parentCode } }).then(res => {
                    this.collegeList = res.data
                })
            },
            'multiInput.campus': function (val) { // 监听批量导入时的页面表格的校区变量
                const parentCode = this.getParentCode(val)
                this.$http.get(getSubPositionListUrl, { params: { parent_code: parentCode } }).then(res => {
                    this.collegeList = res.data
                })
            }
        },
        created () {
            this.username = this.$store.state.user.username
            this.isLeader = this.$store.state.isLeader
            this.isAdmin = this.$store.state.isAdmin
            this.formData.applicant = this.username
            this.loadData() // 创建实例时加载数据
        },
        mounted () {
            
        },
        methods: {
            loadData () {
                this.getRootPositionList()
                this.getLeaders()
            },
            getInfoTableLabel () {
                return '导员'
            },
            getLeaders () {
                this.$http.get(getLeadersUrl).then(res => {
                    if (res) {
                        if (res.result === true && res.code !== '220') {
                            this.formData.leaders = res.data
                            this.multiInput.leaders = res.data
                        }
                    }
                })
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
            changUploadName () { // 改变上传文件组件显示文本
                const importDom = document.querySelector('.file-wrapper')
                if (importDom !== undefined && importDom !== null) {
                    document.querySelector('.file-wrapper').setAttribute('bk-lablename', '选择文件')
                }
            },
            commitMultiApply () { // 批量申请触发
                if (this.selected.selectedRows.length === 0) {
                    this.handleError({ theme: 'warning' }, '未选择任何数据')
                    return
                }
                this.inputVisible = true
            },
            confirmMultiCommit () {
                if (!this.multiInput.campus || !this.multiInput.specificLocation || !this.multiInput.applyReason || !this.multiInput.college) {
                    this.handleError({ theme: 'warning' }, '任何数据不能为空')
                    return
                }
                const applyForm = []
                for (let index = 0; index < this.allSuccessApply.length; index++) {
                    const selectedIdx = this.selected.selectedRows.indexOf(this.allSuccessApply[index].id)
                    if (selectedIdx !== -1) {
                        this.allSuccessApply[index]['good_code'] = this.allSuccessApply[index]['goodCode']
                        delete this.allSuccessApply[index].goodCode
                        this.allSuccessApply[index]['good_name'] = this.allSuccessApply[index]['goodName']
                        delete this.allSuccessApply[index].goodName
                        this.allSuccessApply[index]['require_date'] = this.allSuccessApply[index]['getDate']
                        delete this.allSuccessApply[index].getDate
                        this.allSuccessApply[index]['apply_user'] = this.allSuccessApply[index]['applicant']
                        delete this.allSuccessApply[index].applicant
                        this.allSuccessApply[index]['leaders'] = this.multiInput.leaders
                        this.allSuccessApply[index]['school'] = this.campusList.find(this.multiInputCampusLocationIdToName).name
                        this.allSuccessApply[index]['academy'] = this.collegeList.find(this.multiInputCollegeLocationIdToName).name
                        this.allSuccessApply[index]['detail_position'] = this.multiInput.specificLocation
                        this.allSuccessApply[index]['reason'] = this.multiInput.applyReason
                        applyForm.push(this.allSuccessApply[index])
                    }
                }
                for (let index = 0; index < applyForm.length; index++) {
                    const allApplyIdx = this.allSuccessApply.indexOf(applyForm[index])
                    this.allSuccessApply.splice(allApplyIdx, 1)
                }
                this.$http.post(commitApplyUrl, { apply_list: applyForm }).then(res => {
                    if (res.result === true) {
                        this.handleError({ theme: 'success' }, res.message)
                    } else if (res.result === false) {
                        this.handleError({ theme: 'error' }, res.message)
                    }
                })
                this.selected.selectedRows = []
                this.getSuccessApply(this.pagination.current)
                this.inputVisible = false
            },
            formDataCampusLocationIdToName (obj) {
                return obj.id === this.formData.campus
            },
            formDataCollegeLocationIdToName (obj) {
                return obj.id === this.formData.college
            },
            multiInputCampusLocationIdToName (obj) {
                return obj.id === this.multiInput.campus
            },
            multiInputCollegeLocationIdToName (obj) {
                return obj.id === this.multiInput.college
            },
            commitApply () { // 单个申请触发
                this.$refs.infoForm.validate().then(validator => {
                    const applyList = []
                    // eslint-disable-next-line no-new-object
                    const applyObj = new Object()
                    applyObj['good_code'] = this.formData.goodCode
                    applyObj['good_name'] = this.formData.goodName
                    if (this.formData.getDate) {
                        applyObj['require_date'] = this.dateFormat('YYYY-mm-dd', this.formData.getDate)
                    } else {
                        applyObj['require_date'] = ''
                    }
                    applyObj['apply_user'] = this.formData.applicant
                    applyObj['leaders'] = this.formData.leaders
                    applyObj['school'] = this.campusList.find(this.formDataCampusLocationIdToName).name
                    applyObj['academy'] = this.collegeList.find(this.formDataCollegeLocationIdToName).name
                    applyObj['detail_position'] = this.formData.specificLocation
                    applyObj['reason'] = this.formData.applyReason
                    applyObj['num'] = this.formData.num
                    applyList.push(applyObj)
                    this.$http.post(commitApplyUrl, { apply_list: applyList }).then(res => {
                        if (res.result === true) {
                            this.handleError({ theme: 'success' }, res.message)
                            this.sleep(2).then(res => {
                                this.refresh()
                            })
                        } else if (res.result === false) {
                            this.handleError({ theme: 'error' }, res.message)
                        }
                    })
                }, validator => {
                    // 显示第一个出错位置
                    // alert(`${validator.field}：${validator.content}`)
                })
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
            multiImport () { // 批量导入触发
                this.showInfoForm = false
                this.showMultiImport = true
                this.getSuccessApply(this.pagination.current)
            },
            getSuccessApply (page) { // 获取批量导入后校验成功的数据
                this.successApply = []
                for (let i = (page - 1) * this.pagination.limit; this.successApply.length < this.pagination.limit && i < this.allSuccessApply.length; i++) {
                    this.successApply.push(this.allSuccessApply[i])
                }
                this.pagination.count = this.allSuccessApply.length
            },
            dropdownShow () {
                this.isDropdownShow = true
            },
            dropdownHide () {
                this.isDropdownShow = false
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
                for (let index = 0; index < this.successApply.length; index++) {
                    const ifIdx = this.selected.selectedRows.indexOf(this.successApply[index].id)
                    if (ifIdx === -1) {
                        ifFullPage = false
                    }
                    if (!ifFullPage) {
                        break
                    }
                }
                if (this.selected.selectedRows.length !== 0 && !ifFullPage) {
                    for (let index = 0; index < this.successApply.length; index++) {
                        if (this.selected.selectedRows.indexOf(this.successApply[index].id) === -1) {
                            this.selected.selectedRows.push(this.successApply[index].id)
                        }
                    }
                } else if (this.selected.selectedRows.length !== 0 && ifFullPage) {
                    for (let index = 0; index < this.successApply.length; index++) {
                        const delIdx = this.selected.selectedRows.indexOf(this.successApply[index].id)
                        this.selected.selectedRows.splice(delIdx, 1)
                    }
                } else if (this.selected.selectedRows.length === 0) {
                    for (let index = 0; index < this.successApply.length; index++) {
                        this.selected.selectedRows.push(this.successApply[index].id)
                    }
                }
            },
            upload (file) { // 上传文件函数
                this.getBase64(file.fileObj.origin).then(res => {
                    const excelFile = res.split(',')[1] // 获取文件信息
                    const fileName = this.username + '_' + file.fileObj.name // 获取文件名
                    this.$http.post(analysisExcelUrl, { file: excelFile, fileName: fileName }).then(res => {
                        if (res && res.result === true) { // 全部导入成功
                            this.handleError({ theme: 'success' }, res.message)
                            const data = res.data
                            console.log(res.data)
                            for (let rowIndex = 0; rowIndex < data.success_list.length; rowIndex++) {
                                // eslint-disable-next-line no-new-object
                                const oneOfAllObj = new Object()
                                oneOfAllObj.id = rowIndex + 1
                                oneOfAllObj.applicant = data.success_list[rowIndex][0]
                                oneOfAllObj.goodCode = data.success_list[rowIndex][1]
                                oneOfAllObj.goodName = data.success_list[rowIndex][2]
                                oneOfAllObj.num = data.success_list[rowIndex][3]
                                oneOfAllObj.getDate = data.success_list[rowIndex][6]
                                // oneOfAllObj.leaders = ''
                                // oneOfAllObj.campus = ''
                                // oneOfAllObj.college = ''
                                // oneOfAllObj.specificLocation = ''
                                // oneOfAllObj.applyReason = ''
                                this.allSuccessApply.push(oneOfAllObj)
                            }
                        } else if (res && res.result === false) { // 有错误
                            this.handleError({ theme: 'error' }, res.message)
                        }
                        if (res && res.result === true && res.code === 5003) { // 存在导入失败物品
                            this.handleError({ theme: 'warning' }, '存在申请导入失败')
                            const link = document.createElement('a') // 生成a元素，用以实现下载功能
                            link.href = res.data.file_url
                            document.body.appendChild(link)
                            link.click()
                            document.body.removeChild(link)
                        }
                        this.excelFiles.push({ // 给上传组件绑定列表添加文件信息
                            name: fileName
                        })
                        this.excelFiles = []
                        this.getSuccessApply(this.pagination.current)
                        this.sleep(2).then(() => {
                            const delDirPath = 'analysis_apply_excel' // 后台存放导入文件路径
                            this.$http.post(delFilesUrl, { dirName: delDirPath, fileName: fileName }).then(() => { // 导入后删除文件
                            })
                        })
                    })
                })
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
            handleError (config, message) { // 遇到后台报自定义错误时上方弹窗提醒
                config.message = message
                config.offsetY = 80
                this.$bkMessage(config)
            },
            handlePageLimitChange () { // 修改每页多少条数据触发函数
                this.pagination.limit = arguments[0]
                this.pagination.current = 1
                this.getSuccessApply(this.pagination.current)
            },
            handlePageChange (page) { // 修改当前页触发函数
                this.pagination.current = page
                this.getSuccessApply(this.pagination.current)
            },
            sleep (time) { // 计时器
                return new Promise((resolve, reject) => {
                    setTimeout(resolve, time * 1000)
                })
            },
            refresh () { // 刷新页面
                this.$router.go(0)
            }
        }
    }
</script>

<style lang="postcss" scoped>
.applyHome-wrapper {
    width: 95%;
    margin: 0 auto;
    overflow: hidden;
    .switcher {
        padding: 15px 0 0 0;
    }
    .info-table {
        width: 100%;
        padding: 30px 0;
        overflow: hidden;
        height:calc(100vh - 280px);
        .info-table-row {
            margin-bottom: 50px;
            .commit {
                text-align: right;
            }
            .more-options {
                text-align: right;
                padding: 10px 0 0 0;
                /deep/ .bk-dropdown-content {
                    padding: 0;
                }
                /deep/ .bk-dropdown-menu .bk-dropdown-list>li>a {
                    padding: 0;
                }
            }
        }
    }
    .multi-import-page {
        padding: 15px 0 0 0;
        width: 100%;
        .multi-commit {
            margin: 30px 0;
            text-align: right;
            /deep/ .bk-upload.button .file-wrapper {
                    font-size: 14px;
                }
        }
    }
}
</style>
