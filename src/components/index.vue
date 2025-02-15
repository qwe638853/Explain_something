<template>
  <v-container class="mt-16">
    <v-col>
      <v-row>
        <v-select 
          v-model="period"
          label="選擇查詢時間範圍"
          :items="['day', 'week', 'month', 'year']"
          variant="solo"
        ></v-select>
      </v-row>
      <v-row>
        <v-text-field
        v-model="walletAddress"
        :loading="loading"
        append-inner-icon="mdi-magnify"
        density="default"
        label="Search templates"
        hide-details
        variant="solo"
        @click:append-inner="sendWalletAddress"
      ></v-text-field>
      </v-row>  
    </v-col>
    
    <div v-if="errorMessage" class="alert-overlay" @click="closeAlertOverlay">
      <v-alert type="error" class="text-center alertBox" @click.stop>
        {{ errorMessage }}  
      </v-alert>
    </div>

    <v-col v-if="analysisResult" class="mt-12">
      <v-row >
        <v-card class="pa-3 " elevation="2">
          <v-card-title>分析結果</v-card-title>
          <v-card-text>
            <div class="pre-container">
              <pre>{{ JSON.stringify(analysisResult, null, 2) }}</pre>
            </div>
          </v-card-text>
        </v-card>
      </v-row>
    </v-col>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name:"index",
  data(){
    return {
      walletAddress:"",
      period: "week",
      analysisResult: null,
      loading: false,
      errorMessage: "",
      errorAlert: false,
    }
  },
  methods:{
    async sendWalletAddress(){
      if(!this.walletAddress){
        this.errorMessage = "請輸入有效的錢包地址";
        return;
      }
      this.loading = true;
      this.errorMessage = "";
      this.analysisResult = null;
      try{
        const response = await axios.post("http://localhost:8000/app/analyze_wallet", {
          address: this.walletAddress,
          period: this.period
        });
        this.analysisResult = response.data.analysis;
      }catch (error) {
        console.error("Error analyzing wallet:", error);
        this.errorMessage = "分析失敗，請檢查錢包地址或稍後再試。";
      } finally {
        this.loading = false;
      }
    },
    closeAlertOverlay() {
      this.errorMessage = "";
    },
  }
};


</script>

<style lang="css" scoped>
.v-text-field ::v-deep(.v-icon) {
  color: #f5f5f5
}

.v-container{
  padding: 30px;
}

.v-select{
  max-width: 250px;
}
.alert-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(65, 46, 46, 0.085);  /* 例如：紅色半透明背景 */
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
}
.alertBox {
  max-width: 30%;
}

/* 結果區塊的 pre 容器 */
.pre-container {
  overflow-y: auto;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: Consolas, Menlo, Monaco, monospace;
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow-wrap: break-word;
}







</style>