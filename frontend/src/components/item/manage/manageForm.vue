<template>
    <div class="form-manage">
        <bk-dialog
            v-model="goodDialog.visiable"
            theme="primary"
            :header-position="goodDialog.headerPosition"
            :z-index="1100"
            :title="goodDialog.typeList[goodDialog.typeIndex] + '物品'"
            class="good-dialog"
        >
            <div class="form-wrapper">
                <bk-form
                    :model="goodFormData"
                    :rules="rules"
                    :ext-cls="'good-form'"
                    ref="checkForm"
                >
                    <bk-form-item
                        :label-width="80"
                        label="物品编码"
                        :required="true"
                        :property="'good_code'"
                        :icon-offset="145"
                    >
                        <bk-input
                            v-model="goodFormData.good_code"
                            placeholder="请输入1到30个以内的字符"
                            style="width: 70%"
                        ></bk-input>
                    </bk-form-item>
                    <bk-form-item
                        :label-width="80"
                        label="物品类型"
                        :required="true"
                        :property="'good_type_id'"
                        style="width: 74.5%"
                        :icon-offset="25"
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
                                @click="submitAddGoodType"
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
                    <bk-form-item
                        :label-width="80"
                        label="参考价"
                        ext-cls="price-wrapper"
                        :required="true"
                        :property="'price'"
                        :icon-offset="165"
                    >
                        <bk-input
                            type="number"
                            precision="2"
                            v-model="goodFormData.price"
                            title="保留两位小数"
                            style="width: 70%"
                        >
                            <template slot="prepend">
                                <div class="group-text">
                                    <span
                                        v-bk-tooltips="toolTips.top"
                                        class="top-start"
                                    >
                                        <i
                                            class="
                                                bk-icon
                                                icon-info-circle-shape
                                            "
                                        ></i>
                                    </span>
                                </div>
                            </template>
                        </bk-input>
                    </bk-form-item>
                    <div class="remark-wrapper">
                        <span style="margin: 0 25px 0 15px">备注</span>
                        <bk-input
                            type="textarea"
                            v-model="goodFormData.remark"
                            placeholder="请输入物品备注"
                            style="width: 80%"
                        ></bk-input>
                    </div>
                    <!-- <bk-form-item :label-width="80" label="参考图" ext-cls="pics-wrapper" :required="true" :property="'pics'">
                        <bk-upload
                            :theme="'picture'"
                            :with-credentials="true"
                            :handle-res-code="handleRes"
                            :limit="picsLimit"
                            :custom-request="uploadImg"
                            :files="goodFormData.pics"
                            @on-delete="deleteImg"
                        ></bk-upload>
                    </bk-form-item> -->
                </bk-form>
                <bk-container :col="12" :gutter="4" style="width: 50%">
                    <bk-form
                        :model="goodFormData"
                        :rules="rules"
                        :ext-cls="'good-form'"
                        ref="checkForm"
                    >
                        <bk-row style="margin-bottom: 20px">
                            <bk-form-item
                                :label-width="80"
                                label="物品名称"
                                :required="true"
                                :property="'good_name'"
                                :icon-offset="145"
                            >
                                <bk-input
                                    v-model="goodFormData.good_name"
                                    placeholder="请输入物品名称（50字以内）"
                                    style="width: 70%"
                                ></bk-input>
                            </bk-form-item>
                        </bk-row>
                        <bk-row>
                            <bk-form-item
                                :label-width="80"
                                label="参考图"
                                ext-cls="pics-wrapper"
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
                    </bk-form>
                </bk-container>
            </div>
            <div class="text-wrapper">
                <span>物品介绍</span>
                <v-md-editor
                    v-model="goodFormData.introduce"
                    left-toolbar="undo redo | image"
                    :disabled-menus="[]"
                    @upload-image="handleUploadImage"
                    height="350px"
                />
            </div>
            <div class="text-wrapper">
                <span>物品规格</span>
                <v-md-editor
                    v-model="goodFormData.specifications"
                    left-toolbar="undo redo | image"
                    :disabled-menus="[]"
                    @upload-image="handleUploadImage"
                    height="350px"
                />
            </div>
            <div slot="footer">
                <bk-button
                    :theme="'primary'"
                    :title="'确认'"
                    class="mr10"
                    @click="submitAddOrUpdateGood"
                >
                    确认
                </bk-button>
                <bk-button
                    :theme="'default'"
                    :title="'取消'"
                    class="mr10"
                    @click="cancelGoodDialog"
                >
                    取消
                </bk-button>
            </div>
        </bk-dialog>
    </div>
</template>

