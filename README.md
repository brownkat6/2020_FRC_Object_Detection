# 2020_FRC_Object_Detection
If you simply want to run a trained model that will output the location of objects and goals, scroll below to the section "Run in FRC"
If you want to retrain the model using a new/updated dataset, follow the below steps.
Train Model Using Google Cloud
1) Create a Google Cloud account. https://console.cloud.google.com/getting-started This will give you a $300 free credit that you can use to train a model.
2) Create a new "Project"
3) Setup your project
  Type "Models" in the search bar.
  Click Models (Vision), and "ENABLE AUTOML AI"
  Click the "New Dataset" button.
  Select the Object Detection model, click "Create Dataset".
4) Upload Images
  Click "Select Files" and upload the dataset(all images) from your computer.
  You will need to specify the "Destination on Cloud Storage"
  Click the icon with the + sign to create a new bucket.
  Name your new bucket, and you can click through the rest of the settings.
  Create the bucket.
  Select the bucket.
  Click "Continue" on the main page.
5) Upload Labels for your Images
  Go to https://console.cloud.google.com/storage/browser
  Upload the CSV labels file to the bucket you just created.
  Return to the original page containing your Project Dataset.
  Click "Select a CSV file on Cloud Storage"
  Click the bucket you already created.
  Find and select the labels file you uploaded to your bucket.
6) Start Training
  Switch to the "Images" tab to ensure that all of your labels and images uploaded correctly.
  Switch to the "Train" tab
  "Train New Model"
  Name your model, choose to train an "Edge" Model
  Optimize your model for "Faster predictions"
  Set the recommended 24 hour node budget.
  Start Training
7) Evaluate
  After about 8 hours, your model will finish training. At this point, switch to the "Evaluate" tab. Here you can see how well your model does, looking at images of correctly or incorrectly classified models, or examining Precision and Recall.
  Once you have finished evaluating the model, switch to the "Test & Use" tab.
  Choose to export the model as a "TF Lite" model.
  Choose which bucket to export the model to. I recommend creating a new bucket named "frc_models" and uploading the trained model there. Then, return to the page that contains
  all of your buckets (https://console.cloud.google.com/storage/browser), navigate to the "frc_models" bucket and find the "model.tflite" file that is nested within several    folders. Download this model to your local machine.
8) File format conversions
  Unfortunately, you cannot immediately run this trained model in FRC, as it is unoptimized and would be extremely slow. 
  Open a command line.
  Linux Users
    Follow the instructions here https://coral.ai/docs/edgetpu/compiler/#download to install the edge_tpu compiler.
    Navigate to the directory containing your model.tflite
    $ edgetpu_compiler model.tflite
   Windows Users
    The edge_tpu compiler does not run on Windows, but you can circumvent this by running a docker shell.
    Credit for this workaround to https://github.com/tomassams/docker-edgetpu-compiler
    Open WindowsPowerShell
    $ docker build --tag edgetpu_compiler https://github.com/tomassams/docker-edgetpu-compiler.git
    Navigate to the directory containing model.tflite
    $ docker run -it --rm -v ${pwd}:/home/edgetpu edgetpu_compiler edgetpu_compiler model.tflite
   At this point, your current directory should contain the compiled model_edgetpu.tflite directory along with a few other files. It may warn you that not all operations were compiled successfully, but you may ignore this warning.
9) Final File Organization
  Move your model_edgetpu.tflite and map.pbtxt into a folder frc_model on your computer.
  Rename model_edgetpu.tflite to be "model.tflite"
  Open a command line. Navigate to the directory containing the frc_model folder
  $ tar -zcvf model.tar.gz frc_model
  This will create a .tar.gz file containing your trained, optimized model, and the labels file.
  


Run in FRC
  https://docs.wpilib.org/en/latest/docs/software/examples-tutorials/machine-learning/inference.html
  Follow the instructions in this page using the model.tar.gz file you previously created. The python script inference.py that you will need to upload the model can be found in this repository.
  
Create map.pbtxt
  You will need to generate a map.pbtxt file if you have changed the number or label of objects your dataset identifies.
  Open a command line. Navigate to this repository. Replace Object1_Name etc. with the labels of your objects. Ex. Power_Cell
  $ python generate_pbtxt.py --classes Object1_Name Object2_Name ObjectN_Name --current_dir path/to/current/directory
  This will create map.pbtxt in the current directory.
