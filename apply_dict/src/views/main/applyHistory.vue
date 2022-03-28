<template>
    <div class="applyHistory-wrapper">
        <div class="condition-form">
            <history-form
                @search="handleSearch"
                ref="historyForm"
            ></history-form>
        </div>
        <div class="historyTable">
            <history-table
                @edit="editHistory"
                @destroy="deleteHistory"
                ref="historyTable"
            ></history-table>
            <div class="edit-history-dialog">
                <bk-dialog
                    v-model="editDialogVisible"
                    :render-directive="'show'"
                    theme="primary"
                    :width="700"
                    :mask-close="false"
                    :header-position="'center'"
                    :confirm-fn="confirmEdit"
                    ok-text="确定修改"
                    title="编辑申请记录"
                >
                    <div>
                        <bk-form
                            :label-width="100"
                            :model="remark"
                            :rules="rules"
                            ref="remark"
                        >
                            <bk-container
                                :col="12"
                                :margin="6"
                            >
                                <bk-row style="margin: 0 0 30px 0;">
                                    <bk-col :span="6">
                                        <div>
                                            <bk-form-item
                                                label="物品名称"
                                                :property="'goodName'"
                                            >
                                                <bk-input
                                                    v-model="editFormData.good_name"
                                                    placeholder="请输入"
                                                ></bk-input>
                                            </bk-form-item>
                                        </div>
                                    </bk-col>
                                    <bk-col :span="6">
                                        <div>
                                            <bk-form-item
                                                label="物品编号"
                                                :property="'goodCode'"
                                            >
                                                <bk-input
                                                    v-model="editFormData.good_code"
                                                    placeholder="请输入"
                                                ></bk-input>
                                            </bk-form-item>
                                        </div>
                                    </bk-col>
                                </bk-row>
                                <bk-row style="margin: 0 0 30px 0;">
                                    <bk-col :span="6">
                                        <div>
                                            <bk-form-item
                                                label="申请原因"
                                                :property="'applyReason'"
                                            >
                                                <bk-input
                                                    v-model="editFormData.reason"
                                                    placeholder="请输入"
                                                ></bk-input>
                                            </bk-form-item>
                                        </div>
                                    </bk-col>
                                    <bk-col :span="6">
                                        <div class="apply-num">
                                            <bk-form-item label="申请数量">
                                                <bk-input
                                                    type="number"
                                                    :min="1"
                                                    :precision="precision"
                                                    v-model="editFormData.num"
                                                ></bk-input>
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
                <bk-dialog
                    v-model="deleteDialogVisible"
                    :render-directive="'show'"
                    theme="primary"
                    :width="700"
                    :mask-close="false"
                    :header-position="'center'"
                    :confirm-fn="confirmDelete"
                    ok-text="确定删除"
                    title="确定删除记录？"
                >
                </bk-dialog>
            </div>
        </div>
    </div>
</template>

<script>
    import {
        editApplyUrl, deleteApplyUrl
    } from '@/pattern'
    import HistoryForm from '@/components/apply/history/historyForm.vue'
    import HistoryTable from '@/components/apply/history/historyTable.vue'

    export default {
        components: {
            HistoryForm,
            HistoryTable
        },
        data () {
            return {
                editFormData: {},
                deleteApplyId: 0,
                precision: 0,
                editDialogVisible: false,
                deleteDialogVisible: false
            }
        },
        methods: {
            handleSearch (formData) {
                this.$refs.historyTable.search(formData)
            },
            editHistory (row) {
                this.editDialogVisible = true
                this.editFormData = row
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
                    school = positionList[0]
                    academy = positionList[1]
                    if (positionList.length > 2) {
                        detailPosition = positionList[2]
                    }
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
                        this.$refs.historyTable.getGoodApplyList()
                    }
                })
            },
            confirmDelete () {
                this.deleteDialogVisible = false
                this.$http.post(deleteApplyUrl, {
                    id: this.deleteApplyId
                }).then(res => {
                    if (res.result === true) {
                        this.handleError({ theme: 'success' }, res.message)
                        this.$refs.historyTable.getGoodApplyList()
                    }
                })
            },
            handleError (config, message) { // 遇到后台报自定义错误时上方弹窗提醒
                config.message = message
                config.offsetY = 80
                this.$bkMessage(config)
            }
        }
    }
</script>

<style lang="postcss" scoped>
    .applyHistory-wrapper {
        .condition-form {
            padding: 30px 0 0 0;
        }
        .historyTable {
            text-align: right;
            .more-options {
                margin: 0 10px 10px 0;
                .multi-export:hover {
                }
            }
        }
    }
</style>
