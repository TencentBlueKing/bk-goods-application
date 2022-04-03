<template>
    <div class="home-container">
        <div class="home-title">
            <h1>物资申请系统, 快速办理物资手续</h1>
            <span class="desc">使团队在云端就可完成物资的申请，管理与采购。</span>
        </div>
        <div class="home-content">
            <div class="carousel-control">
                <el-collapse
                    accordion
                    style="width: 100%"
                    v-model="collapselItem"
                    @change="changeCollapse"
                    ref="collapse"
                >
                    <el-collapse-item name="apply">
                        <template slot="title">
                            <h2>物资申请</h2>
                            <el-button
                                type="text"
                                @click="$router.push({ name: 'applyHome' })"
                                v-if="collapselItem === 'apply'"
                            >
                                <h3>查看更多></h3>
                            </el-button>
                        </template>
                        <div>可对单个物资进行申请<br>也可批量对物资申请操作，简便快捷</div>
                    </el-collapse-item>
                    <el-collapse-item
                        name="manage"
                        v-if="userInfo.isScretary"
                    >
                        <template slot="title">
                            <h2>申请管理</h2>
                            <el-button
                                type="text"
                                @click="$router.push({ name: 'applyManagement' })"
                                v-if="collapselItem === 'manage'"
                            >
                                <h3>查看更多></h3>
                            </el-button>
                        </template>
                        <div>对物资申请进行审核<br>查看物资申请进度，方便获取进度状态</div>
                    </el-collapse-item>
                    <el-collapse-item name="history">
                        <template slot="title">
                            <h2>历史记录</h2>
                            <el-button
                                type="text"
                                @click="$router.push({ name: 'applyHistory' })"
                                v-if="collapselItem === 'history'"
                            >
                                <h3>查看更多></h3>
                            </el-button>
                        </template>
                        <div>物资申请历史查看<br>编辑物资申请记录，批量简易修改</div>
                    </el-collapse-item>
                </el-collapse>
            </div>
            <div class="carousel-content">
                <el-carousel
                    direction="vertical"
                    :autoplay="false"
                    height="500px"
                    ref="carousel"
                >
                    <el-carousel-item name="apply">
                        <img
                            src="@/images/apply.png"
                            class="carousel-img"
                        >
                    </el-carousel-item>
                    <el-carousel-item name="manage">
                        <img
                            src="@/images/manage.png"
                            class="carousel-img"
                        >
                    </el-carousel-item>
                    <el-carousel-item name="history">
                        <img
                            src="@/images/history.png"
                            class="carousel-img"
                        >
                    </el-carousel-item>
                </el-carousel>
            </div>
        </div>
        <div class="footer">
            Copyright © 2012-{{new Date().getFullYear()}} Tencent BlueKing. All Rights Reserved. 腾讯蓝鲸 版权所有
        </div>
    </div>
</template>

<script>
    import { mapState } from 'vuex'
    export default {
        data () {
            return {
                collapselItem: 'apply'
            }
        },
        computed: {
            ...mapState({
                userInfo: state => state.user.userInfo
            })
        },
        methods: {
            changeCollapse (val) {
                this.$refs.carousel.setActiveItem(val)
            }
        }
    }
</script>

<style lang="postcss" scoped>
    .home-container {
        width: 100vw;
        height: 100vh;
        display: flex;
        flex-direction: column;
        place-items: center;
        .home-title {
            color: #202d40;
            font-size: 18px;
            height: 150px;
            display: flex;
            flex-direction: column;
            place-items: center;
            .desc {
                color: #606c80;
                font-family: PingFangSC-Regular;
                font-size: 16px;
                font-weight: normal;
                line-height: 24px;
            }
        }
        .home-content {
            width: 90%;
            height: calc(100% - 234px);
            display: flex;
            .carousel-control {
                width: 20%;
                height: 500px;
            }
            .carousel-content {
                width: 80%;
                height: 500px;
                .carousel-img {
                    max-width: 100%;
                    max-height: 100%;
                }
            }
        }
        .footer {
            height: 52px;
            width: 100%;
            margin: 32px 0 0;
            display: -webkit-box;
            display: -ms-flexbox;
            display: flex;
            -webkit-box-align: center;
            -ms-flex-align: center;
            align-items: center;
            -webkit-box-pack: center;
            -ms-flex-pack: center;
            justify-content: center;
            border-top: 1px solid #dcdee5;
            color: #63656e;
            font-size: 12px;
        }
    }
    /deep/.el-collapse-item__header {
        height: 80px;
        justify-content: space-between;
        padding-right: 10px;
    }
    /deep/.el-collapse-item__arrow {
        display: none;
    }
    /deep/.el-collapse-item__content {
        padding-bottom: 25px;
        font-size: 14px;
        color: #606c80;
    }
</style>
