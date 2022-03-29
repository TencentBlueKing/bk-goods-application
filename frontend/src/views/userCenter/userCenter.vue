<template>
    <div class="userCenter-wrapper">
        <center-form ref="centerForm"></center-form>
    </div>
</template>

<script>

    import CenterForm from '@/components/user/center/centerForm.vue'

    export default {
        components: {
            CenterForm
        },
        methods: {
            loadData () {
                this.$refs.centerForm.getUserInfo()
                this.$refs.centerForm.getPosition()
            }
        }
    }
</script>

<style lang="postcss" scoped>
</style>
