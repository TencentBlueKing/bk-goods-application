<template>
    <div class="form-manage">
        <div class="header">
            <bk-divider align="left">
                <router-link :to="{ name: 'itemManagement' }">
                    <bk-tag
                        type="filled"
                        style="font-size: 13px"
                    ><span>物品管理</span></bk-tag>
                </router-link>
                <bk-tag
                    type="filled"
                    style="font-size: 13px"
                ><span>{{$route.query.action === 'create' ? `物品添加` : '物品编辑'}}</span></bk-tag>
            </bk-divider>
        </div>
        <bk-container
            :col="12"
            :margin="6"
            style="margin-top:40px"
        >
            <bk-form
                :model="goodFormData"
                :rules="rules"
                class="good-form"
                ref="checkForm"
                :label-width="100"
            >
                <bk-row
                    class="good-row"
                    style="display: flex;"
                >
                    <bk-form-item
                        label="物品编码"
                        :required="true"
                        :property="'good_code'"
                        style="width: 25%"
                    >
                        <bk-input
                            v-model="goodFormData.good_code"
                            placeholder="请输入1到30个以内的字符"
                        ></bk-input>
                    </bk-form-item>
                    <bk-form-item
                        label="物品类型"
                        :required="true"
                        :property="'good_type_id'"
                        style="margin-left:10px; width: 25%"
                    >
                        <bk-select
                            :disabled="false"
                            v-model="goodFormData.good_type_id"
                            searchable
                        >
                            <bk-option
                                v-for="goodType in goodTypeList"
                                :key="goodType.id"
                                :id="goodType.id"
                                :name="goodType.type_name"
                            >
                            </bk-option>
                            <div
                                slot="extension"
                                @click="addGoodTypeDialog.visiable = true"
                                style="cursor: pointer"
                            >
                                <i class="bk-icon icon-plus-circle"></i>新增
                            </div>
                        </bk-select>
                    </bk-form-item>
                    <bk-form-item
                        label="参考价"
                        :required="true"
                        :property="'price'"
                        style="margin-left:10px; width: 25%"
                    >
                        <bk-input
                            type="number"
                            :precision="2"
                            v-model="goodFormData.price"
                        >
                        </bk-input>
                    </bk-form-item>
                    <bk-form-item
                        label="物品名称"
                        :required="true"
                        :property="'good_name'"
                        style="margin-left:10px; width: 25%"
                    >
                        <bk-input
                            v-model="goodFormData.good_name"
                            placeholder="请输入物品名称（50字以内）"
                        ></bk-input>
                    </bk-form-item>
                </bk-row>
                <bk-row class="good-row">
                    <bk-form-item
                        label="备注"
                        :required="true"
                        :property="'remark'"
                    >
                        <bk-input
                            type="textarea"
                            v-model="goodFormData.remark"
                            placeholder="请输入物品备注"
                            style="width: 80%"
                        ></bk-input>
                    </bk-form-item>
                </bk-row>
                <bk-row class="good-row">
                    <bk-form-item
                        label="参考图"
                        :required="true"
                        :property="'pics'"
                    >
                        <bk-upload
                            :theme="'picture'"
                            :with-credentials="true"
                            :handle-res-code="handleRes"
                            :limit="picsLimit"
                            :custom-request="uploadImg"
                            :files="goodFormData.pics"
                            @on-delete="deleteImg"
                        ></bk-upload>
                    </bk-form-item>
                </bk-row>
                <bk-row class="good-row">
                    <bk-form-item
                        label="物品介绍"
                        :property="'introduce'"
                    >
                        <v-md-editor
                            v-model="goodFormData.introduce"
                            left-toolbar="undo redo | image"
                            :disabled-menus="[]"
                            @upload-image="handleUploadImage"
                        />
                    </bk-form-item>
                </bk-row>
                <bk-row class="good-row">
                    <bk-form-item
                        label="物品规格"
                        :property="'specifications'"
                    >
                        <v-md-editor
                            v-model="goodFormData.specifications"
                            left-toolbar="undo redo | image"
                            :disabled-menus="[]"
                            @upload-image="handleUploadImage"
                        />
                    </bk-form-item>
                </bk-row>
            </bk-form>
        </bk-container>
        <div
            slot="footer"
            class="form-footer"
        >
            <bk-button
                :theme="'primary'"
                :title="'确认'"
                class="mr10"
                @click="submitAddOrUpdateGood"
            >
                保存
            </bk-button>
        </div>
        <bk-dialog
            v-model="addGoodTypeDialog.visiable"
            theme="primary"
            :mask-close="false"
            title="添加物品类型"
        >
            <div class="add-type-wrapper">
                <span style="width: 20%">类型名称：</span>
                <bk-input
                    :clearable="true"
                    v-model="addGoodTypeDialog.typeName"
                    style="width: 65%"
                ></bk-input>
            </div>
            <div slot="footer">
                <bk-button
                    :theme="'primary'"
                    :title="'确认'"
                    class="mr10"
                    @click="addGoodType"
                >
                    确认
                </bk-button>
                <bk-button
                    :theme="'default'"
                    :title="'取消'"
                    class="mr10"
                    @click="addGoodTypeDialog.visiable = false"
                >
                    取消
                </bk-button>
            </div>
        </bk-dialog>
    </div>
