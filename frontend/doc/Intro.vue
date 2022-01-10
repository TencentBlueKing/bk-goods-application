<template>
    <div id="app">
        <app-header></app-header>
        <div class="app-container">
            <div class="app-side-nav">
                <side-nav></side-nav>
            </div>
            <div class="placeholder"></div>
            <div class="app-content">
                <router-view></router-view>
            </div>
        </div>
        <app-footer></app-footer>
    </div>
</template>

<style lang="postcss">
    @import '@/css/reset.css';
    @import '@doc/css/intro.css';
</style>
