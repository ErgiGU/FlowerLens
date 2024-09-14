<template>
  <div>
    <!-- Navigation bar with light background -->
    <nav class="navbar navbar-expand-lg bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">
          <RouterLink to="/admin" class="nav-link" aria-current="page">FlowerLens</RouterLink>
        </a>
         <!-- Navbar toggle button for responsive design -->
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <!-- Navbar items container -->
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
             <!-- Navigation item for instructions page -->
            <li class="nav-item me-2">
              <RouterLink to="/instructions" class="nav-link" aria-current="page">Instructions</RouterLink>
            </li>

           <!-- Navigation item for about page -->
            <li class="nav-item me-md-2">
              <RouterLink to="/about" class="nav-link">About</RouterLink>
            </li>
          </ul>

       <!-- Logout button aligned to the right -->
       <ul>
      <li id="logout" class="nav-item justify-content-end me-4">
        <!-- Container for the logout button -->
      <div class="logout-container" @click="logout">
        <button class="btn btn-success btn-rectangular rounded-2" @mouseover="hovered = true" @mouseleave="hovered = false">
          <!-- SVG icon for logout -->
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-box-arrow-right icon" viewBox="0 0 16 16">
              <path fill-rule="evenodd" d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0z"/>
              <path fill-rule="evenodd" d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3z"/>
            </svg>
            Logout
          </button>
      </div>
    </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>


<script setup>
import { RouterLink, useRouter, RouterView } from 'vue-router'
import 'bootstrap/dist/css/bootstrap.min.css'
// Get the router instance
const router = useRouter();

async function logout() {

  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  // Optionally, redirect to the login page or another page
  router.push('/login');

}
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

/* Logout button styling */
.btn-rectangular {
  background-color: green;
  margin-top: 12px;
  border: 0;
}

.btn-rectangular:hover {
  background-color: white; /* Change background color to white on hover */
  color: #006400;

}
</style>


