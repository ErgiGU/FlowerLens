<template>
  <div class="login-container d-flex justify-content-center align-items-center">
    <div class="col-md-6">
      <div class="card border-success">
        <div class="card-header bg-light-green text-white text-center">
          Admin Login
        </div>
        <div class="card-body">
          <form @submit.prevent="login">
            <div class="form-group">
              <label for="username">Username</label>
              <input
                type="text"
                id="username"
                v-model="username"
                class="form-control"
                required
              />
            </div>
            <div class="form-group">
              <label for="password">Password</label>
              <input
                type="password"
                id="password"
                v-model="password"
                class="form-control"
                required
              />
            </div>
            <div class="d-flex justify-content-center">
              <button type="submit" class="btn btn-light-green text-white mt-3">
                Login
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";
import Cookies from "js-cookie";

export default {
  data() {
    return {
      username: "",
      password: "",
      apiUrl: "http://34.141.210.222:8000/api",
    };
  },
  methods: {
    async login() {
      console.log("login method called");
      try {
        const response = await axios.post(
          `${this.apiUrl}/login/`,
          {
            username: this.username,
            password: this.password,
          },
          { withCredentials: true }
        ); // Make sure to include withCredentials

        localStorage.setItem("access_token", response.data.access);
        localStorage.setItem("refresh_token", response.data.refresh);

        // Now navigate to the admin page
        this.$router.push("/admin");

        console.log(response.data.detail);
      } catch (error) {
        console.error("Invalid credentials", error);
        // Handle error, such as displaying a login error message
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  height: 100vh;
  max-width: 1000px; /* Adjust as necessary */
  margin: auto;
}

.bg-light-green,
.btn-light-green {
  background-color: #187e18; /* This is a lighter green color. Adjust as necessary. */
}
</style>