<br>

# Anti-sleep detection & prevention glasses demonstrated in MetaDrive simulator 


<div style="text-align: center; width:100%; margin: 0 auto; display: inline-block">
<strong>

<a href="https://github.com/metadriverse/metadrive/tree/main">The official MetaDrive repository </a>


</strong>
</div>

<br>

### Setup

Install the necessary libraries from requirements.txt:

```bash
pip install -r requirements.txt
```

You can verify the installation of MetaDrive modified repo via running the testing script:

```bash
# Go to a folder where no sub-folder calls metadrive
python -m metadrive.examples.profile_metadrive
```



### Running the simulation 
You can run the simulation that includes serial communication with the glasses. The car will drive itself when the eyes are detected as open, and sligthly swerve in a random direction while the eyes are detected as closed to imitate losing focus due to drowsiness.
```bash
python -m metadrive.examples.final_code
```
! Note that the simulation assumes you are using port COM5. Change line 12 from final_code.py to adapt it to your port.

