<template>
    <el-row>
        <el-col :span="24" style="text-align: center;">
            <div class="home-box">
                <h1>404 Not Found</h1>
                <h4>盲生，你发现了华点</h4>
            </div>
        </el-col>
    </el-row>
    <el-row>
        <el-col :span="24" style="text-align: center;">
            <div class="router-box">
                <RouterLink :to="{ name: 'home' }">{{ counter }} 秒后返回首页
                </RouterLink>
            </div>
        </el-col>
    </el-row>
</template>
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const timer = ref<number | null>(null);
const counter = ref<number>(10)
onMounted(() => {
    timer.value = setInterval(() => {
        if (counter.value <= 1) {
            router.push({ name: 'home' });
        } else {
            counter.value--;
            console.log(counter.value);
        }
    }, 1000)
})
onUnmounted(() => {
    if (timer.value) { clearInterval(timer.value) }
})
</script>
<style scoped>
.home-box {
    text-shadow: 0px 1px 1px rgba(255, 255, 255, 0.6);

    h1 {
        font-size: 4rem;
    }
}

.router-box {
    a {
        text-decoration: none;
        color: #ec7728;
    }
}
</style>
