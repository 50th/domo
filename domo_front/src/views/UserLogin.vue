<template>
    <el-row style="margin-top: 3%;">
        <el-col :span="6" :offset="9">
            <el-card shadow="hover">
                <template #header>
                    <div class="login-header">
                        <span>Domo</span>
                    </div>
                </template>
                <el-form style="padding: 5% 15% 0 15%;" label-width="auto" :model="loginForm" size="default"
                    :hide-required-asterisk="true">
                    <el-form-item :required="true" label="用户名">
                        <el-input v-model="loginForm.username" />
                    </el-form-item>
                    <el-form-item :required="true" label="密码">
                        <el-input v-model="loginForm.password" type="password" show-password @keyup.enter="userLogin" />
                        <el-checkbox v-model="loginForm.save_password" :value="true">
                            记住密码
                        </el-checkbox>
                    </el-form-item>
                    <el-form-item>
                        <el-button style="margin: auto;" type="success" size="default" plain :auto-insert-space="true"
                            @click="userLogin">登录</el-button>
                    </el-form-item>
                </el-form>
            </el-card>
        </el-col>
    </el-row>
</template>

<script setup lang="ts">
import { onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import { loginApi } from '@/apis/authApis'
import { useUserStore } from '@/stores/user'

const router = useRouter();

const loginForm = reactive({
    username: '',
    password: '',
    save_password: false
})
const user = useUserStore();
const userInfo = user.getUser();

const userLogin = () => {
    if (loginForm.username && loginForm.password) {
        loginApi(loginForm.username, loginForm.password).then(res => {
            if (res.code == 0) {
                if (loginForm.save_password) {
                    localStorage.setItem('username', loginForm.username);
                    // 密码转为 base64 保存
                    localStorage.setItem('password', window.btoa(Date.now() + '_' + loginForm.password));
                }
                user.setUser(res.data)
                router.push({ name: 'home' });
            }
        })
    } else {
        ElMessage.warning('请输入用户名密码');
    }
}

onMounted(async () => {
    if (userInfo) {
        router.push({ name: 'home' });
    } else {
        // 检查是否保存了密码
        const username = localStorage.getItem('username');
        const password = localStorage.getItem('password');
        if (username && password) {
            const pwd = window.atob(password);
            loginForm.username = username;
            loginForm.password = pwd.split('_')[1];
            loginForm.save_password = true;
        }
    }
})
</script>
<style>
.login-header {
    text-align: center;
    font: small-caps bold 25px/1 sans-serif;
}
</style>
