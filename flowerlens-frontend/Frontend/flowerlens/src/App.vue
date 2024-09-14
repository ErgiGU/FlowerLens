<script setup>
import { RouterLink, RouterView } from 'vue-router'
import 'bootstrap/dist/css/bootstrap.min.css'
</script>

<template>
 <div id="app">
    <!-- Render the content of the current page view -->
    <!-- Background image -->
  <img class="bg-img" src="https://images.unsplash.com/photo-1589578036109-592d4dadb148?q=80&w=2942&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="Background">
    <router-view v-bind:user="user" />
  </div>
</template>

<style scoped>

.bg-img {
  height: 100vh;
  width: 100%;
  object-fit: cover;
  position: fixed;
  z-index: -1;
}
</style>
