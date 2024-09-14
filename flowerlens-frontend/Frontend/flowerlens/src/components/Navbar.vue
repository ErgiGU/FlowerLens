<template>
    <nav class="navbar navbar-expand-lg bg-light">
        <div class="container-fluid">
        <a class="navbar-brand" href="#">
            <RouterLink to="/" class="nav-link" aria-current="page">FlowerLens</RouterLink>
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item me-2">
                <RouterLink to="/how-to-use" class="nav-link" aria-current="page">How to Use</RouterLink>
            </li>
            <li class="nav-item me-md-2">
                <RouterLink to="/About" class="nav-link">About Us</RouterLink>
            </li>
            </ul>

        </div>
        </div>
    </nav>
  <!-- Render the content of the current page view -->
  <router-view v-bind:user="user" />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import 'bootstrap/dist/css/bootstrap.min.css'
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Belanosima&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

.navbar {
  background: linear-gradient(to right, #006400, #98FB98); /* DarkGreen to PaleGreen */
  color: white;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1);
  font-family: 'Belanosima', sans-serif;
  font-size: 1.1rem; /* Adjust the size to your preference */
  position: sticky;
  top: 0;
  width: 100%;
  z-index: 1030; /* Bootstrap's default z-index for navbar is 1030 */
  margin-bottom: 40px
}

.navbar-brand {
  font-family: 'Belanosima', sans-serif;
  color: white; /* Ensure the brand text is white */
  font-size: 1.4rem; /* Adjust the size to your preference */
}

.nav-link, .dropdown-toggle {
  color: white;
  padding: 10px 15px; /* Larger clickable area */
  transition: background-color 0.3s ease, color 0.3s ease; /* Smooth transition for hover effects */
  font-weight: 400;
}

.nav-link:hover, .dropdown-toggle:hover {
  background-color: #f8f9fa; /* Light background on hover for highlight */
  color: #006400; /* DarkGreen text color on hover for contrast */
  border-radius: 5px; /* Rounded corners on hover */
}

.nav-item .router-link-active {
  font-weight: bold;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 5px;
}

.navbar .dropdown-item {
  color: #006400; /* DarkGreen */
}

.navbar .dropdown-item:hover {
  background-color: #f8f9fa;
}
</style>

