<template>
  <div>
    <!-- Navbar component at the top -->
    <adminNavbar />
    <!-- Background image --> 
    <img
      class="bg-img"
      src="https://images.unsplash.com/photo-1589578036109-592d4dadb148?q=80&w=2942&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
      alt="Background"
    />
    <!-- Main content starts here -->
    <div class="container">
      <div class="custom-btn">
       <!-- Button container with responsive classes -->
    <div class="d-flex flex-wrap justify-content-center">

      <!-- Rollback Button -->
      <b-col cols="auto" class="mx-2 mb-2">
        <button class="btn btn-success rounded-pill w-100" type="button" @click="rollbackModel">Rollback</button>
      </b-col>

      <!-- Upload data Button -->
      <b-col cols="auto" class="mx-2 mb-2">
        <button class="btn btn-success rounded-pill w-100" type="button" @click="uploadData">Upload Data</button>
      </b-col>

      <!-- Manage Data Button -->
      <b-col cols="auto" class="mx-2 mb-2">
        <button class="btn btn-success rounded-pill w-100" type="button" @click="manageData">Manage Data</button>
      </b-col>

      <!-- Train New Model Button -->
      
      <b-col cols="auto" class="mx-2 mb-2">
        <button class="btn btn-success rounded-pill w-100" type="button" @click="trainModel">Train New Model</button>
      </b-col>
      </div>
        <!-- Display Training Status -->
        <div v-if="trainingInProgress" class="alert alert-success text-center mt-3" role="alert">
          Training in progress. Please wait an hour for the training to complete. Make sure not to click other buttons as it will disrupt the training process.
        </div>
        </div>

           <b-row class="d-flex row justify-content-center my-4">
              <!-- First Card -->
              <div class="flex-wrap col-md-6">
                <div class="card shadow card-container">
            <!-- Card Body -->
            <div class="card-body text-center">
              <!-- Card Title -->
              <h5 class="card-title text-success">Current Model - Version {{ versionCurrent }} </h5>
              <!-- Conditions Card Section -->
              <div
                class="conditions-container mt-4"
                v-if="Object.keys(conditions_card1).length > 0"
              >
                <h5 class="conditions-title">Performance Metrics</h5>
                <div class="subcards-row">
                  <div
                    class="subcard"
                    v-for="(info, title) in conditions_card1"
                    :key="title"
                  >
                    <div class="subcard-content">{{ title }}</div>
                    <div class="subcard-info">{{ info }}</div>
                  </div>
                </div>
              </div>
              <!-- Confusion matrix button -->
                <div>
                <button
                  class="btn btn-success rounded-pill"
                  type="button"
                  @click="toggleMatrixVisibility1"
                >
                  Show Confusion Matrix
                </button>
                  <!-- Show the image only when showMatrix is true -->
                  <div v-if="showMatrix1">
                <!-- Display the image if it exists -->
                 <img v-if="currentVersionMatrix && currentVersionMatrix[0]?.image_path" 
                 :src="currentVersionMatrix[0]?.image_path" alt="Confusion Matrix" class="img-fluid">
                </div>
              </div>  
            </div>
          </div>
        </div>

        <!-- Second Card -->
        <div class="col-md-6">
          <div class="card shadow card-container">
            <!-- Card Body 2 -->
            <div class="card-body text-center">
              <!-- Other model version button with dropdown-->
              <div class="d-grid gap-2 dropdown">
                <button
                  id="button2"
                  class="btn btn-outline-success dropdown-toggle"
                  type="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                 @click="listModels"     
                >
                  Other Models - Version {{ selectedVersion }}
                </button>
                <!-- Dropdown for showing other model version list -->
               <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownMenuButton">
                  <li v-for="version in versions" :key="version">
                     <!--Get the users selected version and pass that to backend -->
                    <a class="dropdown-item" @click="selectVersion(version)">Version {{ version }}</a>
                  </li>
                 </ul> 
              </div>
              <!-- Evaluate model Button -->
              <div class=" card2 d-grid gap-2">
                <button
                  class="btn btn-outline-success"
                  type="button"
                  @click="evaluateVersion"
                >
                  Evaluate
                </button>
              </div>
              <!-- Deploy this model Button -->
              <div class=" card2 d-grid gap-2">
                <button
                  class="btn btn-outline-success"
                  type="button"
                  @click="deployModel"
                >
                 Deploy This Model 
                </button>
              </div>
              <!-- Conditions Card Section 2 -->
              <div
                class="conditions-container mt-4"
                v-if="Object.keys(conditions_card2).length > 0"
              >
                <h5 class="conditions-title">Performance Metrics</h5>
                <div class="subcards-row">
                  <div
                    class="subcard"
                    v-for="(info, title) in conditions_card2"
                    :key="title"
                  >
                    <div class="subcard-content">{{ title }}</div>  
                    <div class="subcard-info">{{ info }}</div>
                  </div>
                </div>
              </div>
              <!-- Confusion Matrix button for card 2 -->
              <div>
                <button
                  class="btn btn-success rounded-pill"
                  type="button"
                  @click="toggleMatrixVisibility"
                >
                  Show Confusion Matrix
                </button>
                <!-- Show the image only when showMatrix is true -->
                  <div v-if="showMatrix">
                  <!-- Display the image if it exists -->
                <img v-if=" selectedVersionMatrix &&  selectedVersionMatrix[0]?.image_path" 
                :src=" selectedVersionMatrix[0]?.image_path" alt="Confusion Matrix1" class="img-fluid">
                </div>
              </div>
            </div>
          </div>
        </div> 
      </b-row>
    </div>
  </div>
