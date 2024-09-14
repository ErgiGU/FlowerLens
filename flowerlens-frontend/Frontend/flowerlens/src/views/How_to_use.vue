<template>
<div>
    <Navbar/>
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-10">
          <div class="card shadow-sm border-0">
            <div class="card-body">
              <h1 class="card-title text-center mb-4">How to use and information</h1>
              <h2 class="text-center text-muted mb-5">Things to consider before and after identifying a flower</h2>
  
              <div class="mb-4">
                <h3>The ideal flower picture</h3>
                <p>
                  The ideal flower picture would be a clear picture of a flower that is a close-up. Ensure that the flower is at a stage where it is fully bloomed and that the picture is in focus, in a well-lit enviroment. Here is how the ideal flower picture should look like:
                </p>
                <!-- Thumbnail image -->
                <img src="../components/icons/example_images/example_flower.jpg" class="thumbnail rounded" alt="Ideal flower picture" @click="enlargeImage">

                <!-- Overlay -->
                <div id="overlay" class="overlay" @click="closeImage"></div>

                <!-- Enlarged image container with close button -->
                <div id="enlargedImageContainer" class="enlarged-image">
                <button id="closeButton" class="close-btn" @click="closeImage">X</button>
                <img id="enlargedImage" src="" alt="Enlarged Flower">
                </div>

              </div>

              <div class="mb-4">
                <h3>The process</h3>
                <p>
                  In order to upload the image and get an identification, you just click choose file and select the image you want to upload. After that, you click the identify flower button and wait for the identification information to appear. You can also press the bin icon to clear the image or prediction in order to make a new one. Reference the pictures below:
                </p>
                <!-- Thumbnail image -->
                <img src="../components/icons/example_images/choose_file.png" class="thumbnail rounded" alt="Ideal flower picture" @click="enlargeImage">
                <img src="../components/icons/example_images/example_prediction.png" class="thumbnail rounded" alt="Ideal flower picture" @click="enlargeImage">
                <img src="../components/icons/example_images/prediction_info.png" class="thumbnail rounded" alt="Ideal flower picture" @click="enlargeImage">
                <!-- Overlay -->
                <div id="overlay" class="overlay" @click="closeImage"></div>

                <!-- Enlarged image container with close button -->
                <div id="enlargedImageContainer" class="enlarged-image">
                <button id="closeButton" class="close-btn" @click="closeImage">X</button>
                <img id="enlargedImage" src="" alt="Enlarged Flower">
                </div>
                </div>

  
                <div class="mb-4">
                    <h3>The information groups</h3>
                    <p>
                        The information groups are the different categories of information that are displayed after identifying a flower. The information groups are as follows:
                        <ul>
                            <li><strong>Identification:</strong> This includes the common name, scientific name, family, and genus of the flower.</li>
                            <li><strong>Appearance:</strong> Details about the color, petal shape, bloom size, and height of the flower.</li>
                            <li><strong>Growing Conditions:</strong> Information on the ideal temperature, sunlight, water, and soil conditions for growing the flower.</li>
                            <li><strong>Care Instructions:</strong> Guidelines on pruning, dealing with pests and diseases, and propagation methods.</li>
                            <li><strong>Flowering:</strong> Information on the blooming season, frequency, duration, and fertilizer requirements.</li>
                            <li><strong>Ecological Impact:</strong> Details on the flower's attractiveness to pollinators, habitat, native regions, and its invasiveness.</li>
                        </ul>
                    </p>
                    <p>You can also hover over a row in order to see exactly what it is. Here is an example below:</p>
                    <!-- Thumbnail image -->
                    <img src="../components/icons/example_images/tooltip.png" class="thumbnail rounded" alt="Ideal flower picture" @click="enlargeImage">

                    <!-- Overlay -->
                    <div id="overlay" class="overlay" @click="closeImage"></div>

                        <!-- Enlarged image container with close button -->
                        <div id="enlargedImageContainer" class="enlarged-image">
                            <button id="closeButton" class="close-btn" @click="closeImage">X</button>
                            <img id="enlargedImage" src="" alt="Enlarged Flower">
                        </div>
                    </div>
  
              <div>
                <h3>Seeing what the AI model focused on</h3>
                <p>
                  You can see in what part of the image the model focused on in order to make its prediction by clicking on the eye icon next to the trash bin icon. The model focuses on the part of the image that it thinks is the most important in order to make its prediction. Here is an example below:
                </p>
                <!-- Thumbnail image -->
                <img src="../components/icons/example_images/heatmap_example.png" class="thumbnail rounded" alt="Ideal flower picture" @click="enlargeImage">

                <!-- Overlay -->
                <div id="overlay" class="overlay" @click="closeImage"></div>

                    <!-- Enlarged image container with close button -->
                    <div id="enlargedImageContainer" class="enlarged-image">
                        <button id="closeButton" class="close-btn" @click="closeImage">X</button>
                        <img id="enlargedImage" src="" alt="Enlarged Flower">
                    </div>
                </div>
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
  },
  methods: {
    enlargeImage(event) {
      const enlargedImageContainer = document.getElementById('enlargedImageContainer');
      const overlay = document.getElementById('overlay');
      const enlargedImage = document.getElementById('enlargedImage');
      enlargedImage.src = event.target.src; // Sets the source of the clicked thumbnail
      enlargedImageContainer.style.display = 'block'; // Show the enlarged image
      overlay.style.display = 'block'; // Show the overlay
    },
    closeImage() {
      const enlargedImageContainer = document.getElementById('enlargedImageContainer');
      const overlay = document.getElementById('overlay');
      enlargedImageContainer.style.display = 'none'; // Hide the enlarged image
      overlay.style.display = 'none'; // Hide the overlay
    }
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
    overflow:auto /* Change to 'hidden' if you don't want any scrollbars */
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


  .thumbnail {
  width: 100px; /* Adjust the thumbnail size as needed */
  height: auto;
  cursor: pointer; /* Indicates that the image is clickable */
}

.enlarged-image {
  display: none; /* Initially don't display the enlarged image */
  position: fixed; /* Fixed position relative to the viewport */
  top: 50%; /* Center vertically */
  left: 50%; /* Center horizontally */
  transform: translate(-50%, -50%); /* Offset the image by half its width and height */
  z-index: 1000; /* Ensure it's above other content */
  cursor: pointer; /* Change cursor for intuitive closing by clicking */
}

/* Optional: Add this for when the enlarged image is visible */
.enlarged-image.show {
  display: block; /* Show the enlarged image */
}

.overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8); /* Dark overlay */
  z-index: 999; /* Under the enlarged image but above everything else */
}

.close-btn {
  position: fixed;
  top: 10px; /* Position as needed */
  right: 10px; /* Position as needed */
  width: 30px; /* Square shape */
  height: 30px; /* Square shape */
  padding: 5px;
  font-size: 14px; /* Adjust as needed */
  line-height: 20px; /* Center the 'X' vertically */
  text-align: center; /* Center the 'X' horizontally */
  background-color: #ffffff;
  border: none;
  border-radius: 5px; /* Rounded edges */
  cursor: pointer;
  z-index: 1001; /* Above the enlarged image */
  box-shadow: 0 2px 5px rgba(0,0,0,0.2); 
}


  </style>
  