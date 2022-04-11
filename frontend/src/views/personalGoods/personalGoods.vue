<template>
    <div class="personalGoods-wrapper">
        <div class="conditions">
            <bk-form
                :label-width="200"
                form-type="vertical"
                style="width:80%"
            >
                <bk-container
                    :col="12"
                    :gutter="4"
                >
                    <bk-row style="margin-bottom: 10px">
                        <bk-col :span="4">
                            <div class="goodCode">
                                <bk-form-item label="物资编码">
                                    <bk-input
                                        v-model="formData.code"
                                        style="width: 70%"
                                    ></bk-input>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="4">
                            <div class="goodName">
                                <bk-form-item label="物品名称">
                                    <bk-input
                                        v-model="formData.name"
                                        style="width: 70%"
                                    ></bk-input>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="4">
                            <div class="goodLocation">
                                <bk-form-item label="省级地区">
                                    <bk-select
                                        :disabled="false"
                                        v-model="formData.province"
                                        style="width: 70%"
                                        ext-cls="select-custom"
                                        ext-popover-cls="select-popover-custom"
                                        searchable
                                    >
                                        <bk-option
                                            key="0"
                                            id="0"
                                            name="所有地区"
                                        >
                                        </bk-option>
                                        <bk-option
                                            v-for="option in provinceList"
                                            :key="option.name"
                                            :id="option.id"
                                            :name="option.name"
                                        >
                                        </bk-option>
                                    </bk-select>
                                </bk-form-item>
                            </div>
                        </bk-col>
                    </bk-row>
                    <bk-row style="margin-bottom: 10px">
                        <bk-col :span="4">
                            <div class="goodTypes">
                                <bk-form-item label="物品类型">
                                    <bk-select
                                        :disabled="false"
                                        v-model="formData.type"
                                        style="width: 250px; width: 70%"
                                        ext-cls="select-custom"
                                        ext-popover-cls="select-popover-custom"
                                        searchable
                                    >
                                        <bk-option
                                            key="0"
                                            id="0"
                                            name="全部类型"
                                        >
                                        </bk-option>
                                        <bk-option
                                            v-for="option in typeList"
                                            :key="option.id"
                                            :id="option.id"
                                            :name="option.type_name"
                                        >
                                        </bk-option>
                                    </bk-select>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="4">
                            <div class="goodStatus">
                                <bk-form-item label="物品状态">
                                    <bk-select
                                        :disabled="false"
                                        v-model="formData.status"
                                        style="width: 70%"
                                        ext-cls="select-custom"
                                        ext-popover-cls="select-popover-custom"
                                        searchable
                                    >
                                        <bk-option
                                            key="0"
                                            id="0"
                                            name="全部状态"
                                        >
                                        </bk-option>
                                        <bk-option
                                            v-for="option in statusList"
                                            :key="option.id"
                                            :id="option.id"
                                            :name="option.status_name"
                                        >
                                        </bk-option>
                                    </bk-select>
                                </bk-form-item>
                            </div>
                        </bk-col>
                        <bk-col :span="4">
                            <div class="goodLocation">
                                <bk-form-item label="市级地区">
                                    <bk-select
                                        :disabled="false"
                                        v-model="formData.city"
                                        style="width: 70%"
                                        ext-cls="select-custom"
                                        ext-popover-cls="select-popover-custom"
                                        searchable
                                    >
                                        <bk-option
                                            key="0"
                                            id="0"
                                            name="所有地区"
                                        >
                                        </bk-option>
                                        <bk-option
                                            v-for="option in cityList"
                                            :key="option.id"
                                            :id="option.name"
                                            :name="option.name"
                                        >
                                        </bk-option>
                                    </bk-select>
                                </bk-form-item>
                            </div>
                        </bk-col>
                    </bk-row>
                </bk-container>
            </bk-form>
            <div class="search">
                <bk-button
                    :theme="'primary'"
                    title="查询"
                    @click="search"
                    size="medium"
                >查询数据</bk-button>
            </div>
        </div>
        <div class="more-options">
            <el-tabs>
                <el-tab-pane>
                    <span
                        slot="label"
                        class="tab-label"
                    >
                        <el-dropdown
                            @command="handleCommand"
                            style="margin-top: -3px"
                        >
                            <span class="el-dropdown-link">
                                批量操作<i class="el-icon-arrow-down el-icon--right"></i>
                            </span>
                            <el-dropdown-menu slot="dropdown">
                                <el-dropdown-item command="derive">导出数据</el-dropdown-item>
                                <el-dropdown-item command="confirm">确认收货</el-dropdown-item>
                                <el-dropdown-item command="return">物资退库</el-dropdown-item>
                            </el-dropdown-menu>
                        </el-dropdown>
                        <div style="height: 5px; background: blue; width: 60px; margin-top:-8px; ; border-radius: 6px"></div>
                    </span>
                    <div class="goods">
                        <bk-table
                            style="margin-top: 15px"
                            :height="300"
                            :data="data"
                            :size="medium"
                            :pagination="pagination"
                            @select="selectRow"
                            @select-all="selectAll"
                            @row-mouse-enter="handleRowMouseEnter"
                            @row-mouse-leave="handleRowMouseLeave"
                            @page-change="handlePageChange"
                            @page-limit-change="handlePageLimitChange"
                            :header-cell-style="{ background: '#fff' }"
                        >
                            <bk-table-column
                                type="selection"
                                width="60"
                            ></bk-table-column>
                            <bk-table-column
                                label="物资编码"
                                prop="good_code"
                            ></bk-table-column>
                            <bk-table-column
                                label="物品名称"
                                prop="good_name"
                            ></bk-table-column>
                            <bk-table-column
                                label="所在地区"
                                prop="position"
                            ></bk-table-column>
                            <bk-table-column
                                label="使用人"
                                prop="username"
                            ></bk-table-column>
                            <bk-table-column label="状态">
                                <template slot-scope="props">
                                    <bk-tag ext-cls="custom-tag">{{props.row.status}}</bk-tag>
                                </template>
                            </bk-table-column>
                        </bk-table>
                    </div>
                </el-tab-pane>
            </el-tabs>
        </div>
        <bk-dialog
            v-model="confirmReceiptDialogVisible"
            theme="primary"
            width="600"
            :render-directive="'if'"
            :mask-close="false"
            :header-position="left"
            @confirm="confirmReceipt"
            :esc-close="false"
            title=""
        >
            确认收货?
        </bk-dialog>
    </div>