</template>

<script>

    import {
        ADD_GOOD_URL, UPDATE_GOOD_URL, UPLOAD_IMG_URL,
        ADD_GOOD_TYPE_URL, DEL_PICS_URL, GET_GOOD_TYPE_LIST_URL,
        GET_GOOD_DETAIL_URL
    } from '@/pattern'

    export default {
        data () {
            return {
                addGoodTypeDialog: {
                    visiable: false,
                    typeName: ''
                },
                // 物品类型信息
                goodTypeList: [],
                // 物品添加/编辑form
                goodFormData: {
                    good_code: '',
                    good_name: '',
                    good_type_id: '',
                    price: 0.00,
                    pics: [],
                    remark: '',
                    introduce: '',
                    specifications: ''
                },
                rules: {
                    good_code: [
                        {
                            required: true,
                            message: '物品编码必填项',
                            trigger: 'blur'
                        }, {
                            min: 3,
                            message: function (val) {
                                return `${val}不能小于3个字符`
                            },
                            trigger: 'blur'
                        }, {
                            max: 20,
                            message: '不能多于20个字符',
                            trigger: 'blur'
                        }

                    ],
                    good_name: [
                        {
                            required: true,
                            message: '必填项',
                            trigger: 'blur'
                        }, {
                            max: 50,
                            message: '不能多于50个字符',
                            trigger: 'blur'
                        }

                    ],
                    good_type_id: [
                        {
                            required: true,
                            message: '请选择物品类型',
                            trigger: 'blur'
                        }
                    ],
                    price: [
                        {
                            required: true,
                            message: '请选择物品参考价',
                            trigger: 'blur'
                        }
                    ],
                    remark: [
                        {
                            required: true,
                            message: '请填写备注',
                            trigger: 'blur'
                        }
                    ],
                    pics: [
                        {
                            required: true,
                            message: '商品参考图不可为空',
                            trigger: 'blur'
                        }
                    ]
                },
                toolTips: {
                    top: {
                        content: '两位小数',
                        showOnInit: true,
                        placements: ['top']
                    }
                },
                picsLimit: 6
            }
        },
        created () {
            this.getGoodTypes()
            if (this.$route.query.action === 'update' && this.$route.query.row_id) {
                this.getGoodInfo(this.$route.query.row_id)
            }
        },
        methods: {
            getGoodTypes () {
                this.isGoodTypesLoad = true
                this.$http.get(GET_GOOD_TYPE_LIST_URL).then(res => {
                    if (res.result) {
                        this.goodTypeList = res.data
                    }
                }).finally(() => {
                    this.isGoodTypesLoad = false
                })
            },
            dealGoodPics () {
                // 处理提交表单前的图片路径
                let picUrls = []
                this.goodFormData.pics.forEach(pic => {
                    picUrls.push(pic.url)
                })
                picUrls = picUrls.join(';')
                return picUrls
            },
            addGood () {
                const formData = JSON.parse(JSON.stringify(this.goodFormData))
                const picUrls = this.dealGoodPics()
                formData.pics = picUrls
                this.$http.post(ADD_GOOD_URL, formData).then(res => {
                    const config = {
                        'offsetY': 80,
                        'delay': 2000
                    }
                    if (res.result) {
                        config.theme = 'success'
                        config.message = '添加物品成功'
                        this.$bkMessage(config)
                        this.$router.push({ name: 'itemManagement' })
                    } else {
                        config.theme = 'error'
                        config.message = res.message
                        this.$bkMessage(config)
                    }
                })
            },
            updateGood () {
                const formData = JSON.parse(JSON.stringify(this.goodFormData))
                const picUrls = this.dealGoodPics()
                formData.pics = picUrls
                formData.id = this.$route.query.row_id
                this.$http.post(UPDATE_GOOD_URL, formData).then(res => {
                    const config = {
                        'offsetY': 80,
                        'delay': 2000
                    }
                    if (res.result) {
                        config.theme = 'success'
                        config.message = '编辑物品信息成功'
                        this.$bkMessage(config)
                        this.$router.push({ name: 'itemManagement' })
                    } else {
                        config.theme = 'error'
                        config.message = res.message
                        this.$bkMessage(config)
                    }
                })
            },
            getBase64 (file) {
                return new Promise(function (resolve, reject) {
                    const reader = new FileReader()
                    let imgResult = ''
                    reader.readAsDataURL(file)
                    reader.onload = function () {
                        imgResult = reader.result
                    }
                    reader.onerror = function (error) {
                        reject(error)
                    }
                    reader.onloadend = function () {
                        resolve(imgResult)
                    }
                })
            },
            uploadImg (files) {
                console.log('files:', files.fileObj)
                this.getBase64(files.fileObj.origin).then(res => {
                    const fileType = files.fileObj.name.split('.')[1]
                    const fileData = res.split(',')[1]
                    this.$http.post(UPLOAD_IMG_URL, { img: fileData, img_type: fileType }).then(res => {
                        if (res.result) {
                            const picUrl = res.data.pic_url
                            // console.log('picUrl:', picUrl)
                            const pic = {
                                'name': picUrl.split('/')[1],
                                'url': picUrl
                            }
                            this.goodFormData.pics.push(pic)
                            return true
                        }
                    })
                }).catch(() => {
                    console.log('文件解析失败')
                    return false
                })
            },
            handleUploadImage (event, insertImage, files) {
                files.forEach(file => {
                    this.getBase64(file).then(res => {
                        const fileType = file.name.split('.')[1]
                        const fileData = res.split(',')[1]
                        this.$http.post(UPLOAD_IMG_URL, { img: fileData, img_type: fileType }).then(res => {
                            if (res.result) {
                                insertImage({
                                    url: res.data.pic_url
                                })
                            }
                        })
                    })
                })
            },
            addGoodType () {
                this.$http.post(ADD_GOOD_TYPE_URL, { type_name: this.addGoodTypeDialog.typeName }).then(res => {
                    const config = {
                        'offsetY': 80
                    }
                    if (res.result) {
                        config.theme = 'success'
                        config.message = '添加物品类型成功'
                        this.$bkMessage(config)
                        // 重新获取物品类型
                        this.getGoodTypes()
                        // 清空输入栏
                        this.addGoodTypeDialog.typeName = ''
                        this.goodFormData.good_type_id = res.data.id
                        this.addGoodTypeDialog.visiable = false
                    } else {
                        config.theme = 'error'
                        config.message = res.message
                        this.$bkMessage(config)
                    }
                })
            },
            deleteImg (file, fileList) {
                this.goodFormData.pics = fileList
                const picUrl = file.url
                this.del_pics.push(picUrl.split('/')[picUrl.split('/').length - 2] + '\\' + picUrl.split('/')[picUrl.split('/').length - 1])
            },
            submitAddOrUpdateGood () {
                // 校验表单
                this.$refs.checkForm.validate().then(validator => {
                    if (this.$route.query.action === 'update' && this.$route.query.row_id) {
                        this.updateGood()
                    } else {
                        this.addGood()
                    }
                    const delForm = this.del_pics
                    if (this.del_pics.length !== 0) {
                        this.$http.post(DEL_PICS_URL, delForm)
                    }
                    this.del_pics = []
                }, validator => {
                    // 验证失败
                    this.$bkMessage({
                        offsetY: 100,
                        theme: 'error',
                        delay: 2000,
                        message: validator.content
                    })
                })
            },
            getGoodInfo (goodId) {
                this.$http.get(GET_GOOD_DETAIL_URL, {
                    params: {
                        good_id: goodId
                    }
                }).then(res => {
                    if (res.result) {
                        this.goodFormData.good_code = res.data.good_code
                        this.goodFormData.good_name = res.data.good_name
                        this.goodFormData.good_type_id = res.data.good_type_id
                        this.goodFormData.price = res.data.price
                        // 处理图片
                        const picfiles = []
                        res.data.pics.forEach(url => {
                            // 避免出现空字符串
                            if (url.length !== 0) {
                                const pic = {
                                    'name': url.split('/')[1],
                                    'url': url
                                }
                                picfiles.push(pic)
                            }
                        })
                        this.goodFormData.pics = picfiles
                        this.goodFormData.remark = res.data.remark
                        this.goodFormData.specifications = res.data.specifications
                        this.goodFormData.introduce = res.data.introduce
                    }
                })
            }
        }
    }
</script>
<style lang="postcss" scoped>
    .form-manage {
        padding: 20px;
        overflow: auto;
        width: 100%;
        height: 100%;
        .good-form {
            flex: 1;
            margin-right: 20px;
            .good-row {
                margin-bottom: 20px;
            }
            .bk-form-item .bk-form-content .bk-form-control .group-box {
                border-right: none;
                .group-text {
                    padding: 0 4px;
                }
            }
        }
        .form-footer {
            display: flex;
            justify-content: center;
            align-items: center;
        }
    }
    /deep/ .bk-form-item + .bk-form-item {
        margin-top: 0px;
    }
</style>
