<template>
    <div class="multi-import">
        <div class="success-apply">
            <bk-table
                :data="successApply"
                :size="medium"
                :pagination="pagination"
                @select="selectRow"
                @select-all="selectAll"
                @page-change="handlePageChange"
                @page-limit-change="handlePageLimitChange"
                @row-click="clickChangeRow"
                class="apply-table"
            >
                <bk-table-column
                    type="selection"
                    width="60"
                ></bk-table-column>
                <bk-table-column
                    label="使用人"
                    width="150"
                >
                    <template slot-scope="props">
                        <bk-input
                            v-model="props.row.applicant"
                            v-if="selectId === props.row.id"
                        ></bk-input>
                        <div v-else>
                            {{props.row.applicant}}
                        </div>
                    </template>
                </bk-table-column>
                <bk-table-column
                    label="物品编码"
                    width="150"
                >
                    <template slot-scope="props">
                        <bk-input
                            v-model="props.row.goodCode"
                            v-if="selectId === props.row.id"
                        ></bk-input>
                        <div v-else>
                            {{props.row.goodCode}}
                        </div>
                    </template>
                </bk-table-column>
                <bk-table-column
                    label="物品名称"
                    width="150"
                >
                    <template slot-scope="props">
                        <bk-input
                            v-model="props.row.goodName"
                            v-if="selectId === props.row.id"
                        ></bk-input>
                        <div v-else>
                            {{props.row.goodName}}
                        </div>
                    </template>
                </bk-table-column>
                <bk-table-column
                    label="数量"
                    width="150"
                >
                    <template slot-scope="props">
                        <bk-input
                            v-model="props.row.num"
                            type="number"
                            :precision="0"
                            :min="1"
                            v-if="selectId === props.row.id"
                        ></bk-input>
                        <div v-else>
                            {{props.row.num}}
                        </div>
                    </template>
                </bk-table-column>
                <bk-table-column
                    label="期望领用日期"
                    width="300"
                >
                    <template slot-scope="props">
                        <bk-date-picker
                            :options="getDateOptions"
                            :timer="false"
                            v-model="props.row.getDate"
                            :disabled="false"
                            v-if="selectId === props.row.id"
                        >
                        </bk-date-picker>
                        <div v-else>
                            {{props.row.getDate ? moment(props.row.getDate).format('YYYY-MM-DD') : ''}}
                        </div>
                    </template>
                </bk-table-column>
                <bk-table-column
                    label="操作"
                    width="150"
                >
                    <template slot-scope="props">
                        <div>
                            <bk-button
                                :text="true"
                                title="primary"
                                @click="clickDeleteRow(props.row)"
                            >删除</bk-button>
                        </div>
                    </template>
                </bk-table-column>
            </bk-table>
        </div>
        <div class="multi-commit">
            <bk-container
                :col="12"
                :gutter="4"
            >
                <bk-row>
                    <bk-col :span="11">
                        <bk-button
                            style="margin: 4px 10% 0 0"
                            size="medium"
                            :outline="true"
                            theme="primary"
                            title="提交申请"
                            @click.stop.prevent="commitMultiApply"
                        >提交申请</bk-button>
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
    </div>
</template>

