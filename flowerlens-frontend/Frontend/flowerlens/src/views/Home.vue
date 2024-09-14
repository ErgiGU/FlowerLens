<template>
  <div>
    <!-- Navbar component at the top -->
    <Navbar />

    <!-- Main content starts here -->
    <div class="container">
      <!-- Page content starts here -->
      <div class="row justify-content-center my-6">
        <!-- Add some top and bottom margin -->
        <div class="col-12 col-sm-10 col-md-8">
          <div class="card shadow card-container">
            <!-- Card Body -->
            <div class="card-body text-center">
              <!-- Title -->
              <h5 class="card-title text-success">Identify a Flower</h5>
              <!-- Subtitle -->
              <p class="card-text">
                Ever wondered which flower you're looking at? Find out!
              </p>
              <!-- File Input and Clear Button -->
              <div class="input-group mb-3">
                <input
                  type="file"
                  class="form-control"
                  id="formFile"
                  accept="image/*"
                  @change="loadAndPreviewImage"
                />
                <button
                  class="btn btn-outline-success"
                  type="button"
                  id="button-addon2"
                  @click="clearImage"
                >
                  <img src="/trash.svg" alt="Clear Image" />
                </button>
                <!-- Eye Button -->
                <button
                  class="btn btn-outline-success"
                  type="button"
                  id="button-addon3"
                  @click="showHeatmap"
                >
                  <img src="/eye.svg" alt="View Heatmap" />
                </button>
              </div>

              <!-- Identify Flower Button -->
              <div class="d-grid gap-2">
                <button
                  class="btn btn-success"
                  type="button"
                  @click="identifyFlower"
                >
                  <span
                    v-if="loading"
                    class="spinner-border spinner-border-sm"
                    role="status"
                    aria-hidden="true"
                  ></span>
                  <span v-else>{{ buttonText }}</span>
                </button>
              </div>

              <!-- Image Preview -->
              <img
                id="frame"
                :src="image"
                class="img-fluid mt-3"
                v-if="image"
              />
              <!-- Predicted Flower -->
              <!-- Predicted Flower -->
              <div v-if="predictedFlower" class="prediction-card mt-2">
                <h5>Predicted Flower:</h5>
                <p class="prediction-text">{{ formattedPredictedFlower }}</p>
              </div>

              <!-- FlowerInfoGroups Card Section -->
              <div v-if="flowerInfoGroups.length > 0">
                <div
                  v-for="group in flowerInfoGroups"
                  :key="group.title"
                  class="flowerInfoGroups-container mt-4"
                >
                  <h5 class="flowerInfoGroups-title">{{ group.title }}</h5>
                  <div class="subcards-row">
                    <div
                      class="subcard"
                      v-for="(info, key) in group.details"
                      :key="key"
                    >
                      <div class="subcard-content" :title="tooltips[key]">
                        {{ key }}
                      </div>
                      <div class="subcard-info">{{ info }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Heatmap Modal -->
              <div v-if="isHeatmapModalOpen" class="heatmap-modal">
                <div class="heatmap-modal-content">
                  <span class="close" @click="showHeatmap">&times;</span>
                  <p class="heatmap-label">Heatmap</p>
                  <!-- This is the text label for the heatmap -->
                  <img :src="heatmap" class="img-fluid" alt="Heatmap Image" />
                </div>
              </div>
              <!-- Note -->
              <p class="note text-secondary mt-3">
                Note: Please ensure the image of your flower is as clear as
                possible, and make sure it's a close-up.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";
import Navbar from "@/components/Navbar.vue";
export default {
  components: {
    Navbar,
  },
  name: "home",
  data() {
    return {
      image: "",
      predictedFlower: "", // To store the predicted flower name
      loading: false,
      buttonText: "Identify Flower", // Default button text
      heatmap: null,
      isHeatmapModalOpen: false,
      selectedFile: null, //Store the selected file
      flowerInfoGroups: [], //this is where the flower info will be stored when the backend returns it
      tooltips: {
        "Common Name":
          "The name commonly used to refer to the flower in everyday language.",
        "Scientific Name":
          "The formal scientific name of the flower, used by botanists and in the scientific community.",
        Family:
          "The larger taxonomic category to which the flower belongs, grouping together related genera.",
        Genus:
          "A category that ranks above species and below family, often grouping species with similar characteristics.",
        Color: "The predominant color(s) of the flower's petals.",
        "Petal Shape":
          "The shape or form of the individual petals of the flower.",
        "Bloom Size":
          "The average diameter or width of the flower when fully open.",
        Height:
          "The typical range of height the plant reaches when fully grown.",
        Temperature: "The range of temperatures the flower can thrive in.",
        Sunlight:
          "The amount of direct sunlight the flower needs for optimal growth.",
        Water:
          "The watering requirements for the flower, indicating how much and how often.",
        Soil: "The type of soil that is best suited for the flower’s growth, including pH level and composition.",
        Pruning:
          "Guidance on cutting back parts of the flower to promote healthy growth.",
        Pests:
          "Information on common pests that may affect the flower and how to manage them.",
        Diseases:
          "Common diseases that can impact the flower and methods for prevention or treatment.",
        Propagation:
          "Methods for breeding the flower from the original stock, such as by seed, cuttings, or division.",
        "Blooming Season":
          "The specific time of year when the flower is expected to bloom.",
        Frequency: "How often the flower blooms within a season or year.",
        "Bloom Duration":
          "The length of time a flower’s bloom is typically expected to last.",
        Fertilizer:
          "The type of fertilizer that is best suited for the flower’s growth.",
        "Attractiveness To Pollinators":
          "An indicator of how likely the flower is to attract bees, butterflies, and other pollinators.",
        Habitat:
          "The natural environment where the flower is typically found or thrives best.",
        "Native Regions":
          "Geographical areas where the flower originates from or is naturally found.",
        Invasiveness:
          "A measure of the flower's tendency to spread beyond its intended area, potentially becoming a weed.",
      },
    };
  },
  computed: {
    formattedPredictedFlower() {
      // Replace underscores with spaces and capitalize the first letter
      let formattedFlower = this.predictedFlower.replace(/_/g, " ");
      return formattedFlower.charAt(0).toUpperCase() + formattedFlower.slice(1);
    },
  },
  methods: {
    loadAndPreviewImage(event) {
      this.selectedFile = event.target.files[0];
      if (this.selectedFile) {
        this.image = URL.createObjectURL(this.selectedFile);
      }
    },
    identifyFlower() {
      if (this.selectedFile) {
        this.loading = true; // Start loading
        this.buttonText = "Identifying..."; // Change button text to show loading state

        const formData = new FormData();
        formData.append("photo", this.selectedFile);
        formData.append("topic", "uploadPhoto"); // Include 'topic' in the FormData

        // Make the POST request with FormData
        axios
          .post("http://34.141.210.222:8000/uploadPhoto/", formData)
          .then((response) => {
            this.loading = false; // Stop loading
            this.buttonText = "Flower Identified!"; // Update button text to indicate completion
            this.predictedFlower = response.data.prediction;
            this.flowerInfoGroups = response.data.flowerInfo;

            // Handle the Base64 encoded heatmap
            if (response.data.heatmap) {
              // Assuming the heatmap data is a Base64 encoded string
              this.heatmap = "data:image/png;base64," + response.data.heatmap;
            }
            console.log(response);
          })
          .catch((error) => {
            this.loading = false; // Stop loading in case of error
            this.buttonText = "Try Again"; // Reset button text
            console.error("There was an error!", error);
          });
      }
    },
    clearImage() {
      document.getElementById("formFile").value = null;
      this.image = "";
      this.predictedFlower = "";
      this.buttonText = "Identify Flower";
      this.flowerInfoGroups = [];
      this.heatmap = null;
    },
    showHeatmap() {
      if (this.heatmap) {
        this.isHeatmapModalOpen = !this.isHeatmapModalOpen;
      }
    },
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Belanosima&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap");

/*subcards css code start*/
/* Conditions container styles */
.flowerInfoGroups-container {
  background: linear-gradient(to right, #34a734, #98fb98);
  border-radius: 10px; /* Rounded corners */
  padding: 10px; /* Inner spacing */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
  width: auto; /* Adjust width as necessary */
  margin: 20px auto; /* Center the card with automatic horizontal margins */
  text-align: left; /* Align the text to the left */
}

.flowerInfoGroups-title {
  font-family: "Belanosima", sans-serif;
  font-size: 1.2rem;
  color: #ffffff; /* Color for the title */
  margin-bottom: 10px; /* Space between title and subcards */
  padding-left: 10px; /* Align title text inside card */
}

.subcards-row {
  display: grid;
  grid-template-columns: repeat(
    2,
    1fr
  ) !important; /* Create exactly two columns */
  gap: 10px; /* Space between subcards */
}

/* For larger screens, if you want two columns, you can add a media query */
@media (max-width: 600px) {
  .subcards-row {
    grid-template-columns: 1fr !important; /* Force a single column layout on small screens */
  }
}

.subcard {
  background: #f9fdfa; /* Light base color */
  background-image: linear-gradient(
    to right top,
    #e4f4ec,
    #e9f7ef,
    #eff9f2,
    #f4fbf5,
    #f9fdfa
  ); /* Subtle gradient */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #e6e6e6; /* Light border */
  transition: all 0.3s ease-in-out; /* Smooth transition for hover effects */
  color: #333; /* Darker text for readability */
  border-radius: 5px; /* Slightly rounded corners for subcards */
  padding: 10px; /* Reduced padding for a tighter look */
  text-align: center; /* Center text inside subcards */
  font-size: 0.9rem; /* Smaller text */
  height: auto !important;
  overflow: hidden; /* Hides the overflow */
}

.subcard:hover {
  background-image: linear-gradient(
    to right top,
    #d9eedc,
    #deefe0,
    #e4f1e4,
    #e9f3e8,
    #eff5ec
  ); /* Slightly different gradient on hover */
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1); /* Larger shadow on hover */
}

.subcard-content {
  font-weight: bold; /* Make title of subcard bold */
  margin-bottom: 5px; /* Space between title and info */
}

.subcard-info {
  font-size: 0.85rem; /* Smaller info text */
  font-weight: normal; /* Regular weight for info */
}

/*subcards css code end*/

.card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 15px;
  max-height: 90vh;
  overflow-y: auto; /* Enables scrolling */
}

.card-title {
  font-size: 1.5rem;
}

.note {
  font-size: 0.9rem;
}

/* Style for the trash bin button */
.btn-outline-success {
  border: none;
  background: transparent;
}

.btn-outline-success img {
  width: 24px; /* adjust size as needed */
  height: auto;
}

/* Flexbox utility classes */
.d-flex {
  display: flex;
  align-items: center;
}

.ml-2 {
  margin-left: 0.5rem; /* adjust spacing as needed */
}

.btn-outline-success img {
  transition: filter 0.3s ease; /* Smooth transition for the filter effect */
  /* Initial filter here if needed */
}

.btn-outline-success:hover img,
.btn-outline-success:active img {
  filter: brightness(0) invert(1); /* This will change the image to white */
}

/* spinner styles */
.btn-success {
  color: #fff;
  background-color: #28a745;
  border-color: #28a745;
}

/* Modal Styles */
.heatmap-modal {
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0, 0, 0); /* Fallback color */
  background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */
}

.heatmap-modal-content {
  margin: 15% auto; /* Adjust top margin as needed, auto centers horizontally */
  padding: 20px;
  border: 1px solid #888;
  width: 90%; /* Adjust to match the card width, or set a fixed width */
  max-width: 600px; /* Optional: if the card has a max-width, match it here */
  background-color: white;
  border-radius: 15px; /* Rounded corners for the modal */
  position: relative; /* Needed for absolute positioning of the close button */
  display: flex;
  overflow-y: auto; /* Enable vertical scrolling */
  max-height: 90vh; /* Maximum height to ensure it fits within the viewport */
  flex-direction: column; /* Stack children vertically */
  align-items: center; /* Center items horizontally */
  justify-content: center; /* Center items vertically */
}

.heatmap-modal-content img {
  max-height: 75vh; /* Limit the image height to ensure it fits within the modal */
  max-width: 100%; /* Image can take up to full width of the modal content */
}

.heatmap-modal-content p {
  margin-bottom: 1rem; /* Add some space between the text and the image */
  font-size: 1.1rem;
  color: green;
}

/* The Close Button */
.close {
  position: absolute; /* Absolute position relative to its parent */
  top: 10px; /* 10px from the top of the modal */
  right: 10px; /* 10px from the right of the modal */
  background-color: #f2f2f2; /* Light background for the button */
  border-radius: 50%; /* Circle shape */
  width: 30px; /* Width of the close button */
  height: 30px; /* Height of the close button */
  line-height: 30px; /* Center the '×' vertically */
  text-align: center; /* Center the '×' horizontally */
  cursor: pointer;
  border: none; /* No border */
  font-size: 24px; /* Larger font size for the '×' symbol */
  display: flex;
  justify-content: center;
  align-items: center;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.prediction-text {
  font-size: 1.5rem;
}
</style>