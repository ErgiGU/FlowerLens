<template>
    <!-- Navbar component at the top -->
    <Navbar/>
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-10">
          <div class="card shadow-sm border-0">
            <div class="card-body">
              <h1 class="card-title text-center mb-4">About Flowerlens</h1>
              <h2 class="text-center text-muted mb-5">Connecting You to the Natural Beauty of Flowers</h2>
  
              <div class="mb-4">
                <h3>Our Journey</h3>
                <p>
                  Flowerlens began with a concious effort to bridge the gap between the natural world and machine learning. Rooted in a passion for botany and digital innovation, our platform is designed to make flower identification not just accessible but also educational and engaging for everyone who is curious.
                </p>
              </div>
  
              <div class="mb-4">
                <h3>Our Flower Identification technology </h3>
                <p>
                  Utilizing a sophisticated Convolutional Neural Network (CNN), Flowerlens offers a unique approach to identifying and learning about various flower species. Our technology delves deep into the attributes of each of the 10 flowers that our model was trained on, presenting users with accurate, insightful information.
                </p>
              </div>
  
              <div class="mb-4">
                <h3>Our Mission</h3>
                <p>
                  Our mission at Flowerlens is simple: to enhance the appreciation of floral diversity and beauty. We strive to provide an informative and user-friendly platform for botanical enthusiasts, gardeners, and anyone curious about the flora around them.
                </p>
              </div>
  
              <div>
                <h3>Get in Touch</h3>
                <p>
                  We're always eager to hear from our users. Whether you have questions, feedback, or want to share your floral discoveries, feel free to reach out at contact@flowerlens.com. Join us in our journey to explore the colorful world of flowers.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>



<script>
    import Navbar from '@/components/Navbar.vue'
    export default {
        components: {
        Navbar
        }
    }
</script>

<style scoped>
.card {
  background: #ffffff;
  border-radius: 15px;
  box-shadow: 0 10px 20px rgba(72, 187, 120, 0.2); /* Light green shadow */
}

.card-body {
  overflow: hidden; /* Change to 'hidden' if you don't want any scrollbars */
  /* Other styles */
}


.card-title, .card h3 {
  color: #48BB78; /* Nice shade of green */
  font-family: 'Belanosima', sans-serif;
}

.card p {
  font-size: 1rem;
  line-height: 1.6;
}

@media (max-width: 767.98px) {
  .card-title {
    font-size: 1.5rem;
  }
  .card h2 {
    font-size: 1.25rem;
  }
  .card h3 {
    font-size: 1.1rem;
  }
}
</style>