</template>


<script>
import axios from "axios";
import adminNavbar from "@/components/adminNavbar.vue";
export default {
  components: {
    adminNavbar,
  },
  name: "admin",
  data() {
    return {
      image: "",
      iterations: 0,
      predictedFlower: "Sunflower",
      selectedFile: null,
      conditions_card1: {
        Precision: "",
        Accuracy: "",
        Recall: "",
        F1: "",
      },
      conditions_card2: {
        Precision: "",
        Accuracy: "",
        Recall: "",
        F1: "",
      },
      versions: [], // Initialize an empty array to store versions
      versionCurrent: "", // Initialize an empty array to store versions for current model
      metrics: null, // Initialize metrics as null
      matrix: null,  // Initialize matrix as null
      showMatrix: false, // Initialize a boolean flag to control the visibility of other matrix version
      showMatrix1: false, // Initialize another boolean flag to control the visibility of current version matrix
      selectedVersionMatrix: [], // Initialize as an empty array to store selected matrixes
      selectedVersion: "", // variable to store the selected version
      trainingInProgress: false, // Initialize a boolean flag to indicate whether training is in progress
    };
  },
  mounted() {
    // Call the methods when the component is mounted (page is loaded)
    this.currentEvaluation();
  },
  methods: {
    trainModel() {
      // Set training in progress to true
      this.trainingInProgress = true;

      const formData = new FormData();
      formData.append("version", "1.0");
      formData.append("topic", "trainModel"); // Updated 'topic' to match the backend

      // Before sending the request
      console.log("Sending FormData:", formData);
      for (var pair of formData.entries()) {
        console.log(pair[0] + ", " + pair[1]);
      }

      // Make the POST request with FormData
      axios
        .post("http://34.141.210.222:8000/trainModel/", formData)
        .then((response) => {
          const responseData = response.data;
          console.log("Message:", responseData.message);      
        })
        .catch((error) => {
          console.error("There was an error!", error);
        });
    },

    /** Get List of all versions of the models via POST with a request body */
    listModels() {
      // Clear the existing versions before making a new request + clearout the versions arraylist upon closing of the dropdown
      this.versions = [];
      const formData = new FormData();
      formData.append("topic", "listModels");

      // POST request with FormData
      axios
        .post("http://34.141.210.222:8000/evaluateModel/", formData)
        .then((response) => {
          const data = response.data;
          console.log("data:", data);

          // Extracting the last 5 versions
          const lastFiveVersions = data.slice(-5);

          // Iterate over each object in the array and extract the version
          lastFiveVersions.forEach((item) => {
            const version = item.version;
            this.versions.push(version);
          });

          // Now "versions" is an array of version strings
          console.log("Versions:", this.versions);
        })
        .catch((error) => {
          console.error("There was an error!", error);
        });
    },

    /** Get currents models - performace metrics & confusion matrix via POST with a request body */
    currentEvaluation() {
      const formData = new FormData();
      formData.append("topic", "currentEvaluation");

      // POST request with FormData
      axios
        .post("http://34.141.210.222:8000/evaluateModel/", formData) // Adjust the endpoint URL as needed
        .then((response) => {
          console.log("Response Data:", response.data);
          const metricsArray = response.data.metrics;
          const matrix = response.data.matrix_images;
          const versionCurrent = response.data.version;

          // Check if the array has at least one element
          if (metricsArray.length > 0) {
            // Extracting the first object from the array
            const metrics = metricsArray[0];
            // Update state variables
            this.metrics = metrics;
            this.matrix = matrix;
            this.versionCurrent = versionCurrent;

            // Extracting values and assigning them to conditions_card1
            this.conditions_card1.Precision = metrics.precision;
            this.conditions_card1.Accuracy = metrics.accuracy;
            this.conditions_card1.Recall = metrics.recall;
            this.conditions_card1.F1 = metrics.f1_score;

            // Now this.metrics and this.matrix can be used as required
            console.log("Metrics:", this.metrics);
            console.log("Matrix:", this.matrix);
            console.log(versionCurrent);

            // Store the matrix for the selected version
            this.currentVersionMatrix = this.matrix;

            // Set showMatrix to true only when the matrix is available
            this.showMatrix1 = this.currentVersionMatrix.length > 0;

            // Set showMatrix to true to display the matrix
            this.showMatrix1 = true;
            console.log("show matrix:", this.showMatrix1);
          } else {
            console.error("Metrics array is empty");
          }
        })
        .catch((error) => {
          console.error("There was an error!", error);
        });
    },

    selectVersion(version) {
      // Set the selected version when a dropdown item is clicked
      this.selectedVersion = version;
      console.log("Selected Version:", this.selectedVersion); // send this.selectedVersion to backend.
      // Clear out the metrics values
      this.metrics = {
        precision: null,
        recall: null,
        accuracy: null,
        f1_score: null,
      };
    },

    /** Get selected models - performace metrics & confusion matrix via POST with a request body */
    evaluateVersion() {
      if (!this.selectedVersion) {
        return; // Ensure that evaluation request is only made when a version is selected.
      }

      const formData = new FormData();
      formData.append("version", this.selectedVersion);
      formData.append("topic", "evaluateVersion");

      // POST request with FormData
      axios
        .post("http://34.141.210.222:8000/evaluateModel/", formData) // Adjust the endpoint URL as needed
        .then((response) => {
          // Storing  metrics and matrix properties from JSON response structure
          const metricsArray = response.data.metrics;
          const matrix = response.data.matrix;

          //Check if the array has at least one element
          if (metricsArray.length > 0) {
            // Extracting the first object from the array
            const metrics = metricsArray[0];
            // Update state variables
            this.metrics = metrics;
            this.matrix = matrix;

            // Extracting values and assigning them to conditions_card2
            this.conditions_card2.Precision = metrics.precision;
            this.conditions_card2.Accuracy = metrics.accuracy;
            this.conditions_card2.Recall = metrics.recall;
            this.conditions_card2.F1 = metrics.f1_score;

            // Now this.metrics and this.matrix can be used as required
            console.log("Metrics:", this.metrics);
            console.log("Matrix:", this.matrix);

            // Store the matrix for the selected version
            this.selectedVersionMatrix = this.matrix;

            // Set showMatrix to true only when the matrix is available
            this.showMatrix = this.selectedVersionMatrix.length > 0;
          } else {
            console.error("Metrics array is empty");
          }
        })
        .catch((error) => {
          console.error("There was an error!", error);
        });
    },

    // Toggle function for the first matrix
    toggleMatrixVisibility() {
      this.showMatrix = !this.showMatrix;
    },

    // Toggle function for the second matrix
    toggleMatrixVisibility1() {
      this.showMatrix1 = !this.showMatrix1;
    },

    /** Delete selected model via POST with a request body */
    rollbackModel() {
      const formData = new FormData();
      formData.append("topic", "rollbackModel");
      // DELETE request with FormData
      axios({
        method: "delete",
        url: "http://34.141.210.222:8000/trainModel/",
        data: formData,
      })
        .then((response) => {
          console.log(response);
          location.reload();
        })
        .catch((error) => {
          console.error("There was an error!", error);
        });
    },

    /** Upload data in database, functionality for the admin */
    uploadData() {
      // Open a new browser window with the specified URL
      window.open("http://34.32.234.118/admin/", "_blank");
    },

    /** Data management in database, fuctionality for admin*/
    manageData() {
      // Open a new browser window with the specified URL
      window.open("http://34.32.239.56/admin/", "_blank");
    },

    /** Deploy model */
    deployModel() {
      const formData = new FormData();
      formData.append("version", this.selectedVersion); // send admins selected version
      formData.append("topic", "deployModel");
      console.log("adminVersion", this.selectedVersion);
      // POST request with FormData
      axios
        .post("http://34.141.210.222:8000/deployModel/", formData)
        .then((response) => {
          const deploy = response.data;
          console.log("response", deploy);

          // Reload the page after successful deployment
          location.reload();
        })
        .catch((error) => {
          console.error("There was an error!", error);
        });
    },
  },
};
</script>


