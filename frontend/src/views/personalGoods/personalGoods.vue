<template>
    <div class="personalGoods-wrapper">
        <div class="breadCrumb">
            <bk-breadcrumb>
                <bk-breadcrumb-item v-for="(item,index) in navList" :key="index" :to="item.link">{{item.title}}</bk-breadcrumb-item>
            </bk-breadcrumb>
        </div>
        <div class="conditions">
            <bk-form :label-width="200" form-type="vertical">
                <bk-container :col="12" :gutter="8">
                    <bk-row style="margin-bottom: 20px;">
                        <bk-col :span="6">
                            <div class="goodCode">
                                <bk-form-item label="物资编码">
                                    <bk-input v-model="formData.code" style="width: 90%"></bk-input>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="6">
                            <div class="goodName">
                                <bk-form-item label="物品名称">
                                    <bk-input v-model="formData.name" style="width: 90%"></bk-input>
                                </bk-form-item>
                            </div>
                        </bk-col>
                    </bk-row>
                    <bk-row style="margin-bottom: 10px;">
                        <bk-col :span="3">
                            <div class="goodTypes">
                                <bk-form-item label="物品类型">
                                    <bk-select :disabled="false" v-model="formData.type" style="width: 250px;width: 80%"
                                        ext-cls="select-custom"
                                        ext-popover-cls="select-popover-custom"
                                        searchable>
                                        <bk-option
                                            key="0"
                                            id="0"
                                            name="全部类型">
                                        </bk-option>
                                        <bk-option v-for="option in typeList"
                                            :key="option.id"
                                            :id="option.id"
                                            :name="option.type_name">
                                        </bk-option>
                                    </bk-select>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="3">
                            <div class="goodStatus">
                                <bk-form-item label="物品状态">
                                    <bk-select :disabled="false" v-model="formData.status" style="width: 80%"
                                        ext-cls="select-custom"
                                        ext-popover-cls="select-popover-custom"
                                        searchable>
                                        <bk-option
                                            key="0"
                                            id="0"
                                            name="全部状态">
                                        </bk-option>
                                        <bk-option v-for="option in statusList"
                                            :key="option.id"
                                            :id="option.id"
                                            :name="option.status_name">
                                        </bk-option>
                                    </bk-select>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="3">
                            <div class="goodLocation">
                                <bk-form-item label="物品地区">
                                    <bk-select :disabled="false" v-model="formData.location" style="width: 80%"
                                        ext-cls="select-custom"
                                        ext-popover-cls="select-popover-custom"
                                        searchable>
                                        <bk-option
                                            key="0"
                                            id="0"
                                            name="所有地区">
                                        </bk-option>
                                        <bk-option v-for="option in locationList"
                                            :key="option.id"
                                            :id="option.name"
                                            :name="option.name">
                                        </bk-option>
                                    </bk-select>
                                </bk-form-item>
                            </div>
                        </bk-col>
                    </bk-row>
                    <bk-row style="margin-bottom: 10px; text-align: right">
                        <bk-col :span="9">
                            <div class="search">
                                <bk-form-item class="mt20">
                                    <bk-button style="margin-right: 15px;" :theme="'primary'" title="查询" :outline="true" @click="search">查询</bk-button>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="1">
                            <div class="output">
                                <bk-form-item class="mt20">
                                    <bk-button :theme="'warning'" title="确认收货" :outline="true" style="margin-right: 40px;width: 90%;padding: 0" @click="confirmReceiptDialog">
                                        确认收货
                                    </bk-button>
                                    <bk-dialog v-model="confirmReceiptDialogVisible"
                                        theme="primary"
                                        width="600"
                                        :render-directive="'if'"
                                        :mask-close="false"
                                        :header-position="left"
                                        @confirm="confirmReceipt"
                                        :esc-close="false"
                                        title="">
                                        确认收货?
                                    </bk-dialog>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="1">
                            <div class="output">
                                <bk-form-item class="mt20">
                                    <bk-button :theme="'success'" title="导出数据" :outline="true" style="margin-right: 40px;width: 90%;padding: 0" @click="deriveExcel">
                                        导出数据
                                    </bk-button>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="1">
                            <div class="return">
                                <bk-form-item class="mt20">
                                    <bk-button :theme="'danger'" title="物资退库" :outline="true" style="margin-right: 40px;width: 90%;padding: 0" @click="returnGoods">
                                        物资退库
                                    </bk-button>
                                </bk-form-item>
                            </div>
                        </bk-col>
                    </bk-row>
                </bk-container>
            </bk-form>
        </div>
        <div class="options">
            
        </div>
        <div class="goods">
            <bk-table style="margin-top: 15px;"
                :data="data"
                :size="medium"
                :pagination="pagination"
                @select="selectRow"
                @select-all="selectAll"
                @row-mouse-enter="handleRowMouseEnter"
                @row-mouse-leave="handleRowMouseLeave"
                @page-change="handlePageChange"
                @page-limit-change="handlePageLimitChange">
                <bk-table-column type="selection" width="60"></bk-table-column>
                <bk-table-column label="物资编码" prop="good_code"></bk-table-column>
                <bk-table-column label="物品名称" prop="good_name"></bk-table-column>
                <bk-table-column label="所在地区" prop="position"></bk-table-column>
                <bk-table-column label="使用人" prop="username"></bk-table-column>
                <bk-table-column label="状态" prop="status"></bk-table-column>
            </bk-table>
        </div>
    </div>
