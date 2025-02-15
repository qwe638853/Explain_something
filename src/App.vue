<template>
  <v-app color="background">
    <v-app-bar :elevation="1">
      <v-app-bar-title color="primary" >Track Something</v-app-bar-title>
    </v-app-bar>
    <v-main class="pa-4" fluid>
        <index/>
    </v-main>
  </v-app>
</template>

<script>

import index from './components/index.vue'

export default {
  name: 'App',

  components: {
    index,
  },

  data: () => ({
    //
  }),
}
</script>
