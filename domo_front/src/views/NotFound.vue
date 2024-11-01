<template>
    <el-row>
        <el-col :span="24" style="text-align: center;">
            <div class="home-box">
                <h1>404 Not Found</h1>
            </div>
        </el-col>
    </el-row>
    <el-row>
        <el-col :span="24" style="text-align: center;">
            <div>
                <RouterLink style="text-decoration: none;" :to="{ name: 'home' }">返回首页</RouterLink>
            </div>
        </el-col>
    </el-row>
</template>
<script setup lang="ts">
</script>
<style scoped>
.home-box {
    font-size: 2rem;
    text-shadow: 0px 1px 1px rgba(255, 255, 255, 0.6);
}
</style>
