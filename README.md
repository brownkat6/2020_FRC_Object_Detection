# 2020_FRC_Object_Detection
This repository is dedicated to providing a trained, ready to use object detection vision model for the 2020 FRC FIRST Robotics season. FRC began the process of providing object detection capabilities in the 2019-2020 season, as shown here. https://docs.wpilib.org/en/latest/docs/software/examples-tutorials/machine-learning/index.html Unfortunately, the platform they used to train the model, AWS, has permissions issues that as of September 2020 remain unresolved. Thus, this repository provides a tutorial for using Google Cloud to train an object detection model. However, it will reference several of the steps outlined by FIRST(to get the original dataset, and to provide the inference.py script that is used to run the trained model on the RoboRio), and for those I take no credit.

If you simply want to get a pre-trained model that will output the location of Power Cells and Upper Power Ports, scroll below to the section "Run in FRC"
If you want to retrain the model using a new/updated dataset, follow the steps in "Get New Labeled Data".

Get New Labeled Data  
  1) https://docs.wpilib.org/en/latest/docs/software/examples-tutorials/machine-learning/setting-up-the-data.html
  Follow the instructions here. However, our team has labeled several hundred additonal images, so instead of using the Supervisely link provided by WPILib, use this link https://app.supervise.ly/share-links/vlZ5F1mj5N6qxB1Ud6KsI1N7QEJr5OPZ3LYkNyFdh946ZEHihPPWwP1VaYP6Ncwq when cloning the dataset.
  2) Label additional data using Supervisely.  
  3) Download Raw Data as .json + images  
  4) Move data into the input folder of this repository  
  Directory structure
  -2020_FRC_Object_Detection
    -input
      -Raw Data
        -Filming Day 1 Images
        -Filming Day 1 Video
        -Filming Day 2 Video
      -all_images
  5) Format New Labeled Data  
    $ python generate_gcloud_labels.py --bucket_name data_bucket_name --current_dir path/to/repository/
    This will create a bucket_name_labels.csv file that you can upload to Google Cloud. These are your labels to tell the model where each object is in the image.
    This will move all of your images into the all_images folder. You may upload all of the images in this folder to your data bucket in Google Cloud.
  6) Create map.pbtxt  
    This file contains the labels for each object you are identifying.
    You will need to generate a map.pbtxt file if your dataset contains new types of labeled objects(e.g. it also identifies the Lower Power Port).
    Open a command line. Navigate to this repository. Replace Object1_Name etc. with the labels of your objects. Ex. Power_Cell
    $ python generate_pbtxt.py --classes Object1_Name Object2_Name ObjectN_Name --current_dir path/to/current/directory
  This will create map.pbtxt in the current directory.
  7) You are now ready to "Train Model Using Google Cloud"

Train Model Using Google Cloud \n
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
  Almost There! You are now ready to move to the section "Run in FRC"


Run in FRC  
  https://docs.wpilib.org/en/latest/docs/software/examples-tutorials/machine-learning/inference.html
  Follow the instructions in this page using the model.tar.gz file you previously created. The python script inference.py that you will need to upload the model can be found in this repository.
