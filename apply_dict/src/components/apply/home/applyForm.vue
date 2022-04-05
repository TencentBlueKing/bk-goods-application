<template>
    <div class="form-container">
        <bk-form
            :label-width="130"
            :model="formData"
            :rules="rules"
            ref="infoForm"
            class="form-content"
        >
            <bk-container
                :col="12"
                :margin="6"
            >
                <bk-row style="margin-bottom: 20px;">
                    <bk-col :span="4">
                        <div style="display: flex; flex-direction: column; place-content:center; place-items:center">
                            <h2 style="color: black">基本信息</h2>
                            <div style="height: 8px; background: blue; width: 120px; margin-top:-10px; ; border-radius: 6px"></div>
                        </div>
                    </bk-col>
                </bk-row>
                <bk-row class="info-row">
                    <bk-col
                        :span="4"
                        :offset="2"
                    >
                        <div class="campus">
                            <bk-form-item
                                label="校区"
                                :required="true"
                                :property="'campus'"
                            >
                                <bk-select v-model="formData.campus">
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
                    <bk-col :span="4">
                        <div class="college">
                            <bk-form-item
                                label="学院"
                                :required="true"
                                :property="'college'"
                            >
                                <bk-select v-model="formData.college">
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
                <bk-row>
                    <bk-col :span="4" :offset="2">
                        <div class="get-date">
                            <bk-form-item
                                label="期望领用日期"
                                :property="'getDate'"
                                :required="true"
                            >
                                <bk-date-picker
                                    placeholder="请选择"
                                    :options="dateOptions"
                                    :timer="false"
                                    v-model="formData.getDate"
                                    :disabled="false"
                                    style="width: 100%"
                                >
                                </bk-date-picker>
                            </bk-form-item>
                        </div>
                    </bk-col>
                    <bk-col :span="4">
                        <div class="specificLocation">
                            <bk-form-item
                                label="具体地点"
                                :required="true"
                                :property="'specificLocation'"
                            >
                                <bk-input
                                    v-model="formData.specificLocation"
                                    placeholder=""
                                ></bk-input>
                            </bk-form-item>
                        </div>
                    </bk-col>
                </bk-row>
                <bk-row style="margin-bottom: 20px;">
                    <bk-col :span="4">
                        <div style="display: flex; flex-direction: column; place-content:center; place-items:center">
                            <h2 style="color: black">申请详情</h2>
                            <div style="height: 8px; background: blue; width: 120px; margin-top:-10px; ; border-radius: 6px"></div>
                        </div>
                    </bk-col>
                </bk-row>
                <bk-row class="info-row">
                    <bk-col
                        :span="4"
                        :offset="2"
                    >
                        <div class="applicant">
                            <bk-form-item
                                label="申请人"
                                :property="'applicant'"
                            >
                                <bk-tag style="width:100%; height:32px; display: flex; align-items:center">{{ formData.applicant }}</bk-tag>
                            </bk-form-item>
                        </div>
                    </bk-col>
                    <bk-col :span="4">
                        <div class="apply-num">
                            <bk-form-item
                                label="申请数量"
                                :property="'applyNum'"
                            >
                                <bk-input
                                    type="number"
                                    :min="1"
                                    :precision="precision"
                                    v-model="formData.num"
                                ></bk-input>
                            </bk-form-item>
                        </div>
                    </bk-col>
                </bk-row>
                <bk-row>
                    <bk-col
                        :span="4"
                        :offset="2"
                    >
                        <bk-row class="info-row">
                            <div class="apply-good-name">
                                <bk-form-item
                                    label="申请物品名"
                                    :required="true"
                                    :property="'goodName'"
                                >
                                    <bk-input
                                        v-model="formData.goodName"
                                        placeholder=""
                                    ></bk-input>
                                </bk-form-item>
                            </div>
                        </bk-row>
                        <bk-row class="info-row">
                            <div class="apply-good-code">
                                <bk-form-item
                                    label="申请物品编号"
                                    :required="true"
                                    :property="'goodCode'"
                                >
                                    <bk-input
                                        v-model="formData.goodCode"
                                        placeholder=""
                                    ></bk-input>
                                </bk-form-item>
                            </div>
                        </bk-row>
                    </bk-col>
                    <bk-col :span="4">
                        <div class="apply-reason">
                            <bk-form-item
                                :required="true"
                                label="申请原因"
                                :property="'applyReason'"
                            >
                                <bk-input
                                    type="textarea"
                                    v-model="formData.applyReason"
                                    :rows="6"
                                ></bk-input>
                            </bk-form-item>
                        </div>
                    </bk-col>
                </bk-row>
                <bk-row class="info-row">
                    <bk-col :span="12">
                        <div class="commit">
                            <bk-button
                                size="medium"
                                theme="primary"
                                title="提交申请"
                                @click.stop.prevent="commitApply"
                            >提交申请</bk-button>
                        </div>
                    </bk-col>
                </bk-row>
            </bk-container>
        </bk-form>
    </div>
</template>

<script>
    import {
        commitApplyUrl
    } from '@/pattern'
    import { mapState } from 'vuex'
    export default {
        props: {
            leaders: String,
            campusList: Array,
            collegeList: Array
        },
        data () {
            return {
                formData: {
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
                },
                dateOptions: {
                    disabledDate: function (date) {
                        const myDate = new Date()
                        if (date < myDate.setDate(myDate.getDate() - 1)) {
                            return true
                        }
                        return false
                    }
                } // 禁用日期
            }
        },
        computed: {
            ...mapState({
                userInfo: state => state.user.userInfo
            })
        },
        watch: {
            'formData.campus' (val) {
                // 监听单个导入时的页面表格的校区变量
                this.$emit('campusChange', val)
            }
        },
        created () {
            this.formData.applicant = this.userInfo.username
        },
        methods: {
            commitApply () { // 单个申请触发
                this.$refs.infoForm.validate().then(validator => {
                    const applyList = []
                    const applyObj = {}
                    applyObj['good_code'] = this.formData.goodCode
                    applyObj['good_name'] = this.formData.goodName
                    applyObj['detail_position'] = this.formData.specificLocation
                    applyObj['reason'] = this.formData.applyReason
                    applyObj['num'] = this.formData.num
                    applyObj['apply_user'] = this.formData.applicant
                    applyObj['leaders'] = this.leaders
                    applyObj['require_date'] = this.formData.getDate ? this.moment(this.formData.getDate).format('YYYY-MM-DD') : ''
                    const campus = this.campusList.find(obj => obj.id === this.formData.campus)
                    applyObj['school'] = campus ? campus.name : ''
                    const college = this.collegeList.find(obj => obj.id === this.formData.college)
                    applyObj['academy'] = college ? college.name : ''
                    applyList.push(applyObj)
                    this.$http.post(commitApplyUrl, { apply_list: applyList }).then(res => {
                        if (res.result === true) {
                            this.handleError({ theme: 'success' }, res.message)
                            this.sleep(2).then(res => {
                                this.$router.go(0)
                            })
                        } else if (res.result === false) {
                            this.handleError({ theme: 'error' }, res.message)
                        }
                    })
                }, validator => {
                })
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
            }
        }
    }
</script>

<style lang="postcss" scoped>
    .form-container {
        .form-content {
            .info-row {
                margin-bottom: 50px;
                .applicant {
                }
                .group-leaders {
                }
                .apply-good-name {
                }
                .apply-good-code {
                }
                .campus {
                }
                .college {
                }
                .specificLocation {
                }
                .apply-num {
                }
                .get-date {
                }
                .apply-reason {
                }
                .commit {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
            }
        }
    }
</style>