</template>

<script>
    const getPersonalGoodsUrl = '/purchase/get_personal_goods/' // 获取个人物资接口
    const getTypesUrl = '/purchase/get_good_type_list' // 获取所有类型接口
    const getStatusUrl = '/purchase/get_good_status_list' // 获取所有物品状态接口
    const getPositionsUrl = '/apply/get_position_list' // 获取所有地区接口
    const deriveExcelUrl = '/purchase/derive_excel' // 生成excel文件并导出接口
    const delFilesUrl = '/purchase/del_excel' // 删除已生成的excel文件接口
    const confirmReceiptUrl = '/purchase/confirm_receipt'
    export default {
        data () {
            return {
                username: '',
                navList: [ // 面包屑列表
                    {
                        title: '个人物资查询', link: { name: 'personalGoods' }
                    }
                ],
                statusList: [], // 物资状态列表
                typeList: [], // 物资种类列表
                locationList: [], // 地点列表
                formData: { // 条件搜索表单数据
                    name: '',
                    code: '',
                    location: 0,
                    status: 0,
                    type: 0
                },
                data: [], // 表格数据
                pagination: { // 分页器数据
                    current: 1,
                    count: 50,
                    limit: 10
                },
                get_params: { // 用于提交请求的数据
                    form: {
                        name: '',
                        code: '',
                        location: '',
                        status: '',
                        type: ''
                    },
                    page: 1,
                    pageLimit: 10
                },
                selected: {
                    selectedRows: []
                }, // 存放被选中行数
                fileCache: [], // 存放待删除excel文件名以及文件夹名,
                confirmReceiptDialogVisible: false
            }
        },
        created () {
            this.username = this.$store.state.user.username // 从state中获取用户名
            this.loadData() // 向后台请求数据
            if (this.$route.params.isFromReturnGoods) { // 判断是否来自退库的跳转
                this.handleError({ theme: 'warning' }, '无在使用商品, 已自动跳转回个人物资查询页')
            }
        },
        methods: {
            loadData () { // 渲染时请求数据
                this.getPersonalGoods()
                this.getTypes()
                this.getStatus()
                this.getPosition()
            },
            sleep (time) { // 定时器
                return new Promise((resolve) => setTimeout(resolve, time * 1000))
            },
            confirmReceiptDialog () {
                if (this.selected.selectedRows.length === 0) {
                    this.handleError({ theme: 'warning' }, '未选择任何数据')
                    return
                }
                this.confirmReceiptDialogVisible = true
            },
            confirmReceipt () {
                this.$http.post(confirmReceiptUrl, { idList: this.selected.selectedRows }).then(res => {
                    if (res && res.result === true) {
                        this.handleError({ theme: 'success' }, res.message)
                        this.selected.selectedRows = []
                        this.pagination.current = 1
                        this.get_params.page = this.pagination.current
                        this.getPersonalGoods()
                    } else if (res && res.result === false) {
                        this.handleError({ theme: 'error' }, '状态为非待收货的物品不可确认收货')
                    }
                })
            },
            returnGoods () { // 物资退库
                if (this.selected.selectedRows.length === 0) {
                    this.handleError({ theme: 'warning' }, '未选择任何数据')
                    return
                }
                this.$router.push({
                    name: 'returnGoods',
                    params: {
                        idList: this.selected,
                        isFromPersonalGoods: true
                    }
                })
            },
            deriveExcel () { // 导出excel表
                if (this.selected.selectedRows.length === 0) {
                    this.handleError({ theme: 'warning' }, '未选择任何数据')
                    return
                }
                try {
                    this.$http.post(deriveExcelUrl, { model: 1, dataList: this.selected }).then(res => {
                        if (res && res.result === true) {
                            const link = document.createElement('a') // 生成a元素，用以实现下载功能
                            link.href = res.data.file_url
                            document.body.appendChild(link)
                            link.click()
                            document.body.removeChild(link)
                            const fileName = res.data.file_url.split('/').slice(-1)[0] // 获取文件名
                            const dirName = res.data.file_url.split('/').slice(-2, -1)[0] // 获取文件夹名
                            this.fileCache.push([fileName, dirName])
                            this.sleep(30 * 60).then(() => { // 半小时后删除excel文件
                                this.$http.post(delFilesUrl, { dirName: this.fileCache[0][1], fileName: this.fileCache[0][0] }).then(() => {
                                    this.fileCache.shift()
                                })
                            })
                        } else if (res && res.result === false) {
                            this.handleError({ theme: 'error' }, res.message)
                        }
                    })
                } catch (e) {
                    console.log('catch错误：', e)
                }
            },
            
            getPersonalGoods () { // 获得个人物资
                this.$http.get(getPersonalGoodsUrl, {
                    params: {
                        form: this.get_params.form,
                        page: this.get_params.page,
                        pageLimit: this.get_params.pageLimit
                    }
                }).then(res => {
                    if (res && res.result === true) {
                        this.pagination.count = res.data[res.data.length - 1].total
                        res.data.pop()
                        this.data = res.data
                    } else if (res && res.result === false) {
                        this.handleError({ theme: 'error' }, res.message)
                    }
                }).catch(err => {
                    console.log('错误为：', err)
                })
            },
            getTypes () { // 获得物品类型
                this.$http.get(getTypesUrl).then(res => {
                    if (res) {
                        if (res && res.result === true) {
                            this.typeList = res.data
                        } else if (res && res.result === false) {
                            this.handleError({ theme: 'error' }, res.message)
                        }
                    }
                })
            },
            getStatus () { // 获得物资状态
                this.$http.get(getStatusUrl).then(res => {
                    if (res) {
                        if (res && res.result === true) {
                            this.statusList = res.data
                        } else if (res && res.result === false) {
                            this.handleError({ theme: 'error' }, res.message)
                        }
                    }
                })
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
            selectRow (selection, row) { // 选择单行时触发函数
                const idx = this.selected.selectedRows.indexOf(row.id)
                if (idx !== -1) {
                    this.selected.selectedRows.splice(idx, 1)
                } else {
                    this.selected.selectedRows.push(row.id)
                }
            },
            selectAll () { // 全选时触发函数
                if (this.selected.selectedRows.length !== 0 && this.selected.selectedRows.length !== this.pagination.limit) {
                    this.selected.selectedRows = []
                    for (let index = 0; index < this.data.length; index++) {
                        this.selected.selectedRows.push(this.data[index].id)
                    }
                } else if (this.selected.selectedRows.length !== 0 && this.selected.selectedRows.length === this.pagination.limit) {
                    this.selected.selectedRows = []
                } else if (this.selected.selectedRows.length === 0) {
                    for (let index = 0; index < this.data.length; index++) {
                        this.selected.selectedRows.push(this.data[index].id)
                    }
                }
            },
            handleError (config, message) { // 遇到后台报自定义错误时上方弹窗提醒
                config.message = message
                config.offsetY = 80
                this.$bkMessage(config)
            },
            search () { // 条件搜索触发函数
                this.get_params.username = this.username
                const form = JSON.stringify(this.formData)
                this.get_params.form = JSON.parse(form)
                // this.get_params.form = this.formData
                this.pagination.current = 1
                this.get_params.page = this.pagination.current
                this.getPersonalGoods()
                this.selected.selectedRows = []
            },
            handlePageLimitChange () { // 修改每页多少条数据触发函数
                this.pagination.limit = arguments[0]
                this.get_params.pageLimit = this.pagination.limit
                this.pagination.current = 1
                this.get_params.page = this.pagination.current
                this.selectedRows = []
                this.getPersonalGoods()
            },
            handlePageChange (page) { // 修改当前页触发函数
                this.pagination.current = page
                this.get_params.page = this.pagination.current
                this.getPersonalGoods()
            }
        }
    }

</script>

<style lang="postcss" scoped>
.personalGoods-wrapper{
    .breadCrumb{
        margin: 15px 20px;
    }
    .conditions{
        width: 100%;
    }
    .goods{
        margin: 20px 10px;
    }
}
</style>
