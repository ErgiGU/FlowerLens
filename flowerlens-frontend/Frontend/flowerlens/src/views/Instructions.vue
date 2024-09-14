<template>
<div>
    <adminNavbar/>
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-md-10">
          <div class="card shadow-sm border-0">
            <div class="card-body">
              <h1 class="card-title text-center mb-4">Instructions for Admin Page</h1>
              <h2 class="text-center text-muted mb-5">Functionality</h2>
             <!-- Rollback Functionality Section  -->
              <div class="mb-4">
                <h3>Rollback</h3>
                <p>
                 The rollback button is used to revert to the previous model version from the current one.
                </p>
              </div>

              <!-- Upload Image Functionality Section -->
              <div class="mb-4">
                <h3> Upload Image</h3>
                <p>
                  Upload image button redirects to the database where new images can be uploaded.
                </p>
              </div>
  
             <!-- Data Management Section  -->
              <div class="mb-4">
                <h3>Manage Data</h3>
                <p>
                  Manage Data Button redirects to the database where various operations for example delete, update etc can be conducted on the data.
                </p>
              </div>

              <!-- Train Model Functionality Section -->
              <div class="mb-4">
                <h3>Train Model</h3>
                <p>
                  Train Model Button triggers a training of a model which could take approximately an hour. 
                </p>
              </div>

             <!-- Current Model Section -->
              <h2 class="text-center text-muted mb-5">Models</h2>
              <div class="mb-4">
                <h3>Current Model</h3>
                <p>
                 The Current Model Section shows which model is currently deployed along with it's performance metrics and confusion metrics. 
                </p>
              </div>

              <!-- Performance Metrics Section -->
              <div class="mb-4">
                <h3>Performance Metrics</h3>
                <p>
                 Performance Metrics gives the following information about the model : Accuracy, Precision, F1 score and Recall in percentages. These metrics can be used to compare the quality and efficiency of current model with other models.  </p> 
                     <p> - Accuracy: The proportion of correctly classified flower images out of the total flower images in the class. </p> 
                     <p> - Precision:  The proportion of true positives out of the total predicted positives. </p> 
                     <p> - Recall: The proportion of true positives out of the total actual positives. </p> 
                    <p> - F1 Score: The harmonic mean of precision and recall, providing a balance between the two metrics. </p>  
              </div>

             <!-- Confusion Matrix Section -->
              <div class="mb-4">
                <h3>Confusion Matrix</h3>
                <p>
                  The Show Confusion Matrix button presents a Confusion Matrix image of the respective model version which provides the summary of the models predictions compared to the actual value. The distinct diagonal line seen in the matrix represents the flower images that are correctly classified by the model. 
                </p>
              </div>

            <!-- Other Model Versions Section -->
              <div class="mb-4">
                <h3>Other Model Versions (Dropdown) </h3>
                <p>
                  The Other Model Versions shows a dropdown wih the list of versions of the trained models. A specific model version can be selected from the dropdown with the purpose of checking the performance metrics and confusion matrix 
                </p>
              </div>

              <!-- Model Evaluation Section -->
              <div class="mb-4">
                <h3>Evaluate Model</h3>
                <p>
                  Evaluate Model button shows the information i.e performance metrics percentages and confusion matrix of the selected model version from aforementioned dropdown list.
                </p>
              </div>

              <!-- Model Deployment Section -->
              <div class="mb-4">
                <h3>Deploy Model</h3>
                <p>
                  Deploy Model button deploys the specific model which is selected and evaluated. When a model is deployed it replaces the previously existing current version model.
                </p>
              </div>

              <!-- Technical Issue Section -->
              <div>
                <h3>Technical Issues</h3>
                <p>
                  In case of any technical issues, contact the developer team via the email: contact@flowerlens.com
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</div>
  </template>

   <script>
  import adminNavbar from '@/components/adminNavbar.vue'
  export default {
    components: {
        adminNavbar
    }
  }
  </script>

  <style scoped>
.card {
  background: #ffffff;  /* Set background color to white */
  border-radius: 15px;   /* Apply a border radius of 15 pixels for rounded corners */
  box-shadow: 0 10px 20px rgba(72, 187, 120, 0.2);  /* Apply a light green shadow */
}

.card-body {
  overflow-y: auto;  /* Add vertical scrollbars if content overflows */
}

.card-title,
.card h3 {
  color: #48BB78;   /* Set text color to a nice shade of green */
  font-family: 'Belanosima', sans-serif;  /* Use 'Belanosima' font family */
}

.card p {
  font-size: 1rem;   /* Set font size to 1 rem */
  line-height: 1.6;  /* Set line height to 1.6 for better readability */
}

/* Media query for screens with a maximum width of 767.98 pixels */
@media (max-width: 767.98px) {
  .card-title {
    font-size: 1.5rem;   /* Increase font size for smaller screens */
  }
  .card h2 {
    font-size: 1.25rem;  /* Adjust font size for smaller screens */
  }
  .card h3 {
    font-size: 1.1rem;   /* Adjust font size for smaller screens */
  }
}

  </style>