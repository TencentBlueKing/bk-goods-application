<template>
    <div class="applyHome-wrapper">
        <div
            class="info-table"
            v-if="!showMultiImport"
        >
            <apply-form
                ref="applyForm"
                :leaders="leaders"
                :campus-list="campusList"
                :college-list="collegeList"
                @campusChange="changeCollegeList"
            ></apply-form>
        </div>
        <div
            class="multi-import-page"
            v-if="showMultiImport"
        >
            <multi-table
                @showInput="changeInputVisible"
                ref="multiTable"
            ></multi-table>
        </div>
        <bk-dialog
            v-model="inputVisible"
            theme="primary"
            :width="500"
            :mask-close="false"
            :header-position="'center'"
            :confirm-fn="confirmMultiCommit"
            ok-text="确定提交"
            title="请完善信息"
        >
            <bk-form
                :label-width="80"
                ref="inputForm"
            >
                <bk-container
                    :col="12"
                    :margin="6"
                >
                    <bk-row style="margin-bottom: 25px;">
                        <bk-col :span="12">
                            <div class="leaders">
                                <bk-form-item label="导员">
                                    <bk-tag>{{ multiInput.leaders }}</bk-tag>
                                </bk-form-item>
                            </div>
                        </bk-col>
                    </bk-row>
                    <bk-row style="margin-bottom: 25px;">
                        <bk-col :span="12">
                            <div class="campus">
                                <bk-form-item
                                    label="校区"
                                    :required="true"
                                    :property="'multiCampus'"
                                >
                                    <bk-select
                                        v-model="multiInput.campus"
                                        style="width: 80%"
                                    >
                                        <bk-option
                                            v-for="option in campusList"
                                            :key="option.id"
                                            :id="option.id"
                                            :name="option.name"
                                        >
                                        </bk-option>
                                    </bk-select>
                                </bk-form-item>
                            </div>
                        </bk-col>
                    </bk-row>
                    <bk-row style="margin-bottom: 25px;">
                        <bk-col :span="12">
                            <div class="college">
                                <bk-form-item
                                    label="学院"
                                    :required="true"
                                    :property="'multiCollege'"
                                >
                                    <bk-select
                                        v-model="multiInput.college"
                                        style="width: 80%"
                                    >
                                        <bk-option
                                            v-for="option in collegeList"
                                            :key="option.id"
                                            :id="option.id"
                                            :name="option.name"
                                        >
                                        </bk-option>
                                    </bk-select>
                                </bk-form-item>
                            </div>
                        </bk-col>
                    </bk-row>
                    <bk-row style="margin-bottom: 25px;">
                        <bk-col :span="12">
                            <div class="specificLocation">
                                <bk-form-item
                                    label="具体地点"
                                    :required="true"
                                    :property="'multiSpecificLocation'"
                                >
                                    <bk-input
                                        v-model="multiInput.specificLocation"
                                        placeholder=""
                                        style="width: 80%"
                                    ></bk-input>
                                </bk-form-item>
                            </div>
                        </bk-col>
                    </bk-row>
                    <bk-row style="margin-bottom: 25px;">
                        <bk-col :span="12">
                            <div class="apply-reason">
                                <bk-form-item
                                    :required="true"
                                    label="申请原因"
                                    :property="'multiApplyReason'"
                                >
                                    <bk-input
                                        type="textarea"
                                        v-model="multiInput.applyReason"
                                        style="width: 80%"
                                    ></bk-input>
                                </bk-form-item>
                            </div>
                        </bk-col>
                    </bk-row>
                </bk-container>
            </bk-form>
        </bk-dialog>
    </div>
</template>

