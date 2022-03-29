<template>
    <div class="applyHistory-wrapper">
        <div class="condition-form">
            <history-form
                @search="handleSearch"
                ref="historyForm"
            ></history-form>
        </div>
        <div class="historyTable">
            <history-table
                @edit="editHistory"
                ref="historyTable"
            ></history-table>
        </div>
    </div>
</template>

<script>
    import HistoryForm from '@/components/apply/history/historyForm.vue'
    import HistoryTable from '@/components/apply/history/historyTable.vue'

    export default {
        components: {
            HistoryForm,
            HistoryTable
        },
        data () {
            return {
            }
        },
        methods: {
            handleSearch (formData) {
                this.$refs.historyTable.search(formData)
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
    .applyHistory-wrapper {
        .condition-form {
            padding: 30px 0 0 0;
        }
        .historyTable {
            text-align: right;
            .more-options {
                margin: 0 10px 10px 0;
                .multi-export:hover {
                }
            }
        }
    }
</style>
