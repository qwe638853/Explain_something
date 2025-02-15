import { createApp } from 'vue'
import App from './App.vue'
import { loadFonts } from './plugins/webfontloader'
import { createVuetify } from 'vuetify'
import './style.css'
import 'vuetify/styles'; 
import '@mdi/font/css/materialdesignicons.css';


loadFonts()

const vuetify = createVuetify({
  theme: {
    defaultTheme: 'customTheme',
    themes: {
      customTheme: {
        dark: false, // 默認淺色主題
        colors: {
          primary: '#333333', // 深灰色
          secondary: '#121212', // 黑色
          background: '#f5f5f5', // 淺灰色背景
          surface: '#424242', // 表面灰色
          error: '#ff5252', // 錯誤紅色
          success: '#4caf50', // 成功綠色
        },
      },
    },
  },
});


createApp(App)
  .use(vuetify)
  .mount('#app')
