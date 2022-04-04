<template>
    <div class="form-content">
        <bk-form
            :label-width="130"
            :model="formData"
            ref="infoForm"
        >
            <bk-container
                :col="12"
                :margin="6"
            >
                <bk-row>
                    <bk-col :span="9">
                        <bk-row class="condition-form-row">
                            <bk-col :span="3">
                                <div>
                                    <bk-form-item
                                        label="申请人"
                                        :property="'applicant'"
                                    >
                                        <bk-select v-model="formData.applicant">
                                            <bk-option
                                                key="0"
                                                id="0"
                                                name="全部"
                                            >
                                            </bk-option>
                                            <bk-option
                                                v-for="option in applicantList"
                                                :key="option.id"
                                                :id="option.username"
                                                :name="option.username"
                                            >
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
                                        :icon-offset="35"
                                    >
                                        <bk-date-picker
                                            :options="startDateOptions"
                                            placeholder="请选择"
                                            :timer="false"
                                            v-model="formData.startDate"
                                            :disabled="false"
                                            style="width: 100%"
                                        >
                                        </bk-date-picker>
                                    </bk-form-item>
                                </div>
                            </bk-col>
                            <bk-col :span="3">
                                <div class="end-date">
                                    <bk-form-item
                                        label="结束时间"
                                        :property="'endDate'"
                                        :icon-offset="0"
                                    >
                                        <bk-date-picker
                                            :options="endDateOptions"
                                            placeholder="请选择"
                                            :timer="false"
                                            v-model="formData.endDate"
                                            :disabled="false"
                                            style="width: 100%"
                                        >
                                        </bk-date-picker>
                                    </bk-form-item>
                                </div>
                            </bk-col>
                        </bk-row>
                        <bk-row class="condition-form-row">
                            <bk-col
                                :span="3"
                                :offset="3"
                            >
                                <div class="campus">
                                    <bk-form-item
                                        label="校区"
                                        :property="'campus'"
                                    >
                                        <bk-select v-model="formData.campus">
                                            <bk-option
                                                key="0"
                                                id="0"
                                                name="全部"
                                            >
                                            </bk-option>
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
                            <bk-col :span="3">
                                <div class="college">
                                    <bk-form-item
                                        label="学院"
                                        :property="'college'"
                                    >
                                        <bk-select v-model="formData.college">
                                            <bk-option
                                                key="0"
                                                id="0"
                                                name="全部"
                                            >
                                            </bk-option>
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
                    </bk-col>
                    <bk-col :span="3">
                        <div style="text-align: center;line-height: 90px;">
                            <bk-button
                                size="medium"
                                theme="primary"
                                title="查询"
                                @click.stop.prevent="search"
                            >查询</bk-button>
                        </div>
                    </bk-col>
                </bk-row>
            </bk-container>
        </bk-form>
    </div>
</template>

<script>
    import { getApplyUserUrl, getRootPositionListUrl, getSubPositionListUrl } from '@/pattern'
    export default {
        data () {
            return {
                formData: { // 查询条件表单数据
                    applicant: 0,
                    startDate: '',
                    endDate: '',
                    campus: 0,
                    college: 0
                },
                applicantList: [],
                startDateOptions: {},
                endDateOptions: {},
                collegeList: [], // 学院列表
                campusList: [] // 校区列表
            }
        },
        watch: {
            'formData.startDate' (val) {
                this.endDateOptions = {
                    disabledDate (date) {
                        if (date < val.setDate(val.getDate())) {
                            return true
                        }
                        return false
                    }
                }
            },
            'formData.endDate' (val) {
                this.startDateOptions = {
                    disabledDate (date) {
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
            this.getApplyUser()
            this.getRootPositionList()
        },
        methods: {
            getApplyUser () { // 获取小组成员
                this.$http.get(getApplyUserUrl).then(res => {
                    if (res) {
                        this.applicantList = res.data
                    }
                })
            },
            getRootPositionList () { // 获取校区列表
                this.$http.get(getRootPositionListUrl).then(res => {
                    this.campusList = res.data
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
            search () {
                this.$emit('search', this.formData)
            }
        }
    }
</script>

<style lang="postcss" scoped>
    .form-content {
        .condition-form-row {
            margin-bottom: 30px;
        }
    }
</style>