<script>
    import {
        delFilesUrl, analysisExcelUrl
    } from '@/pattern'
    import { mapState } from 'vuex'
    export default {
        data () {
            return {
                successApply: [], // 页面展示数据
                pagination: { // 分页器数据
                    current: 1,
                    count: 50,
                    limit: 10
                },
                selected: {
                    selectedRows: []
                }, // 存放被选中行数
                excelFiles: [],
                allSuccessApply: [], // 所有数据
                getDateOptions: {
                    disabledDate: function (date) {
                        const myDate = new Date()
                        if (date < myDate.setDate(myDate.getDate() - 1)) {
                            return true
                        }
                        return false
                    }
                },
                selectId: null
            }
        },
        computed: {
            ...mapState({
                userInfo: state => state.user.userInfo
            })
        },
        methods: {
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
            handlePageChange (page) { // 修改当前页触发函数
                this.pagination.current = page
                this.getSuccessApply(this.pagination.current)
            },
            getSuccessApply (page) { // 获取批量导入后校验成功的数据
                this.successApply = []
                for (let i = (page - 1) * this.pagination.limit; this.successApply.length < this.pagination.limit && i < this.allSuccessApply.length; i++) {
                    this.successApply.push(this.allSuccessApply[i])
                }
                this.pagination.count = this.allSuccessApply.length
                this.selected = {
                    selectedRows: []
                }
            },
            handlePageLimitChange () { // 修改每页多少条数据触发函数
                this.pagination.limit = arguments[0]
                this.pagination.current = 1
                this.getSuccessApply(this.pagination.current)
            },
            commitMultiApply () { // 批量申请触发
                if (this.selected.selectedRows.length === 0) {
                    this.handleError({ theme: 'warning' }, '未选择任何数据')
                    return
                }
                this.$emit('showInput', true)
            },
            addDataToTable (res) {
                const data = res.data
                for (let rowIndex = 0; rowIndex < data.success_list.length; rowIndex++) {
                    const oneOfAllObj = {}
                    oneOfAllObj.id = rowIndex + 1
                    oneOfAllObj.applicant = data.success_list[rowIndex][0]
                    oneOfAllObj.goodCode = data.success_list[rowIndex][1]
                    oneOfAllObj.goodName = data.success_list[rowIndex][2]
                    oneOfAllObj.num = data.success_list[rowIndex][3]
                    oneOfAllObj.getDate = data.success_list[rowIndex][6]
                    this.allSuccessApply.push(oneOfAllObj)
                }
            },
            upload (file) { // 上传文件函数
                this.getBase64(file.fileObj.origin).then(res => {
                    const excelFile = res.split(',')[1] // 获取文件信息
                    const fileName = this.userInfo.username + '_' + file.fileObj.name // 获取文件名
                    this.$http.post(analysisExcelUrl, { file: excelFile, fileName: fileName }).then(res => {
                        if (res && res.result === true) {
                            // 全部导入成功
                            this.handleError({ theme: 'success' }, res.message)
                            this.addDataToTable(res)
                        } else if (res && res.result === false) { // 有错误
                            if (res.code === 5003) {
                                // 存在导入失败物品
                                this.handleError({ theme: 'warning' }, '存在申请导入失败')
                                const link = document.createElement('a')
                                link.href = res.data.file_url
                                document.body.appendChild(link)
                                link.click()
                                document.body.removeChild(link)
                                this.addDataToTable(res)
                            } else {
                                this.handleError({ theme: 'error' }, res.message)
                            }
                        }
                        this.excelFiles.push({ // 给上传组件绑定列表添加文件信息
                            name: fileName
                        })
                        this.excelFiles = []
                        this.getSuccessApply(this.pagination.current)
                        this.sleep(2).then(() => {
                            const delDirPath = 'analysis_apply_excel' // 后台存放导入文件路径
                            this.$http.post(delFilesUrl, { dirName: delDirPath, fileName: fileName })
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
            changUploadName () { // 改变上传文件组件显示文本
                const importDom = document.querySelector('.file-wrapper')
                if (importDom !== undefined && importDom !== null) {
                    document.querySelector('.file-wrapper').setAttribute('bk-lablename', '选择文件')
                }
            },
            handleError (config, message) { // 遇到后台报自定义错误时上方弹窗提醒
                config.message = message
                config.offsetY = 80
                this.$bkMessage(config)
            },
            sleep (time) { // 计时器
                return new Promise((resolve, reject) => {
                    setTimeout(resolve, time * 1000)
                })
            },
            clickChangeRow (row) {
                this.selectId = row.id
            },
            clickDeleteRow (row) {
                const index = this.allSuccessApply.indexOf(row)
                if (index !== -1) {
                    this.allSuccessApply.splice(index, 1)
                }
                this.getSuccessApply(this.pagination.current)
            }
        }
    }
</script>

<style lang="postcss" scoped>
    .multi-import {
        .success-apply {
            .apply-table {
            }
        }
        .multi-commit {
            margin: 30px 0;
            text-align: right;
            /deep/ .bk-upload.button .file-wrapper {
                font-size: 14px;
            }
        }
    }
    /deep/ .bk-table-body-wrapper {
        overflow: auto;
    }
</style>
