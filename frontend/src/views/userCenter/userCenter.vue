<template>
    <div class="userCenter-wrapper">
        <div class="Info" style="width: 100%;">
            <bk-form :label-width="100" :model="userInfo" :rules="rules" ref="userInfo" class="InfoForm">
                <bk-container :col="12" :gutter="8">
                    <bk-row style="margin-bottom: 20px;">
                        <bk-col :span="11">
                            <bk-form-item label="用户名" :required="true" :property="'name'" :error-display-type="'normal'">
                                <bk-input v-model="userInfo.username" placeholder="请输入新的用户名" :disabled="true"></bk-input>
                            </bk-form-item>
                        </bk-col>
                    </bk-row>
                    <bk-row style="margin-bottom: 20px;">
                        <bk-col :span="11">
                            <bk-form-item label="手机号码" :property="'phone'" :required="true" :error-display-type="'normal'">
                                <bk-input v-model="userInfo.phone" placeholder="请输入手机号码" :disabled="editable"></bk-input>
                            </bk-form-item>
                        </bk-col>
                    </bk-row>
                    <bk-row style="margin-bottom: 20px;">
                        <bk-col :span="12">
                            <bk-form-item label="所在地区" :error-display-type="'normal'">
                                <bk-select :disabled="editable" v-model="userInfo.position" style="width: 80%"
                                    ext-cls="select-custom"
                                    ext-popover-cls="select-popover-custom"
                                    searchable>
                                    <bk-option
                                        key="0"
                                        id="0"
                                        name="无">
                                    </bk-option>
                                    <bk-option v-for="option in locationList"
                                        :key="option.id"
                                        :id="option.name"
                                        :name="option.name">
                                    </bk-option>
                                </bk-select>
                            </bk-form-item>
                        </bk-col>
                    </bk-row>
                    <bk-row style="margin-bottom: 20px;">
                        <bk-col :span="6">
                            <bk-form-item class="mt20">
                                <bk-button :theme="'primary'" :title="'修改信息'" class="mr10" @click="editInfo" v-if="editable">
                                    修改信息
                                </bk-button>
                                <bk-button :theme="'warning'" :title="'取消修改'" class="mr10" @click="cancelEdit" v-if="!editable">
                                    取消修改
                                </bk-button>
                            </bk-form-item>
                        </bk-col>
                        <bk-col :span="6">
                            <bk-form-item class="mt20">
                                <bk-button :theme="'success'" :title="'确定修改'" @click="confirmEdit" v-if="!editable">
                                    确定修改
                                </bk-button>
                            </bk-form-item>
                            <bk-dialog v-model="submitDialogVisible"
                                width="400"
                                :render-directive="'if'"
                                :mask-close="false"
                                :header-position="left"
                                @confirm="submitEdit"
                                :esc-close="false">
                                确定修改?
                            </bk-dialog>
                        </bk-col>
                    </bk-row>
                </bk-container>
            </bk-form>
        </div>
    </div>
</template>

<script>
    const getPositionsUrl = '/apply/get_position_list' // 获取所有地区接口
    const getUserInfoUrl = '/purchase/get_user_info' // 获取用户信息
    const editUserInfoUrl = '/purchase/edit_user_info' // 修改用户信息

    export default {
        data () {
            return {
                userInfo: {
                    username: '',
                    phone: '',
                    position: 0
                },
                cacheUserInfo: '',
                editable: true,
                locationList: '',
                submitDialogVisible: false,
                rules: {
                    name: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        },
                        {
                            max: 30,
                            message: '不能多于30个字符',
                            trigger: 'blur'
                        }
                    ],
                    phone: [
                        {
                            max: 11,
                            message: '不能多于11个字符',
                            trigger: 'blur'
                        },
                        {
                            validator: this.checkPhone,
                            message: '号码格式错误',
                            trigger: 'blur'
                        }
                    ]
                }
            }
        },
        created () {
            this.loadData()
        },
        methods: {
            loadData () {
                this.userInfo.username = this.$store.state.user.username
                this.getPosition()
                this.getUserInfo()
            },
            getPosition () { // 获得所有地点
                this.$http.get(getPositionsUrl).then(res => {
                    if (res) {
                        if (res && res.result === true) {
                            this.locationList = res.data
                        } else if (res && res.result === false) {
                            this.handleError({ theme: 'error' }, res.message)
                        }
                    }
                })
            },
            getUserInfo () {
                this.$http.post(getUserInfoUrl).then(res => {
                    if (res) {
                        if (res && res.result === true) {
                            this.userInfo.phone = res.data.phone
                            this.userInfo.position = res.data.position
                        } else if (res && res.result === false) {
                            this.handleError({ theme: 'error' }, res.message)
                        }
                    }
                })
            },
            editInfo () {
                this.cacheUserInfo = JSON.stringify(this.userInfo)
                this.editable = false
            },
            cancelEdit () {
                this.userInfo = JSON.parse(this.cacheUserInfo)
                this.editable = true
                this.$refs.userInfo.clearError()
            },
            confirmEdit () {
                this.$refs.userInfo.validate().then(validator => {
                    this.submitDialogVisible = true
                })
            },
            submitEdit () {
                const editForm = new FormData()
                editForm.append('phone', this.userInfo['phone'])
                editForm.append('position', this.userInfo['position'])
                this.$http.post(editUserInfoUrl, editForm, { headers: { 'Content-Type': 'multipart/form-data' } }).then(res => {
                    if (res) {
                        if (res && res.result === true) {
                            this.handleError({ theme: 'success' }, res.message)
                            this.editable = true
                            this.$refs.userInfo.clearError()
                            this.getUserInfo()
                        } else if (res && res.result === false) {
                            this.handleError({ theme: 'error' }, res.message)
                        }
                    }
                })
            },
            checkPhone (val) {
                if (val) {
                    if (!(/^1(3|4|5|6|7|8|9)\d{9}$/.test(val))) {
                        return false
                    }
                }
                return true
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
.userCenter-wrapper{
    .Info{
        .InfoForm{

        }
    }
}
</style>