<script>
    import { mapState } from 'vuex'
    import {
        getRootPositionListUrl, getSubPositionListUrl, getLeadersUrl, commitApplyUrl
    } from '@/pattern'
    import ApplyForm from '@/components/apply/home/applyForm.vue'
    import MultiTable from '@/components/apply/home/multiTable.vue'

    export default {
        components: {
            ApplyForm,
            MultiTable
        },
        data () {
            return {
                showMultiImport: false,
                leaders: '',
                inputVisible: false,
                multiInput: { // 批量导入时所需填写的表格数据
                    leaders: '无',
                    campus: '',
                    college: '',
                    specificLocation: '',
                    applyReason: ''
                },
                precision: 0,
                campusList: [], // 校区列表
                collegeList: [] // 学院列表
            }
        },
        computed: {
            ...mapState({
                userInfo: state => state.user.userInfo
            })
        },
        watch: {
            '$store.state.isApplyViewSwitcherOn' (val) {
                this.showMultiImport = val
                if (val) {
                    this.$nextTick(() => {
                        this.$refs.multiTable.changUploadName()
                    })
                }
            },
            'multiInput.campus' (val) { // 监听批量导入时的页面表格的校区变量
                this.changeCollegeList(val)
            }
        },
        created () {
            this.loadData() // 创建实例时加载数据
        },
        mounted () {
            this.$store.commit('updateViewInfo', {
                viewInfo: '批量申请',
                hasApplyViewSwitcher: true
            })
        },
        methods: {
            loadData () {
                this.getRootPositionList()
                this.getLeaders()
            },
            getLeaders () {
                this.$http.get(getLeadersUrl).then(res => {
                    if (res) {
                        if (res.result === true && res.code !== '220') {
                            this.leaders = res.data
                        }
                    }
                })
            },
            changeCollegeList (val) {
                const parentCode = this.getParentCode(val)
                this.$http.get(getSubPositionListUrl, { params: { parent_code: parentCode } }).then(res => {
                    this.collegeList = res.data
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
            confirmMultiCommit () {
                if (!this.multiInput.campus || !this.multiInput.specificLocation || !this.multiInput.applyReason || !this.multiInput.college) {
                    this.handleError({ theme: 'warning' }, '任何数据不能为空')
                    return
                }
                const applyList = []
                const allSuccessApply = this.$refs.multiTable.allSuccessApply
                const pagination = this.$refs.multiTable.pagination
                const selected = this.$refs.multiTable.selected
                for (let index = 0; index < allSuccessApply.length; index++) {
                    const selectedIdx = selected.selectedRows.indexOf(allSuccessApply[index].id)
                    if (selectedIdx !== -1) {
                        allSuccessApply[index]['good_code'] = allSuccessApply[index]['goodCode']
                        delete allSuccessApply[index].goodCode
                        allSuccessApply[index]['good_name'] = allSuccessApply[index]['goodName']
                        delete allSuccessApply[index].goodName
                        allSuccessApply[index]['require_date'] = allSuccessApply[index]['getDate'] ? this.moment(allSuccessApply[index]['getDate']).format('YYYY-MM-DD') : ''
                        delete allSuccessApply[index].getDate
                        allSuccessApply[index]['apply_user'] = allSuccessApply[index]['applicant']
                        delete allSuccessApply[index].applicant
                        allSuccessApply[index]['leaders'] = this.multiInput.leaders
                        allSuccessApply[index]['school'] = this.campusList.find(obj => obj.id === this.multiInput.campus).name
                        allSuccessApply[index]['academy'] = this.collegeList.find(obj => obj.id === this.multiInput.college).name
                        allSuccessApply[index]['detail_position'] = this.multiInput.specificLocation
                        allSuccessApply[index]['reason'] = this.multiInput.applyReason
                        applyList.push(allSuccessApply[index])
                    }
                }
                for (let index = 0; index < applyList.length; index++) {
                    const allApplyIdx = allSuccessApply.indexOf(applyList[index])
                    allSuccessApply.splice(allApplyIdx, 1)
                }
                this.$http.post(commitApplyUrl, { apply_list: applyList }).then(res => {
                    if (res.result === true) {
                        this.handleError({ theme: 'success' }, res.message)
                    } else if (res.result === false) {
                        this.handleError({ theme: 'error' }, res.message)
                    }
                })
                selected.selectedRows = []
                this.$refs.multiTable.getSuccessApply(pagination.current)
                this.inputVisible = false
            },
            multiImport () { // 批量导入触发
                this.showMultiImport = true
                const pagination = this.$refs.multiTable.pagination
                this.$refs.multiTable.getSuccessApply(pagination.current)
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
            changeInputVisible (val) {
                this.inputVisible = val
            }
        }
    }
</script>

<style lang="postcss" scoped>
    .applyHome-wrapper {
        overflow-x: hidden;
        .switcher {
            padding: 15px 0px 0px 0px;
        }
        .info-table {
            width: 100%;
            padding-bottom: 30px;
            overflow: auto;
        }
        .multi-import-page {
            padding: 15px 0 0 0;
            width: 100%;
        }
    }
    /deep/.bk-dialog-wrapper .bk-dialog-content {
        border-radius: 8px;
    }
    /deep/.bk-dialog-wrapper .bk-dialog-footer {
        border-radius: 8px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
</style>
