# Audi_Development_Camp
This App can predict the temperature based on hard coded data and also show you the previous temperatures and can compare them. Also it can show how intense some sectors are

I was in Audi Development Camp this year and it was hell of a fun and this is the project I did for my team(but I did work alone).
They wanted us to monitor their factory's water consumption level. We figure it out that the only thing what matters was monitoring and use a little bit of a prediction will give them what they need so I begin to code it 

So I think the best way to monitor prediction would be show the intensity levels on a map. If a sector on a map was intense then I will make it red and if it was not intense I will make it green same thing is goes for simulated and existing data, it is a little different for comparison grey-black for no jumps in terms of intensity and redish-pink means that sector was not intense but it will be.

I used Lineer Regression model for prediction but I could have use something much more efficient but Audi workers mentioned the lineer regression models in the slayt so we wanted to use that to impress them but it is not hard to change the model because I opened new python files for everysingle job that this thing had to do so it is easier to change things.

It might some errors or bugs in it but this is the very first project I made. Thats why it looks little complicated

Smiulate file has the Lineer Model in it is there to fit it and send the predicted water amount the required files for example intensity file
Intensity file for calculating the intensity it takes the predicted water amount and then divide it with a value that value is fixed because I had to make it a smaller value for rgb values which will be used in map coloring part. Also every sector is different from each other some of them are much intense or less intense

Data generation is the hardcoded part it uses np.random to generate data. Normally you write volume and tempurater to get predicted result but if user don't write anything here app will generate random numbers for each sector at generate_simulated_data function 

global_vars is just there the prevent collision between files 

GUI is the main code in here ever single command is executed. This file is connected to the Map_coloring file, Map_coloring file has the calculations for rgb values and gathering the values as inputs for commands in the app and start them. GUI is also works with comparison file to compare existing and simulated data.

Sector another hardcoded input I made this code usin painter to take the coordinates of each sector in the map.

Thats all I think if I forget something or made a mistake I somewhere explaining I wrote this 2 months ago I had hard time remembering everything.




