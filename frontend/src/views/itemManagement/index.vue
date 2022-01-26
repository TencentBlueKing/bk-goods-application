<template>
    <div class="itemManagement-wrapper">
        <div class="title-wapper">
            <bk-breadcrumb>
                <bk-breadcrumb-item :key="1" :to="itemManagement">物品管理</bk-breadcrumb-item>
            </bk-breadcrumb>
        </div>
        <div class="header-wrapper">
            <div class="fun-bar">
                <span>物品编号：</span>
                <bk-input :clearable="true" v-model="unSubmitSearch.goodCode"></bk-input>
            </div>
            <div class="fun-bar">
                <span>物品名称：</span>
                <bk-input :clearable="true" v-model="unSubmitSearch.goodName"></bk-input>
            </div>
            <div class="fun-bar">
                <span style="width:72px;">物品类别：</span>
                <bk-select :disabled="false" v-model="unSubmitSearch.goodTypeId" style="width:200px;"
                    searchable
                >
                    <bk-option
                        :key="0"
                        :id="0"
                        :name="'全部'">
                    </bk-option>
                    <bk-option v-for="goodType in goodTypeList"
                        :key="goodType.id"
                        :id="goodType.id"
                        :name="goodType.type_name">
                    </bk-option>
                </bk-select>
            </div>

            <bk-button :theme="'primary'" :title="'搜索按钮'" class="mr10 search-btn" @click="searchGoodsInfo">
                搜索
            </bk-button>
            <bk-button :theme="'primary'" :title="'添加按钮'" class="mr10 add-btn" @click="clickAddGood">
                添加
            </bk-button>
        </div>
        <bk-dialog v-model="goodDialog.visiable"
            theme="primary"
            :header-position="goodDialog.headerPosition"
            :z-index="1100"
            :title="goodDialog.typeList[goodDialog.typeIndex] + '物品'"
            class="good-dialog"
        >
            <div class="form-wrapper">
                <bk-form :model="goodFormData" :rules="rules" :ext-cls="'good-form'" ref="checkForm">
                    <bk-form-item :label-width="80" label="物品编码" :required="true" :property="'good_code'">
                        <bk-input v-model="goodFormData.good_code" placeholder="请输入1到30个以内的字符"></bk-input>
                    </bk-form-item>
                    <bk-form-item :label-width="80" label="物品名称" :required="true" :property="'good_name'">
                        <bk-input v-model="goodFormData.good_name" placeholder="请输入物品名称（50字以内）"></bk-input>
                    </bk-form-item>
                    <bk-form-item :label-width="80" label="物品类型" :required="true" :property="'good_type_id'">
                        <bk-select :disabled="false" v-model="goodFormData.good_type_id"
                            searchable
                        >
                            <bk-option v-for="goodType in goodTypeList"
                                :key="goodType.id"
                                :id="goodType.id"
                                :name="goodType.type_name">
                            </bk-option>
                            <div slot="extension" @click="addGoodTypeDialog.visiable = true" style="cursor: pointer;">
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
                            <span>类型名称：</span>
                            <bk-input :clearable="true" v-model="addGoodTypeDialog.typeName"></bk-input>
                        </div>
                        <div slot="footer">
                            <bk-button :theme="'primary'" :title="'确认'" class="mr10" @click="submitAddGoodType">
                                确认
                            </bk-button>
                            <bk-button :theme="'default'" :title="'取消'" class="mr10" @click="addGoodTypeDialog.visiable = false">
                                取消
                            </bk-button>
                        </div>
                    </bk-dialog>
                    <bk-form-item :label-width="80" label="参考价" ext-cls="price-wrapper" :required="true" :property="'price'">
                        <bk-input type="number" precision="2" v-model="goodFormData.price" title="保留两位小数">
                            <template slot="prepend">
                                <div class="group-text">
                                    <span v-bk-tooltips="toolTips.top" class="top-start">
                                        <i class="bk-icon icon-info-circle-shape"></i>
                                    </span>
                                </div>
                            </template>
                        </bk-input>
                    </bk-form-item>
                    <bk-form-item :label-width="80" label="参考图" ext-cls="pics-wrapper" :required="true" :property="'pics'">
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
                </bk-form>
                <div class="remark-wrapper">
                    <span>备注</span>
                    <bk-input type="textarea" v-model="goodFormData.remark" placeholder="请输入物品备注"></bk-input>
                </div>
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
                <bk-button :theme="'primary'" :title="'确认'" class="mr10" @click="submitAddOrUpdateGood">
                    确认
                </bk-button>
                <bk-button :theme="'default'" :title="'取消'" class="mr10" @click="cancelGoodDialog">
                    取消
                </bk-button>
            </div>
        </bk-dialog>
        <div class="goods-info-load" v-bkloading="{ isLoading: isGoodsInfoLoad, theme: 'primary', zIndex: 10 }"></div>
        <div class="goods-info-table">
            <bk-table v-show="!isGoodsInfoLoad" v-if="getGoodsFlag" style="margin-top: 20px;"
                max-height="400"
                :data="goodsInfo.goodList"
                :pagination="goodsInfo.pagination"
                :is-loading="isGoodsInfoLoad"
                @row-mouse-enter="handleRowMouseEnter"
                @row-mouse-leave="handleRowMouseLeave"
                @page-change="handlePageChange"
                @page-limit-change="handlePageLimitChange">
                <bk-table-column type="index" label="序列" width="60"></bk-table-column>
                <bk-table-column label="物品编号" prop="good_code"></bk-table-column>
                <bk-table-column label="物品名称" prop="good_name"></bk-table-column>
                <bk-table-column label="物品类型" prop="good_tye_name"></bk-table-column>
                <bk-table-column label="参考价" prop="price"></bk-table-column>
                <bk-table-column label="操作" width="150">
                    <template slot-scope="props">
                        <bk-button class="mr10" theme="primary" text :disabled="props.row.status === '创建中'" @click="clickEditGood(props.row)">编辑</bk-button>
                        <bk-button class="mr10" theme="primary" text @click="clickDownGood(props.row)">下架</bk-button>
                    </template>
                </bk-table-column>
            </bk-table>
        </div>
    </div>
