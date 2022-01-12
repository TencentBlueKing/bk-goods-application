<template>
    <div class="itemDetail-wrapper">
        <div class="good-info-wapper">
            <div class="good-pic">
                <div class="main-pic">
                    <bk-zoom-image :src="myimage" class="zoom-image"></bk-zoom-image>
                </div>
                <div class="pic-list">
                    <div class="pic-slide-btn pic-slide-left">
                        <bk-icon type="arrows-m-left-shape" />
                    </div>
                    <div class="pic-item-wapper">
                        <img src="../../images/403.png" alt="" v-for="index in [1,1,1,1,1,1,1,1,1,1,1]" :key="index">
                    </div>
                    
                    <div class="pic-slide-btn pic-slide-right">
                        <bk-icon type="arrows-m-right-shape" />
                    </div>
                </div>
            </div>
            <div class="good-text">

            </div>
        </div>
        <div class="good-detail-wapper">

        </div>
    </div>
</template>

<script>
    import { bkZoomImage } from 'bk-magic-vue'
    import myimage from '../../images/403.png'
    export default {
        components: {
            bkZoomImage
        },
        data () {
            return {
                myimage
            }
        },
        created () {
        },
        methods: {
            
        }
    }
</script>

<style scoped lang="postcss">
    @import './index.css';
    .itemDetail-wrapper{
        height: 100%;
        width: 100%;
        .good-info-wapper{
            width: 100%;
            height: 75%;
            display: flex;
            .good-pic{
                height: 750px;
                width: 470px;
                padding: 10px;
                .main-pic{
                    width: 450px;
                    height: 450px;
                    border: 1px solid #999;
                }
                .pic-list{
                    display: flex;
                    flex-wrap: nowrap;
                    height: 108px;
                    margin-top: 10px;
                    .pic-item-wapper{
                        width: 676px;
                        height: 108px;
                        display: flex;
                        flex-wrap: nowrap;
                        overflow: hidden;
                            img{
                                margin: 4px;
                                width: 100px;
                                height: 100px;
                            }
                    }
                    .pic-slide-btn{
                        width: 20px;
                        height: 100%;
                        background: #EAEBF0;
                        cursor: pointer;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    }
                }
            }
            .good-text{
                height: 100%;
                width: 60%;
                border-left: 1px solid #EAEBF0;
            }
        }
    }
</style>
