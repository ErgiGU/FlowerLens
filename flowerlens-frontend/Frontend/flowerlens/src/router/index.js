import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import HowTo from '../views/How_to_use.vue'
import AdminLogin from '../views/AdminLogin.vue'
import Cookies from 'js-cookie'
import About from '../views/About.vue'
import Instructions from '../views/Instructions.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },

    {
      path: '/admin',
      name: 'Admin',
      component: AdminDashboard,
      meta: { requiresAuth: true } // Indicate that this route requires authentication
    },
    {
      path: '/login',
      name: 'AdminLogin',
      component: AdminLogin
    },
    {
      path: '/how-to-use',
      name: 'How-to-use',
      component: HowTo
    },
    {
      path: '/about',
      name: 'about',
      component: About
    },
    {
      path: '/instructions',
      name: 'instructions',
      component: Instructions,
      meta: { requiresAuth: true } // Indicate that this route requires authentication
    }
  ]
})

router.beforeEach((to, from, next) => {
  const accessToken = localStorage.getItem('access_token');

  if (to.path === '/login' && accessToken) {
    // If trying to access login page but the token already exists, redirect to admin page
    next({ path: '/admin' });
    return;
  }

  if (to.path === '/login' && accessToken) {
    // If trying to access login page but the token already exists, redirect to instructions page
    next({ path: '/instructions' });
    return;
  }

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (accessToken) {
      next(); // If token exists, proceed
    } else {
      next({ path: '/login' }); // If no token, redirect to login
    }
  } else {
    next(); // Proceed if the route does not require authentication
  }
});





export default router