</template>

<script>
    const delPicsUrl = '/purchase/del_pics'
    export default {
        components: {},
        data () {
            return {
                unSubmitSearch: {
                    goodCode: '',
                    goodName: '',
                    goodTypeId: 0
                },
                submitSearchInput: {
                    goodCode: '',
                    goodName: '',
                    goodTypeId: 0
                },
                addGoodTypeDialog: {
                    visiable: false,
                    typeName: ''
                },
                isGoodsInfoLoad: true,
                goodsInfo: {
                    totalNum: 0,
                    goodList: [],
                    pagination: {
                        current: 1,
                        count: 500,
                        limit: 20
                    }
                },
                // 物品类型信息
                getGoodsFlag: true,
                goodTypeList: [],
                isGoodTypesLoad: true,
                // 物品添加/编辑dialog
                goodDialog: {
                    visiable: false,
                    typeIndex: 0,
                    typeList: ['新增', '编辑'],
                    headerPosition: 'center'
                },
                currentGoodId: 0,
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
                    } },
                picsLimit: 6,
                goodsCodeList: [],
                del_pics: []
            }
        },
        created () {
            this.getGoods()
            this.getGoodTypes()
            this.getGoodCodeList()
        },
        methods: {

            // 后端请求函数
            getGoods () {
                this.isGoodsInfoLoad = true
                this.$http.get('/purchase/get_good_list'
                    + '?good_code=' + this.submitSearchInput.goodCode
                    + '&good_name=' + this.submitSearchInput.goodName
                    + '&good_type_id=' + this.submitSearchInput.goodTypeId
                    + '&page=' + this.goodsInfo.pagination.current
                    + '&size=' + this.goodsInfo.pagination.limit
                ).then(res => {
                    if (res.result) {
                        this.getGoodsFlag = false
                        this.goodsInfo.totalNum = res.data.total_num
                        this.goodsInfo.goodList = res.data.good_list
                        this.goodsInfo.pagination.count = res.data.total_num
                    } else {
                        this.$bkMessage({
                            'offsetY': 80,
                            'delay': 2000,
                            'theme': 'error',
                            'message': res.message
                        })
                    }
                }).finally(() => {
                    this.getGoodsFlag = true
                    this.isGoodsInfoLoad = false
                })
            },
            getGoodTypes () {
                this.isGoodTypesLoad = true
                this.$http.get('/purchase/get_good_type_list').then(res => {
                    if (res.result) {
                        this.goodTypeList = res.data
                    }
                }).finally(() => {
                    this.isGoodTypesLoad = false
                })
            },
            getGoodCodeList () {
                this.$http.get('/purchase/get_good_code_list').then(res => {
                    if (res.result) {
                        res.data.forEach((item, index) => {
                            this.goodsCodeList.push({
                                id: index,
                                name: item
                            })
                        })
                    }
                }).catch(() => {
                    this.$$bkMessage({
                        message: 'get_good_code_list接口报错',
                        theme: 'error'
                    })
                })
            },
            searchCodeSelect (value, option) {
                this.unSubmitSearch.goodCode = this.goodsCodeList[value].name
                console.log('this.unSubmitSearch.goodCode == ', this.unSubmitSearch.goodCode)
            },
            getGoodInfo (goodId) {
                this.$http.get('/purchase/get_good_detail?good_id=' + goodId).then(res => {
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
                this.$http.post('/purchase/add_good', formData).then(res => {
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
                this.$http.post('/purchase/update_good', formData).then(res => {
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
            // 下架物品
            downGood (goodId) {
                this.$http.get('/purchase/down_good?id=' + goodId).then(res => {
                    const config = {
                        'offsetY': 80,
                        'delay': 2000
                    }
                    if (res.result) {
                        config.theme = 'success'
                        config.message = '下架物品成功'
                        this.$bkMessage(config)
                        // 下架成功，重新初始化页面
                        this.getGoods()
                    } else {
                        // 可以省略，没有错误信息
                        console.log(res.message)
                        // config.theme = 'error'
                        // config.message = res.message
                        // this.$bkMessage(config)
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
                    this.$http.post('/purchase/upload_img', { img: fileData, img_type: fileType }).then(res => {
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
                        this.$http.post('/purchase/upload_img', { img: fileData, img_type: fileType }).then(res => {
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
                this.$http.post('/purchase/add_good_type', { type_name: this.addGoodTypeDialog.typeName }).then(res => {
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
            // 操作事件
            searchGoodsInfo () {
                this.submitSearchInput.goodCode = this.unSubmitSearch.goodCode
                this.submitSearchInput.goodName = this.unSubmitSearch.goodName
                this.submitSearchInput.goodTypeId = this.unSubmitSearch.goodTypeId
                this.getGoods()
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
                this.getGoodInfo(row.id)
                this.currentGoodId = row.id
            },
            clickDownGood (row) {
                this.$bkInfo({
                    title: '确认下架物品',
                    subTitle: row.good_code + '（' + row.good_name + '）',
                    showFooter: true,
                    extCls: 'down-good-dialog',
                    confirmFn: () => {
                        this.downGood(row.id)
                    }
                })
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
                        this.$http.post(delPicsUrl, delForm).then(res => {

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
            handlePageLimitChange () {
                // 点击切换选择数据条数
                this.goodsInfo.pagination.limit = arguments[0]
                // console.log('handlePageLimitChange', arguments)
                this.getGoods()
            },
            toggleTableSize () {
                const size = ['small', 'medium', 'large']
                const index = (size.indexOf(this.size) + 1) % 3
                this.size = size[index]
            },
            handlePageChange (page) {
                // 点击切换页数
                this.goodsInfo.pagination.current = page
                this.getGoods()
            }
        }
    }
</script>

<style scoped lang="postcss">
@import './index.css';
.title-wapper{
    margin-top: 10px;
}
.header-wrapper {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    margin-top: 10px;
    .fun-bar {
        display: flex;
        align-items: center;
        margin-right: 20px;
        span {
            width: 100px;
        }
    }
}
.add-type-wrapper {
    display: flex;
    align-items: center;
    span {
        width: 100px;
    }
}
.goods-info-table /deep/ .bk-table .bk-table-header-wrapper .bk-table-header {
    width: 100% !important;
}
.goods-info-table /deep/ .bk-table .bk-table-body-wrapper .bk-table-body {
    width: 100% !important;
}
.goods-info-table /deep/ .bk-table .bk-table-body-wrapper .bk-table-empty-block {
    width: 100% !important;
}

.good-dialog /deep/ .bk-dialog-wrapper .bk-dialog{
    width: 80% !important;
    top: 100px;
    .bk-dialog-content{
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
        .good-form{
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

.pic-wrapper {
    display: flex;
    margin-top: 20px;
    span {
        margin-right: 24px;
        width: 56px;
        text-align: right;
    }
}

</style>
