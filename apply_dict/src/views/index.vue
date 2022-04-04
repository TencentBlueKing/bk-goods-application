<template>
    <div
        class="wrapper"
        :class="{ his: $route.name === 'applyHistory' }"
    >
        <div class="header">
            <!-- <bk-divider align="left">
                <bk-tag
                    type="filled"
                    style="font-size: 13px"
                ><span>{{$route.meta.alias}}</span></bk-tag>
            </bk-divider> -->
        </div>
        <router-view :key="$route.path"></router-view>
    </div>
</template>

<script>
    export default {

    }
</script>

<style lang="postcss" scoped>
    .wrapper {
        width: 95%;
        margin: 0 auto;
        overflow: auto;
        &.his {
            height: calc(100vh - 200px);
        }
    }
</style>