<style scoped>
#button2 {
  font-size: 1.5rem; /* Set font size to 1.5 rem */
  font-weight: bold; /* Set font weight to bold */
}

.bg-img {
  height: 150vh; /* Set height to 150 viewport heights */
  width: 100%; /* Set width to 100% */
  object-fit: cover; /* Ensure the image covers the entire container */
  position: absolute; /* Position absolute for precise placement */
  top: 0; /* Align to the top of the container */
  left: 0; /* Align to the left of the container */
  margin: 0; /* Remove margin */
  padding: 0; /* Remove padding */
  z-index: -1; /* Place the image behind other elements */
}

.card {
  background: rgba(
    255,
    255,
    255,
    0.9
  ); /* Set a slightly transparent white background */
  border-radius: 15px; /* Apply a border radius of 15 pixels for rounded corners */
}

.card-title {
  font-size: 1.5rem; /* Set font size to 1.5 rem */
  margin-bottom: 133px; /* Set margin bottom to 133 pixels */
  font-weight: bold; /* Set font weight to bold */
}

.note {
  font-size: 0.9rem; /* Set font size to 0.9 rem */
}

.btn-outline-success img {
  width: 24px; /* adjust size as needed */
  height: auto;
}

.conditions-container {
  background: linear-gradient(to right, #34a734, #98fb98);
  border-radius: 10px; /* Rounded corners */
  padding: 10px; /* Inner spacing */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
  width: auto; /* Adjust width as necessary */
  margin: 20px auto; /* Center the card with automatic horizontal margins */
  text-align: left; /* Align the text to the left */
}

.conditions-title {
  font-size: 1.2rem;
  color: #ffffff; /* Color for the title */
  margin-bottom: 10px; /* Space between title and subcards */
  padding-left: 10px; /* Align title text inside card */
}

.subcards-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* Creates a 2-column grid */
  grid-auto-rows: minmax(
    50px,
    auto
  ); /* Adjust the minimum height of the rows */
  gap: 10px; /* Space between subcards */
  justify-content: center; /* This will center the grid within the conditions container */
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
  height: 60px; /*height of subcards */
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
.btn-outline-success {
  font-size: 1.25rem; /* Adjust the font size as needed */
}
/* Styling for a container with class 'justify-content-center' */
.justify-content-center {
  display: flex; /* Use flexbox for layout */
  align-items: flex-start; /* Align items to the start of the cross axis */
  justify-content: center; /* Center items along the main axis */
}

/* Styling for the element with id 'updateButton' */
#updateButton {
  margin-right: 10px; /* Set a right margin of 10 pixels */
  margin-left: 10px; /* Set a left margin of 10 pixels */
}

/* Styling for the element with id 'manageButton' */
#manageButton {
  margin-right: 10px; /* Set a right margin of 10 pixels */
  margin-left: 10px; /* Set a left margin of 10 pixels */
}

/* Styling for the element with id 'trainButton' */
#trainButton {
  margin-left: 10px; /* Set a left margin of 10 pixels */
}

#updateButton {
  border-radius: 5px; /* Slightly rounded corners for subcards */
  padding: 10px; /* Reduced padding for a tighter look */
  text-align: center; /* Center text inside subcards */
  font-size: 0.9rem; /* Smaller text */
  height: auto !important;
  overflow: hidden; /* Hides the overflow */
}
</style>
