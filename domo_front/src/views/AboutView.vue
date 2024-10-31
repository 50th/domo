<template>
    <el-row>
        <el-col :span="24" style="text-align: center;">
            <div class="home-box">
                <h1>Domo</h1>
            </div>
        </el-col>
    </el-row>
</template>
<script setup lang="ts">
</script>
<style scoped>
.home-box {
    h1 {
        font-size: 3rem;
        /* color: rgb(218, 92, 223); */
        letter-spacing: -3px;
        text-shadow: 0px 1px 1px rgba(255, 255, 255, 0.6);
        position: relative;
        z-index: 3;
        margin: 0;
    }

    margin-top: 40px;
    margin-bottom: 80px;
    z-index: 1;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 2rem;
    /* box-shadow: 0px 0px 12px rgba(117, 122, 131, 0.20); */
}
</style>
