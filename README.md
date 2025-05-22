<br>

# Anti-sleep detection & prevention glasses demonstrated in MetaDrive simulator 


<div style="text-align: center; width:100%; margin: 0 auto; display: inline-block">
<strong>

<a href="https://github.com/metadriverse/metadrive/tree/main">The official MetaDrive repository which served as a base for this code</a>


</strong>
</div>

<br>

### Setup
There are 2 main steps required to be able to replicate this project and run it at home.  

## Step 1 (Run Arduino code)
-Download the Arduino IDE (version 2.3.6 was used) and upload the file `arduino_code.ino`. Select the Arduino Nano board as the controller from the interface and upload the code to the real board.  
-This code will make the buzzer activate when the eyes are detected as closed and print the responses to the serial monitor which will serve as input to the MetaDrive simulation.  
## Step 2 (Run the MetaDrive modified simulation)

Install the necessary libraries from `requirements.txt`:  

```bash
pip install -r requirements.txt
```

You can verify the installation of MetaDrive modified repository by running the testing script:  

```bash
# Go to a folder where no sub-folder calls metadrive
python -m metadrive.examples.profile_metadrive
```



### Running the simulation 
You can run the simulation that includes serial communication with the glasses. The car will drive itself when the eyes are detected as open, and sligthly swerve in a random direction while the eyes are detected as closed to imitate losing focus due to drowsiness.
```bash
python -m metadrive.examples.final_code
```
! Note that the simulation assumes you are using port COM5. Change line 12 from `final_code.py` to adapt it to your port.

### Troubleshooting
If the MetaDrive simulation does not run, try running these commands (to run a setup file from the original repository) before installing the requirements from Step 2:
```python
cd metadrive
pip install -e .
```
