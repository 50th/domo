<template>
    <!-- <el-row>
        <el-col :span="24" style="text-align: center;">
            <div class="home-box">
                <h1>Domo</h1>
            </div>
        </el-col>
    </el-row> -->
    <el-row>
        <el-col style="text-align: center;">
            <el-card style="max-width: 480px; margin: auto;" shadow="hover">
                <template #header>
                    <div class="home-box">
                        <h1>Domo</h1>
                    </div>
                </template>
                <img src="/src/assets/about.jpg" style="width: 100%" />
            </el-card>
        </el-col>
    </el-row>
</template>
<script setup lang="ts">
</script>
<style scoped>
.home-box {
    text-shadow: 0px 1px 1px rgba(255, 255, 255, 0.6);

    h1 {
        font-size: 3rem;
        margin: 0;
    }
}
</style>