<script>

    import {
        ADD_GOOD_URL, UPDATE_GOOD_URL, UPLOAD_IMG_URL, ADD_GOOD_TYPE_URL, DEL_PICS_URL
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
                // 物品添加/编辑dialog
                goodDialog: {
                    visiable: false,
                    typeIndex: 0,
                    typeList: ['新增', '编辑'],
                    headerPosition: 'center'
                },
                // 物品添加/编辑form
                goodFormData: {
                    good_code: '',
                    good_name: '',
                    good_type_id: '',
                    price: 0,
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
        },
        methods: {
            formGetGoodInfo (id) {
                this.$emit('getGoodInfo', id)
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
                        // 添加成功，重新初始化页面
                        this.getGoods()
                        // 清空dialog
                        this.goodFormData = {
                            good_code: '',
                            good_name: '',
                            good_type_id: '',
                            price: 0,
                            pics: [],
                            remark: '',
                            introduce: '',
                            specifications: ''
                        }
                        this.goodDialog.visiable = false
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
                formData.id = this.currentGoodId
                this.$http.post(UPDATE_GOOD_URL, formData).then(res => {
                    const config = {
                        'offsetY': 80,
                        'delay': 2000
                    }
                    if (res.result) {
                        config.theme = 'success'
                        config.message = '编辑物品信息成功'
                        this.$bkMessage(config)
                        // 编辑成功，重新初始化页面
                        this.getGoods()
                        this.goodDialog.visiable = false
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
                console.log('mdupload', files)
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
            submitAddGoodType () {
                this.addGoodType()
            },
            deleteImg (file, fileList) {
                this.goodFormData.pics = fileList
                const picUrl = file.url
                this.del_pics.push(picUrl.split('/')[picUrl.split('/').length - 2] + '\\' + picUrl.split('/')[picUrl.split('/').length - 1])
            },
            cancelGoodDialog () {
                this.goodDialog.visiable = false
                this.del_pics = []
            },
            submitAddOrUpdateGood () {
                // 校验表单
                this.$refs.checkForm.validate().then(validator => {
                    // 添加物品点击确认
                    if (this.goodDialog.typeIndex === 0) {
                        this.addGood()
                    } else {
                        // 编辑物品点击确认
                        this.updateGood()
                    }
                    const delForm = this.del_pics
                    if (this.del_pics.length !== 0) {
                        this.$http.post(DEL_PICS_URL, delForm).then(res => {

                        })
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
            clickAddGood () {
                this.$refs.checkForm.clearError()
                this.goodDialog.visiable = true
                // 如果刚才是编辑，去掉物品信息；同时避免上一次为新增时的物品信息被抹去
                if (this.goodDialog.typeIndex === 1) {
                    this.goodFormData = {
                        good_code: '',
                        good_name: '',
                        good_type_id: '',
                        price: 0,
                        pics: [],
                        remark: '',
                        introduce: '',
                        specifications: ''
                    }
                }
                // 选定为新增物品
                this.goodDialog.typeIndex = 0
            },
            clickEditGood (row) {
                this.$refs.checkForm.clearError()
                this.goodDialog.visiable = true
                // 选定为编辑物品
                this.goodDialog.typeIndex = 1
                // 获取物品信息
                this.formGetGoodInfo(row.id)
                this.currentGoodId = row.id
            }
        }
    }
</script>
<style lang="postcss" scoped>
    .good-dialog /deep/ .bk-dialog-wrapper .bk-dialog {
        width: 80% !important;
        top: 100px;
        .bk-dialog-content {
            width: 100% !important;
            left: 0 !important;
        }
    }
    .good-dialog /deep/ .bk-dialog-body {
        height: 600px;
        overflow: auto;
        .form-wrapper {
            display: flex;
            flex-wrap: wrap;
            .good-form {
                flex: 1;
                /* width: 40%; */
                margin-right: 20px;
                .bk-form-item
                    .bk-form-content
                    .bk-form-control
                    /deep/
                    .bk-input-text {
                    width: 100%;
                }
                .bk-form-item .bk-form-content .bk-form-control .group-box {
                    border-right: none;
                    .group-text {
                        padding: 0 4px;
                    }
                }
            }
            .remark-wrapper {
                display: flex;
                flex: 1;
                margin: 20px 0 0 0;
                span {
                    width: 40px;
                }
            }
        }
        .text-wrapper {
            display: flex;
            margin-top: 20px;
            span {
                width: 80px;
            }
        }
    }
    .form-wrapper {
        display: flex;
        flex-wrap: wrap;
        .good-form {
            flex: 1;
            /* width: 40%; */
            margin-right: 20px;
            .bk-form-item .bk-form-content .bk-form-control /deep/ .bk-input-text {
                width: 100%;
            }
            .bk-form-item .bk-form-content .bk-form-control .group-box {
                border-right: none;
                .group-text {
                    padding: 0 4px;
                }
            }
        }
        .remark-wrapper {
            display: flex;
            flex: 1;
            margin: 20px 0 0 0;
            span {
                width: 40px;
            }
        }
    }
    .text-wrapper {
        display: flex;
        margin-top: 20px;
        span {
            width: 80px;
        }
    }
</style>
