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
                                <div class="goodName">
                                    <bk-form-item
                                        label="物品名称"
                                        :property="'goodName'"
                                    >
                                        <bk-input
                                            v-model="formData.good_name"
                                            placeholder="请输入"
                                        ></bk-input>
                                    </bk-form-item>
                                </div>
                            </bk-col>
                            <bk-col :span="3">
                                <div class="goodCode">
                                    <bk-form-item
                                        label="物品编号"
                                        :property="'goodCode'"
                                    >
                                        <bk-input
                                            v-model="formData.good_code"
                                            placeholder="请输入"
                                        ></bk-input>
                                    </bk-form-item>
                                </div>
                            </bk-col>
                            <bk-col :span="3">
                                <div class="applyReason">
                                    <bk-form-item
                                        label="申请原因"
                                        :property="'applyReason'"
                                    >
                                        <bk-input
                                            v-model="formData.apply_reason"
                                            placeholder="请输入"
                                        ></bk-input>
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
                            <bk-col :span="3">
                                <div class="status">
                                    <bk-form-item
                                        label="状态"
                                        :property="'status'"
                                    >
                                        <bk-select v-model="formData.status">
                                            <bk-option
                                                key="999"
                                                id="999"
                                                name="全部"
                                            >
                                            </bk-option>
                                            <bk-option
                                                v-for="option in statusList"
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
                                size="large"
                                :outline="true"
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
    import { getApplyStatusUrl } from '@/pattern'
    export default {
        data () {
            return {
                endDateOptions: {}, // 禁用日期
                startDateOptions: {}, // 禁用日期
                formData: { // 查询条件表单数据
                    good_name: '',
                    good_code: '',
                    apply_reason: '',
                    startDate: '',
                    endDate: '',
                    status: 999
                },
                statusList: []
            }
        },
        watch: {
            'formData.startDate' (val) {
                if (val) {
                    this.endDateOptions = {
                        disabledDate (date) {
                            if (date < val.setDate(val.getDate())) {
                                return true
                            }
                            return false
                        }
                    }
                }
            },
            'formData.endDate' (val) {
                if (val) {
                    this.startDateOptions = {
                        disabledDate (date) {
                            if (date > val.setDate(val.getDate())) {
                                return true
                            }
                            return false
                        }
                    }
                }
            }
        },
        created () {
            this.getApplyStatus()
        },
        methods: {
            getApplyStatus () {
                this.$http.get(getApplyStatusUrl).then(res => {
                    if (res) {
                        this.statusList = res.data
                    }
                })
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
            margin-bottom: 15px;
        }
    }
</style>