</template>

<script>
    import {
        GET_GOOD_TYPE_LIST_URL, GET_ROOT_POSITION_LIST_URL, GET_SUB_POSITION_LIST_URL, DERIVE_EXCEL_URL, CONFIRM_RECEIPT_URL,
        DEL_EXCEL_URL, GET_PERSONAL_GOODS_URL, GET_GOOD_STATUS_LIST_URL
    } from '@/pattern'
    export default {
        data () {
            return {
                username: '',
                // navList: [ // 面包屑列表
                //     {
                //         title: '个人物资查询', link: { name: 'personalGoods' }
                //     }
                // ],
                statusList: [], // 物资状态列表
                typeList: [], // 物资种类列表
                provinceList: [], // 一级地点列表
                cityList: [], // 二级地点列表
                formData: { // 条件搜索表单数据
                    name: '',
                    code: '',
                    province: 0,
                    city: 0,
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
                        province: '',
                        city: '',
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
                confirmReceiptDialogVisible: false,
                isDropdownShow: false
            }
        },
        watch: {
            'formData.province': function (val) { // 监听单个导入时的页面表格的校区变量
                this.cityList = []
                this.formData.city = 0
                if (val === 0 || val === '0') {
                    return
                }
                const parentCode = this.getParentCode(val)
                this.$http.get(GET_SUB_POSITION_LIST_URL, {
                    params: {
                        parent_code: parentCode,
                        org_id: 1
                    }
                }).then(res => {
                    console.log(res)
                    this.cityList = res.data
                })
            }
        },
        created () {
            this.username = this.$store.state.user.username // 从state中获取用户名
            this.loadData() // 向后台请求数据
            if (this.$route.params.isFromReturnGoods) { // 判断是否来自退库的跳转
                this.handleError({ theme: 'warning' }, '无在使用商品, 已自动跳转回个人物资查询页')
            }
        },
        mounted () {
            this.$store.commit('updateViewInfo', '个人物资查询')
        },
        methods: {
            loadData () { // 渲染时请求数据
                this.getPersonalGoods()
                this.getTypes()
                this.getStatus()
                this.getPosition()
            },
            getParentCode (val) { // 获取父级地区的编码
                console.log('val', val)
                let parentCode = ''
                for (let index = 0; index < this.provinceList.length; index++) {
                    if (this.provinceList[index].id === val) {
                        parentCode = this.provinceList[index].code
                        break
                    }
                }
                return parentCode
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
                this.$http.post(CONFIRM_RECEIPT_URL, { idList: this.selected.selectedRows, org_id: 1 }).then(res => {
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
                const query = { idList: JSON.stringify(this.selected) }
                this.$router.push({
                    name: 'returnGoods',
                    query: query
                })
            },
            deriveExcel () { // 导出excel表
                if (this.selected.selectedRows.length === 0) {
                    this.handleError({ theme: 'warning' }, '未选择任何数据')
                    return
                }
                try {
                    this.$http.post(DERIVE_EXCEL_URL, { model: 1, dataList: this.selected, org_id: 1 }).then(res => {
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
                                this.$http.post(DEL_EXCEL_URL, { dirName: this.fileCache[0][1], fileName: this.fileCache[0][0] }).then(() => {
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
                this.$http.get(GET_PERSONAL_GOODS_URL, {
                    params: {
                        ...this.get_params.form,
                        org_id: 1,
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
                    console.error('错误为：', err)
                })
            },
            getTypes () { // 获得物品类型
                this.$http.get(GET_GOOD_TYPE_LIST_URL, {
                    params: {
                        org_id: 1
                    }
                }).then(res => {
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
                this.$http.get(GET_GOOD_STATUS_LIST_URL).then(res => {
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
                this.$http.get(GET_ROOT_POSITION_LIST_URL, {
                    params: {
                        org_id: 1
                    }
                }).then(res => {
                    if (res) {
                        if (res && res.result === true) {
                            this.provinceList = res.data
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
            search () {
                // 条件搜索触发函数
                this.get_params.username = this.username
                const form = JSON.stringify(this.formData)
                this.get_params.form = JSON.parse(form)
                this.pagination.current = 1
                this.get_params.page = this.pagination.current
                this.getPersonalGoods()
                this.selected.selectedRows = []
            },
            handlePageLimitChange () {
                // 修改每页多少条数据触发函数
                this.pagination.limit = arguments[0]
                this.get_params.pageLimit = this.pagination.limit
                this.pagination.current = 1
                this.get_params.page = this.pagination.current
                this.selectedRows = []
                this.getPersonalGoods()
            },
            handlePageChange (page) {
                // 修改当前页触发函数
                this.pagination.current = page
                this.get_params.page = this.pagination.current
                this.getPersonalGoods()
            },
            refresh () {
                this.$router.go(0)
            },
            handleCommand (command) {
                if (command === 'derive') {
                    this.deriveExcel()
                } else if (command === 'confirm') {
                    this.confirmReceiptDialog()
                } else if (command === 'return') {
                    this.returnGoods()
                }
            }
        }
    }

</script>

<style lang="postcss" scoped>
    .personalGoods-wrapper {
        overflow: hidden;
        padding: 20px;
        .header {
            display: block;
        }
        .conditions {
            width: 100%;
            display: flex;
            .search {
                display: flex;
                justify-content: center;
                align-items: center;
            }
        }
        .more-options {
            text-align: right;
        }
        .goods {
            margin-top: 10px;
        }
    }
    /deep/.bk-table-enable-row-transition .bk-table-body td {
        border: none !important;
    }
    /deep/.bk-table {
        border: none !important;
        &:before {
            height: 0px !important;
        }
    }
    /deep/.bk-table-outer-border:after {
        width: 0px !important;
    }
    /deep/.bk-table-pagination-wrapper {
        border: none !important;
    }
    /deep/.el-tabs__nav {
        float: right;
    }
    /deep/.el-tabs__item {
        width: 120px;
        height: 50px;
        display: flex;
        flex-direction: column;
        place-content: center;
        place-items: center;
        border: #409eff solid 2px;
        border-radius: 8px;
    }
    /deep/.el-tabs__active-bar {
        display: none;
    }
    /deep/.el-tabs__nav-wrap::after {
        background-color: #409eff;
    }
    .custom-tag {
        color: #409EFF;
    }
</style>
